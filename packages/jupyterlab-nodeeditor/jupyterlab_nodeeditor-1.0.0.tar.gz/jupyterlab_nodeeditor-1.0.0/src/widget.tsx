import { DocumentWidget, DocumentRegistry } from "@jupyterlab/docregistry"
import {
    Dialog,
    showDialog,
    SessionContextDialogs,
    ReactWidget,
    ICommandPalette,
} from "@jupyterlab/apputils";
import {
    JupyterFrontEnd,
} from "@jupyterlab/application"
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';
import { KernelError } from "@jupyterlab/notebook";
import { KernelMessage } from '@jupyterlab/services';
import { IOutput } from '@jupyterlab/nbformat';
import { NodeBookModel } from "./model";
import { OutputArea, OutputAreaModel } from "@jupyterlab/outputarea"
import { CodeCellModel, CellModel } from "@jupyterlab/cells"
import {
    RenderMimeRegistry,
    standardRendererFactories
} from '@jupyterlab/rendermime';
import {
    NodeMap,
    FlumeConfig,
    generateMenuOption,
    Ower,
    NodeEditor,
    GetSvgContainerRef,
    SvgContainerStyle,
    ContextMenu
} from "../flume";
import React, { useState } from "react"
import createConfig, {
    setImageUrls,
    refreshImageUrls,
    get_port_func,
    tuple_value_name,
    get_tuple_max_index,
    parse_dict_name,
    headerFontsize,
    nodeMinWidth,
    nodeMaxWidth,
    common_out,
} from "./flumeConfig"
import { v4 as uuidv4 } from "uuid"
import { buildNodeWidth, cloneDeep, nextFrame, findAll } from './utils'
import RunIcon from "./runIcon";
import DeleteIcon from "./deleteIcon";
import ImageViewer from "./imageViewer";
import ReRunIcon from "./ReRunIcon";
import LockIcon from "./lockIcon";
import ArrownIcon from "./arrownIcon";
import ClearIcon from "./clearIcon";
import ExportIcon from "./exportIcon";
import YesIcon from "./yesIcon";
import * as monaco from 'monaco-editor';

const nodeInitBoxShadow = "0px 4px 8px rgba(0,0,0,0)"
const nodeSelectedBoxShadow = "0px 0px 10px 10px rgb(0 216 255)"
const nodeRunningBoxShadow = "rgb(52 255 223) 0px 0px 7px 10px"
const nodeErrorBoxShadow = "rgb(255 38 227) 0px 0px 10px 10px"
const kernelStateMap = {
    "idle": "空闲",
    "busy": "繁忙"
}
export class NodeEditorWidget extends ReactWidget {
    private _context: DocumentRegistry.IContext<NodeBookModel>; // 上下文
    private _app: JupyterFrontEnd
    private _palette: ICommandPalette
    private _settings: ISettingRegistry
    private _isReady: boolean = false   // 是否一切都准备就绪了
    private _stopCreateNodeType = false // 是否停止向python请求complete
    private _internal_options: any[] = [] // 内部选项，用于右键菜单的选项
    private _isSaveNodes = true // 是否保存nodes,用于有时候需要阻止修改nodes
    private _curNodesId = ""    // 当前的nodes的ID
    private _loadingNodes = false   // 是否正在加载节点数据
    private _nodeTypes = {} // 缓存的节点类型，用于在保存节点的时候保存到文件中，加载节点时，直接用
    private _redoList: any[] = [] // 保存的操作和它的反向操作，用于撤销和重做
    private _redoListIndex = 0 // 操作的索引，用于指示当前撤销到了哪一步
    private _redoListMaxLength = 200 // 用于限制_redoList要保存多少步的操作
    private _redoing: any = null // 是否正在执行撤销或重做操作
    private _renderCache: any = null // 渲染缓存，由于render()函数会重复执行，所以，缓存一份渲染出来的组件，用于快速返回，并且避免重复执行
    private _mouseMove!: MouseEvent; // 鼠标移动事件的缓存，用于多种操作
    private _dragging = false // 是否正在执行快速拖拽操作
    private _dragStartPos: MouseEvent | null = null // 拖拽操作的起始点
    private _dragXDistance = 0 // 拖拽进行的位移X
    private _dragYDistance = 0 // 拖拽进行的位移Y
    private _scaling = false // 是否正在进行缩放操作
    private _scaleStartPos: MouseEvent | null = null // 缩放的目标点
    private _scaleDistance = 0 // 缩放的距离，用于计算缩放的大小
    private _scaleXDistance = 0 // 由于缩放引起的位置偏移X
    private _scaleYDistance = 0 // 由于缩放引起的位置偏移Y
    private _preAction: any = null // 用于记录上次出发的action, 防止由于机制问题导致的重复触发
    private _copyedNodes: any = null // 拷贝的节点
    private _containerRef: any = null // 当前组件最外层的div
    private _editorContainerRef: any = null // 编辑器外层的div
    private _draggingSelectedNodes = false // 是否正在拖拽选择的节点
    private _stageDragging = false // 是否在拖拽背景
    private _showSelectRect: any // 是否显示选择框
    private _selectRectRef: any = null // 用于保存选择框
    private _drawStartPos: MouseEvent | null = null // 拖拽操作的起始点
    private _lockedNodes = new Set<string>() // 锁住的节点
    private _headRenderCache: any = {} // 节点头部渲染缓存
    private _runCache = {} // 运行缓存
    private _runCheckCache = true // 是否检查运行缓存
    private _outputArea: OutputArea
    private _showOutputArea
    private _setShowOutputArea
    private _outputAreaContainerRef
    private _outputAreaAutoScroll = true
    private _runningNodeId: any = null
    private _runningError = false
    private _exportingCodeNodeId = null
    private _exportRet: any[] = []
    private _exportIndent = ""
    private _showMsgToNotebook = true
    private _setshowCodeEditor
    private _codeEditorValueCache = ""
    private _saveCode: any = null
    private _setUseDiffEditor
    private _curEditingCellIndex = -1
    private _stopFilterCell = false
    private _codeEditor: monaco.editor.IStandaloneCodeEditor | null = null
    private _codeDiffEditor: monaco.editor.IStandaloneDiffEditor | null = null
    private _cellIndexInputRef
    private _renameCache = ""
    private _interruptingKernel = false


    scaleSpeed = 0.01 // 缩放的速度，_scaleDistance * scaleSpeed 就是新的缩放值
    selectedNodes = new Set<string>() // 选择的节点
    keyEventFilter = new Set<string>()// 按键过滤器，用于过滤键盘操作
    editorOptions = {} // 有flume导出的函数变量等。。
    setShowImg: any // 用于设置是否打开图片查看器 setShowImg(true/false)
    setShowImgUrls: any // 用于设置图片查看器的urls数据
    setShowImgStartIndex: any // 用于设置图片查看器当前的图片地址索引，img的src=[urls[index]]
    curNodeName = "" // 当前节点数据的名称
    setCurNodeName: any // 用于设置curNodeName
    editorNodes: NodeMap = {}  // 编辑器内当前的节点数据
    setEditorNodes: any // 用于同步节点数据到编辑器
    editorConfig: FlumeConfig // flume的配置文件state,
    setEditorConfig: any // 用于将flume配置修改传递到编辑器
    dispatchNodes: any // 从flume里面导出来的函数，用于在外面修改nodes
    getInitialNodes: any // 从flume里面导出来的函数，用于解析存储的nodes

    constructor(
        context: DocumentRegistry.IContext<NodeBookModel>,
        app: JupyterFrontEnd,
        palette: ICommandPalette,
        settings: ISettingRegistry,
    ) {
        super();
        this._context = context;
        this._app = app
        this._palette = palette
        this._settings = settings

        let that = this
        this._context.model.sharedModel.changed.connect((sender, change) => {
            this.onContentChanged(sender, change)
        });

        this._context.sessionContext.ready.then(async (value) => { await that.onReady() })
        this._context.saveState.connect(() => { that.onSaveState() })
        this.editorConfig = createConfig()

        // 创建输出框
        const rendermime = new RenderMimeRegistry({
            initialFactories: standardRendererFactories
        });
        const model = new OutputAreaModel();
        this._outputArea = new OutputArea({
            model,
            rendermime,
        });
        model.changed.connect(() => { this._onOutputModelChanged() })


        // 注册python的语法
        monaco.languages.register({ id: "python" })
        monaco.languages.setMonarchTokensProvider("python", {
            defaultToken: '',
            tokenPostfix: '.python',
            keywords: [
                'and',
                'as',
                'assert',
                'break',
                'class',
                'continue',
                'def',
                'del',
                'elif',
                'else',
                'except',
                'exec',
                'finally',
                'for',
                'from',
                'global',
                'if',
                'import',
                'in',
                'is',
                'lambda',
                'None',
                'not',
                'or',
                'pass',
                'print',
                'raise',
                'return',
                'self',
                'try',
                'while',
                'with',
                'yield',

                'int',
                'float',
                'long',
                'complex',
                'hex',

                'abs',
                'all',
                'any',
                'apply',
                'basestring',
                'bin',
                'bool',
                'buffer',
                'bytearray',
                'callable',
                'chr',
                'classmethod',
                'cmp',
                'coerce',
                'compile',
                'complex',
                'delattr',
                'dict',
                'dir',
                'divmod',
                'enumerate',
                'eval',
                'execfile',
                'file',
                'filter',
                'format',
                'frozenset',
                'getattr',
                'globals',
                'hasattr',
                'hash',
                'help',
                'id',
                'input',
                'intern',
                'isinstance',
                'issubclass',
                'iter',
                'len',
                'locals',
                'list',
                'map',
                'max',
                'memoryview',
                'min',
                'next',
                'object',
                'oct',
                'open',
                'ord',
                'pow',
                'print',
                'property',
                'reversed',
                'range',
                'raw_input',
                'reduce',
                'reload',
                'repr',
                'reversed',
                'round',
                'set',
                'setattr',
                'slice',
                'sorted',
                'staticmethod',
                'str',
                'sum',
                'super',
                'tuple',
                'type',
                'unichr',
                'unicode',
                'vars',
                'xrange',
                'zip',

                'True',
                'False',

                '__dict__',
                '__methods__',
                '__members__',
                '__class__',
                '__bases__',
                '__name__',
                '__mro__',
                '__subclasses__',
                '__init__',
                '__import__'
            ],

            brackets: [
                { open: '{', close: '}', token: 'delimiter.curly' },
                { open: '[', close: ']', token: 'delimiter.bracket' },
                { open: '(', close: ')', token: 'delimiter.parenthesis' }
            ],

            tokenizer: {
                root: [
                    { include: '@whitespace' },
                    { include: '@numbers' },
                    { include: '@strings' },

                    [/[,:;]/, 'delimiter'],
                    [/[{}\[\]()]/, '@brackets'],

                    [/@[a-zA-Z]\w*/, 'tag'],
                    [/[a-zA-Z]\w*/, {
                        cases: {
                            '@keywords': 'keyword',
                            '@default': 'identifier'
                        }
                    }]
                ],

                // Deal with white space, including single and multi-line comments
                whitespace: [
                    [/\s+/, 'white'],
                    [/(^#.*$)/, 'comment'],
                    [/('''.*''')|(""".*""")/, 'string'],
                    [/'''.*$/, 'string', '@endDocString'],
                    [/""".*$/, 'string', '@endDblDocString']
                ],
                endDocString: [
                    [/\\'/, 'string'],
                    [/.*'''/, 'string', '@popall'],
                    [/.*$/, 'string']
                ],
                endDblDocString: [
                    [/\\"/, 'string'],
                    [/.*"""/, 'string', '@popall'],
                    [/.*$/, 'string']
                ],

                // Recognize hex, negatives, decimals, imaginaries, longs, and scientific notation
                numbers: [
                    [/-?0x([abcdef]|[ABCDEF]|\d)+[lL]?/, 'number.hex'],
                    [/-?(\d*\.)?\d+([eE][+\-]?\d+)?[jJ]?[lL]?/, 'number']
                ],

                // Recognize strings, including those broken across lines with \ (but not without)
                strings: [
                    [/'$/, 'string.escape', '@popall'],
                    [/'/, 'string.escape', '@stringBody'],
                    [/"$/, 'string.escape', '@popall'],
                    [/"/, 'string.escape', '@dblStringBody']
                ],
                stringBody: [
                    [/[^\\']+$/, 'string', '@popall'],
                    [/[^\\']+/, 'string'],
                    [/\\./, 'string'],
                    [/'/, 'string.escape', '@popall'],
                    [/\\$/, 'string']
                ],
                dblStringBody: [
                    [/[^\\"]+$/, 'string', '@popall'],
                    [/[^\\"]+/, 'string'],
                    [/\\./, 'string'],
                    [/"/, 'string.escape', '@popall'],
                    [/\\$/, 'string']
                ]
            }
        })
        monaco.languages.registerCompletionItemProvider("python", {
            triggerCharacters: ['.'],
            provideCompletionItems: async (model, position) => {
                return await this._codeEditorprovideCompletionItems(model, position)
            },
        });

        // 创建命令
        this._createCommands()
    }

    dispose(): void {
        if (this.isDisposed) {
            return;
        }
        super.dispose();
    }

    render() {
        const Ret = () => {
            // 管理图片浏览器的开关
            const [showImg, setShowImg] = useState(false)
            this.setShowImg = setShowImg
            // 图片浏览器的数据
            const [showImgUrls, setShowImgUrls] = useState(false)
            this.setShowImgUrls = setShowImgUrls
            // 当前图片的索引
            const [showImgStartIndex, setShowImgStartIndex] = useState(0)
            this.setShowImgStartIndex = setShowImgStartIndex

            // 节点编辑器的节点类型配置
            const [conf, setConf] = useState(this.editorConfig)
            this.editorConfig = conf
            this.setEditorConfig = setConf

            // 当前的节点
            const [nodes, setNodes] = useState(this.editorNodes)
            this.editorNodes = nodes
            this.setEditorNodes = setNodes

            // 节点的名称
            const [nodesName, setNodesName] = useState("未命名")
            this.curNodeName = nodesName
            this.setCurNodeName = setNodesName

            // 用来保存最外层控件
            const containerRef = React.useRef(null)
            this._containerRef = containerRef

            // 输出引用
            const outputAreaContainerRef = React.useRef(null)
            this._outputAreaContainerRef = outputAreaContainerRef

            // 输出控制
            const [showOutput, setShowOutput] = useState(false)
            this._showOutputArea = showOutput
            this._setShowOutputArea = setShowOutput

            // 编辑器容器
            const editorContainerRef = React.useRef(null)
            this._editorContainerRef = editorContainerRef

            // 编辑器控制
            const [showCodeEditor, setshowCodeEditor] = useState(false)
            this._setshowCodeEditor = setshowCodeEditor
            const codeEditorRef = React.useRef(null)
            const [useDiffEditor, setUseDiffEditor] = useState(false)
            this._setUseDiffEditor = setUseDiffEditor
            const [codeEditorMenuOpen, setCodeEditorMenuOpen] = React.useState(false);
            const [menuCoordinates, setMenuCoordinates] = React.useState({ x: 0, y: 0 });
            const [codeEditorMenuOptions, setCodeEditorMenuOptions] = useState([] as any)
            const cellIndexInputRef = React.useRef(null)
            this._cellIndexInputRef = cellIndexInputRef

            // 注册键盘事件
            const handleKeyDown = async e => { await this.onKeyDown(e) }
            const handleKeyUp = async e => { await this.onkeyUp(e) }
            const mouseMove = async e => { await this.onMouseMove(e) }
            const handleMouseEnter = e => {
                this._mouseMove = e
            }

            React.useEffect(() => {
                if (!showImg) {
                    // 获取真个Draggable组件
                    const draggableRef = this.editorOptions["draggableRef"]
                    if (draggableRef.current) {
                        // 获取焦点，否则不能进行空格位移操作
                        draggableRef.current.focus()
                    }
                    this.keyEventFilter.clear()
                } else {
                    this._commonFilterKeys()
                    this._setshowCodeEditor(false)
                    this._setShowOutputArea(false)
                }
            }, [showImg])

            const preScrollTop = React.useRef(0)
            React.useEffect(() => {
                const element = outputAreaContainerRef.current as unknown as HTMLElement
                let left = "0px"
                let width = "100%"
                if (showOutput) {
                    ReactWidget.attach(
                        this._outputArea,
                        element,
                        null
                    )
                    this._outputArea.show()
                    element.scrollTop = element.scrollHeight - element.clientHeight;
                    const rect = element.getBoundingClientRect()
                    left = `${rect.width}px`
                    const container = containerRef.current as unknown as HTMLDivElement
                    const containerRect = container.getBoundingClientRect()
                    width = `${(containerRect.width - rect.width) / containerRect.width * 100}%`

                    // 保存一些必要数据
                    preScrollTop.current = element.scrollTop
                }

                // 设置编辑器的位置和宽度
                let editor = editorContainerRef.current as unknown as HTMLElement
                editor.style.left = left
                editor.style.width = width


            }, [showOutput])

            const onOutputAreaScroll = (e: React.UIEvent<HTMLDivElement, UIEvent>) => {
                let element = e.target as HTMLDivElement

                // 计算滚动方向
                let scrollUp = element.scrollTop - preScrollTop.current < 0
                if (scrollUp) {
                    this._outputAreaAutoScroll = false
                } else if (!this._outputAreaAutoScroll) {
                    this._outputAreaAutoScroll = element.scrollHeight - element.scrollTop < element.clientHeight + 1
                }

                preScrollTop.current = element.scrollTop
            }


            React.useEffect(() => {
                if (!showCodeEditor) {
                    // 获取真个Draggable组件
                    const draggableRef = this.editorOptions["draggableRef"]
                    if (draggableRef.current) {
                        // 获取焦点，否则不能进行空格位移操作
                        draggableRef.current.focus()
                    }
                    this.keyEventFilter.clear()
                    this._setShowOutputArea(false)
                    if (this._codeDiffEditor) {
                        this._codeDiffEditor = null
                    }
                    if (this._codeEditor) {
                        this._codeEditor = null
                    }
                } else {
                    this._commonFilterKeys()
                    this.setShowImg(false)
                    if (codeEditorRef.current) {
                        if (useDiffEditor) {
                            this._codeDiffEditor = monaco.editor.createDiffEditor(
                                codeEditorRef.current as unknown as HTMLElement,
                                {
                                    originalEditable: true,
                                    automaticLayout: true,
                                    theme: "vs-dark",
                                }
                            )
                            this._codeDiffEditor.focus()
                        } else {
                            this._codeEditor = monaco.editor.create(
                                codeEditorRef.current as unknown as HTMLElement, {
                                theme: "vs-dark",
                                language: "python",
                            })

                            this._codeEditor.focus()

                            this._codeEditor.onDidChangeModelContent(e => {
                                this._onCodeEditorChange(this._codeEditor?.getValue(), e)
                            })

                            this._codeEditor.onContextMenu(e => {
                                handleCodeEditorContextMenu(e)
                            })
                        }
                    }

                }
            }, [showCodeEditor])

            const handleCodeEditorContextMenu = (e: monaco.editor.IEditorMouseEvent) => {
                e.event.preventDefault()
                setMenuCoordinates({ x: e.event.posx, y: e.event.posy });
                setCodeEditorMenuOpen(true)
                setTimeout(() => {
                    let inputElement = document.querySelector('[data-flume-component="ctx-menu-input"]') as HTMLInputElement
                    inputElement.focus()
                })
                return false;
            }


            const closeContextMenu = () => {
                setCodeEditorMenuOpen(false);
            };


            React.useEffect(() => {
                if (codeEditorMenuOpen) {
                    const length = this._context.model.cells.length
                    const options: any[] = []
                    for (let index = 0; index < length; index++) {
                        options.push({
                            label: `Cell_${index}`,
                            value: {
                                cellIndex: index,
                                startLine: 0,
                                startColumn: 0,
                                endLine: 0,
                                endColumn: 0
                            },
                            description: `Cell_${index}`
                        })
                    }
                    setCodeEditorMenuOptions(options)
                }
            }, [codeEditorMenuOpen])

            const iconLength = 24
            const codeEditorIconLength = 50
            return <Ower.Provider value={this}>
                <div ref={containerRef}
                    className="nd-container"
                    onKeyDown={handleKeyDown}
                    onKeyUp={handleKeyUp}
                    onMouseMove={mouseMove}
                    onMouseEnter={handleMouseEnter}
                    data-show-image-viewer={showImg}
                    data-show-code-editor={showCodeEditor}
                    data-use-diff-editor={useDiffEditor}
                    data-inputing="falses"
                >
                    {/* 输出浏览器 */}
                    {showOutput && <div
                        style={{
                            position: "absolute",
                            left: "0px",
                            top: "0px",
                            backgroundColor: "white",
                            width: "30%",
                            height: "100%",
                            resize: "horizontal",
                        }}
                    >
                        <div style={{
                            display: "flex",
                            alignItems: "center",
                            float: "right",
                        }}>
                            <ClearIcon onClick={e => {
                                this._clearOutputArea()
                            }} width={iconLength} height={iconLength} leaveColor="black" />
                            <ArrownIcon onClick={() => {
                                const element = outputAreaContainerRef.current as unknown as HTMLElement
                                element.scrollTop = 0;
                            }} width={iconLength} height={iconLength} rotate="90deg" leaveColor="black" />
                            <ArrownIcon onClick={() => {
                                const element = outputAreaContainerRef.current as unknown as HTMLElement
                                element.scrollTop = element.scrollHeight - element.clientHeight;
                            }} width={iconLength} height={iconLength} rotate="-90deg" leaveColor="black" />
                            <DeleteIcon onClick={() => {
                                try { ReactWidget.detach(this._outputArea) } catch { }
                                setShowOutput(false)
                            }} width={iconLength} height={iconLength} leaveColor="black" />
                        </div>
                        <div ref={outputAreaContainerRef}
                            style={{
                                width: "100%",
                                height: `calc(100% - ${iconLength}px)`,
                                overflowY: "scroll",
                            }}
                            onScroll={onOutputAreaScroll}
                        ></div>

                    </div>}
                    <div
                        ref={editorContainerRef}
                        style={{
                            position: "absolute",
                            left: "0px",
                            top: "0px",
                            width: "100%",
                            height: "100%",
                        }}>
                        {/* 编辑器 */}
                        <NodeEditor nodeTypes={conf.nodeTypes}
                            portTypes={conf.portTypes}
                            circularBehavior="allow"
                            onChange={nodes => this.onNodesChange(nodes)}
                            context={this}
                            renderNodeHeader={(header, currentNodeType, options, id) => {
                                return this.renderNodeHeader(header, currentNodeType, options, id)
                            }}
                        ></NodeEditor>
                        {/* 上层工具栏 */}
                        <div style={{ position: "absolute", right: "0px", top: "0px" }} >
                            <span style={{
                                alignItems: "center",
                                color: "#fff",
                            }}>
                                <label>名称:({nodesName})</label>
                                <br />
                                <label data-name="node-editor-kernel-state-label" style={{
                                    height: "100%",
                                    backgroundColor: "rgba(0, 0, 0, 0)"
                                }}>空闲</label>
                            </span>
                        </div>
                        {/* 图片浏览器 */}
                        {showImg && <div style={{
                            position: "absolute", left: "0px", top: "0px",
                            width: "100%",
                            height: "100%",
                        }}>
                            <ImageViewer src={showImgUrls} startIndex={showImgStartIndex} />
                            <div style={{
                                position: "absolute", right: "0px", top: "0px",
                            }}>
                                <DeleteIcon onClick={() => {
                                    this.setShowImg(false)
                                }} width={"100px"} height={"100px"} />
                            </div>
                        </div>}

                        {/* 代码编辑器 */}
                        {showCodeEditor && <div style={{
                            position: "absolute", left: "0px", top: "0px",
                            width: "100%",
                            height: "100%",
                            backgroundColor: "black",
                        }}
                        >
                            <div style={{
                                width: "100%",
                                height: "100%",
                            }}
                                ref={codeEditorRef}
                            ></div>
                            {
                                codeEditorMenuOpen && <ContextMenu
                                    x={menuCoordinates.x}
                                    y={menuCoordinates.y}
                                    options={codeEditorMenuOptions}
                                    onRequestClose={closeContextMenu}
                                    onOptionSelected={(option) => {
                                        this._onSelectedCodeEditorOption(option)
                                    }}
                                    label="搜索cell"
                                    from="codeEditor"
                                />
                            }
                            <div style={{
                                position: "absolute", right: "0px", top: "0px",
                                zIndex: 100,
                                display: "flex",
                                alignItems: "center",
                            }}>
                                {
                                    useDiffEditor && <YesIcon onClick={() => {
                                        setshowCodeEditor(false)
                                        if (this._saveCode) {
                                            this._saveCode()
                                        }
                                    }}
                                        width={codeEditorIconLength}
                                        height={codeEditorIconLength}
                                    />
                                }
                                <RunIcon onClick={() => {
                                    this._editorRun()
                                }} width={codeEditorIconLength} height={codeEditorIconLength} />
                                <DeleteIcon onClick={() => {
                                    setshowCodeEditor(false)
                                    this._saveCode = null
                                    this._curEditingCellIndex = -1
                                }} width={codeEditorIconLength} height={codeEditorIconLength}
                                />
                            </div>
                            <div style={{
                                position: "absolute", left: "0px", bottom: "0px",
                                zIndex: 100,
                            }}>
                                <label data-name="node-editor-kernel-state-label" style={{
                                    height: "100%",
                                    color: "white",
                                }}>空闲</label>
                                <br />
                                {!useDiffEditor && <span>
                                    <label style={{
                                        height: "100%",
                                        color: "white",
                                    }}>当前索引:</label>
                                    <input
                                        ref={cellIndexInputRef}
                                        type="number"
                                        onChange={e => {
                                            let value = Number(e.target.value)
                                            if (value < 0) {
                                                e.target.value = "0"
                                                value = 0
                                            }
                                            const maxValue = this._context.model.cells.length - 1
                                            if (value > maxValue) {
                                                value = maxValue
                                                e.target.value = `${maxValue}`
                                            }
                                            this._editCell(value)
                                        }}
                                    /></span>
                                }
                            </div>
                        </div>}
                    </div>
                </div>
            </Ower.Provider>
        }

        if (this._renderCache == null) {
            this._renderCache = <Ret />
        }

        // 刷新选择表现
        this.refreshNodeBoxShadow()

        return this._renderCache
    }

    async onKeyDown(e: KeyboardEvent) {
        if (this.keyEventFilter.has(e.key)) {
            return
        }
        // console.log(e)
        switch (e.key) {
            case " ": {
                this._startDrag()
            } break
            case "s": {
                this._startScale()
            } break
            case "a": {
                if (!e.ctrlKey) {
                    if (this._isDraggableFocus())
                        this._startDrawSelect()
                }
            } break
        }
    }

    async onkeyUp(e: KeyboardEvent) {
        if (this.keyEventFilter.has(e.key)) {
            return
        }
        switch (e.key) {
            case " ": {
                this._stopDrag()
            } break
            case "s": {
                this._stopScale()
            } break
            case "a": {
                if (!e.ctrlKey)
                    this._stopDrawSelect()
            } break

        }
    }

    async onMouseMove(e: MouseEvent) {
        this._mouseMove = e
        this._drag(e)
        this._scale(e)
        this._drawSelect(e)
    }

    async onReady() {
        // this._checkSessionAndKernel(null)首先要检测，必须要有内核
        if (!await this._checkSessionAndKernel(null)) {
            return false
        }

        // this._initPython() 必须在 this._loadNodesFromAllCell()之前
        if (!await this._initPython()) {
            return false
        }

        // 加载第一个节点
        let nodes = this._loadNodesFromAllCell()
        if (nodes.length > 0) {
            if (!await this._loadNodes(nodes[0].data)) {
                showDialog({
                    title: "加载节点失败",
                    body: "加载节点失败，请重新加载节点",
                    buttons: [Dialog.okButton({ label: 'Ok' })]
                });
                return false
            }
        }

        this._isReady = true
        return true
    }


    async runAllCells() {
        for (let index = 0; index < this._context.model.cells.length; index++) {
            const cell = this.cellGet(index);
            if (cell.type == "code") {
                await this._runCell(cell as CodeCellModel, nullTranslator)
            }
        }
        this._context.save()
    }

    async createNewNodes() {
        this._isSaveNodes = false
        this._curNodesId = ""
        this.setCurNodeName("未命名")
        this._clearNodes()
        this._isSaveNodes = true
    }

    async onConnectToSpace(e, nodeId, portName) {
        // let node = this.editorNodes[nodeId]
        // if (!node) {
        //     return
        // }

        // let outVarName = this._get_out_var_name(nodeId)
        // switch (node.type) {
        //     case "image":
        //         if (portName == "curUrl") {
        //             outVarName = `${outVarName}_cur`
        //         }
        //         break
        //     default:
        //         let ret = /instance@(get|set)@(.*)/g.exec(node.type)
        //         if (ret) {
        //             outVarName = ret[2]
        //         }
        //         break
        // }

        // this._setMenuOpen(`${outVarName}`)
    }

    async runNode(id, clearCache = false) {
        this._interruptingKernel = false
        this._showMsgToNotebook = true
        this._stopCreateNodeType = true
        this._clearCurOutput()
        let removeList = [id]
        let exceptIds: any = []
        if (clearCache) {
            for (const nodeId in this._runCache) {
                if (this._lockedNodes.has(nodeId)) {
                    exceptIds = [
                        ...await this._getNodeInputLinkedNodes(nodeId),
                        ...exceptIds,
                        nodeId,
                    ]
                }
                removeList.push(nodeId)
            }
        }
        exceptIds = new Set(exceptIds)
        for (const nodeId of removeList) {
            if (exceptIds.has(nodeId) && nodeId != id) {
                continue
            }
            delete this._runCache[nodeId]
        }

        this._setRunningNode(id)
        this.refreshNodeBoxShadow()
        this._runCache[id] = await this._runNode(id)
        this._saveNodes(this.editorNodes)
        this._setRunningNode(0)
        this.refreshNodeBoxShadow()
    }

    async deleteNodes() {
        let ret = await showDialog({
            title: "确定要删除吗？",
            body: "确定要删除吗？删除就没了哦",
            buttons: [Dialog.cancelButton({ label: "取消" }),
            Dialog.okButton({ label: '确定' })]
        });

        if (ret.button.label != "确定") {
            return
        }

        this._clearNodes()
        setTimeout(() => {
            let index = this._getNodesCellIndex(this._curNodesId)
            if (index == null) {
                return
            }
            console.log("_deleteNodes", this._curNodesId)
            this._context.model.sharedModel.deleteCell(index)
            let nodes = this._loadNodesFromAllCell()
            if (nodes.length > 0) {
                this._loadNodes(nodes[0].data)
            }
        }, 50);
    }

    async save() {
        await this._context.save()
    }

    async redo(direct) {
        // 检测是否有历史
        if (this._redoList.length == 0) {
            return
        }

        // 获取目标index
        let target_index = this._redoListIndex + direct
        if (target_index < 0 || target_index >= this._redoList.length) {
            return
        }
        this._redoListIndex = target_index
        let action = this._redoList[this._redoListIndex]
        if (direct > 0) {
            action = action.action
        } else {
            action = action.redoAction
        }
        this._redoing = action
        console.log("redo", action, this._redoListIndex)
        this.dispatchNodes(action)
    }



    refreshNodeBoxShadow() {
        // 刷新选择表现
        let element: HTMLElement | null
        for (const id in this.editorNodes) {
            element = document.getElementById(id)
            if (!element) {
                continue
            }
            this._setNodeBoxShadow(id, nodeInitBoxShadow)
        }
        this._refreshSelectedNodes()
        this._refreshRunningNode()
    }

    async onNodeStartDrag(id, nodeElement: HTMLElement) {
        if (this.selectedNodes.has(id)) {
            this._draggingSelectedNodes = true
        }
    }

    async onNodeMouseDown(e: MouseEvent, id, nodeElement: HTMLElement) {
        // 判断该节点是否在选择的节点中
        if (this.selectedNodes.has(id)) {
            // 对所有的选中节点发送鼠标按下的事件
            for (const nodeId of this.selectedNodes) {
                if (nodeId == id) {
                    continue
                }
                const startDragDelay = this.editorOptions[`startDragDelay_${nodeId}`].current
                if (startDragDelay) {
                    startDragDelay(e)
                }
            }
        }
    }

    async onNodeMouseUp(e: MouseEvent, id, nodeElement: HTMLElement) {
        if (!this._draggingSelectedNodes) {
            // 处理选择操作
            if (e.button == 0) {
                // 处理多选
                if (e.ctrlKey) {
                    if (this.selectedNodes.has(id)) {
                        this.selectedNodes.delete(id)
                    } else {
                        this.selectedNodes.add(id)
                    }
                }
                // 处理单选
                else {
                    this.selectedNodes.clear()
                    this.selectedNodes.add(id)
                }

                // 需要延时一下，
                // 因为refreshSelectedNodes里面会出发界面的刷新，导致如何点到按钮会执行不到按钮的事件
                setTimeout(() => {
                    this.refreshNodeBoxShadow()
                })
            }
        }

        this._draggingSelectedNodes = false
    }


    async onStageDraggableMouseDown(e: MouseEvent) {
    }


    async onStageDraggableMouseUp(e: MouseEvent) {
        if (!this._stageDragging) {
            this.selectedNodes.clear()
            this.refreshNodeBoxShadow()
        }
        this._stageDragging = false
    }

    async onStageStartDrag(e: MouseEvent) {
        this._stageDragging = true
    }

    onSaveState() {
    }

    onNodesChange(nodes: NodeMap) {
        console.log("onNodesChange", nodes)
        if (!this._checkReady(false)) {
            return
        }
        refreshImageUrls(this)
        this._saveNodes(nodes)
        if (this._redoing) {
            switch (this._redoing.type) {
                case "SET_NODE_COORDINATES": {
                    this.updateNodeConnections(this._redoing.nodeId)
                } break
                case "SET_PORT_DATA": {
                    this._setNodePortControlInputValue(
                        this._redoing.nodeId,
                        this._redoing.portName,
                        this._redoing.controlName,
                        this._redoing.data
                    )
                } break
            }
            this._redoing = null
        }

        // 执行一些后处理
        setTimeout(() => {
            this._updateHeaderCache()
        });
    }

    onNodeAction(nodes, action, nanoid) {
        if (this._redoing != null) {
            return
        }

        if (this._preAction == action) {
            return
        }
        this._preAction = action

        let redoAction
        switch (action.type) {
            case "CLEAR":
            case "RE_INIT":
                this._redoList = []
                this._redoListIndex = 0
                let draggableRef = this.editorOptions["draggableRef"]
                if (document.activeElement != draggableRef.current)
                    draggableRef.current.focus()
                return
            case "SET_NODE_COORDINATES": {
                const node = nodes[action.nodeId]
                if (!node) return
                redoAction = {
                    ...action,
                    x: node.x,
                    y: node.y
                }
            } break
            case "SET_PORT_DATA": {
                const node = nodes[action.nodeId]
                if (!node) return
                let prePortData = node.inputData[action.portName]
                let pre_data = null
                if (prePortData) {
                    pre_data = prePortData[action.controlName]
                }
                redoAction = {
                    ...action,
                    data: pre_data
                }
            } break
            case "REMOVE_NODE": {
                const node = nodes[action.nodeId]
                if (!node) return
                redoAction = {
                    type: "ADD_NODE",
                    node
                }
            } break
            case "REMOVE_NODES": {
                const removed_nodes: any[] = []
                for (const nodeId of action.nodeIds) {
                    const node = nodes[nodeId]
                    if (!node) continue
                    removed_nodes.push(node)
                }
                redoAction = {
                    type: "ADD_NODES",
                    nodes: removed_nodes
                }

            } break
            case "ADD_NODE": {
                action.id = action.id || nanoid(10)
                redoAction = {
                    type: "REMOVE_NODE",
                    nodeId: action.id
                }
            } break
            case "ADD_NODES": {
                const nodeIds: any[] = []
                for (const node of action.nodes) {
                    nodeIds.push(node.id)
                }
                redoAction = {
                    type: "REMOVE_NODES",
                    nodeIds
                }
            } break
            case "ADD_CONNECTION": {
                redoAction = {
                    ...action,
                    type: "REMOVE_CONNECTION",
                }
            } break
            case "REMOVE_CONNECTION": {
                redoAction = {
                    ...action,
                    type: "ADD_CONNECTION",
                }
            } break
        }
        this._addRedo({
            action,
            redoAction
        })
    }

    onNodeLockChange(nodeId, isLock) {
        if (isLock) {
            this._lockedNodes.add(nodeId)
        } else {
            this._lockedNodes.delete(nodeId)
        }
    }

    onContentChanged(
        sender: any,
        change: any) {
        // console.log("_onContentChanged")
        // console.log(sender, change)
    }

    renderNodeHeader(NodeHeader, currentNodeType, {
        openMenu: handleContextMenu,
        closeMenu: closeContextMenu,
        deleteNode
    }, id) {
        const Ret = () => {
            const [fontSize, setFontSize] = useState(headerFontsize);
            const instanceBackgroundColor = "#d9822b"
            const functionBackgroundColor = "#5F41FF"
            const defaultBackGroundColor = "rgba(248, 28, 149, 0.8)"
            let backgroundColor
            if (/instance@/g.exec(currentNodeType.type)) {
                backgroundColor = instanceBackgroundColor
            } else if (/function@/g.exec(currentNodeType.type)) {
                backgroundColor = functionBackgroundColor
            } else {
                backgroundColor = defaultBackGroundColor
            }
            let HeaderDeleteIcon = () => {
                return <DeleteIcon
                    onClick={e => {
                        e.preventDefault()
                        this.dispatchNodes({
                            type: "REMOVE_NODE",
                            nodeId: id
                        })
                    }}
                    width={fontSize}
                    height={fontSize} />
            }

            let HeaderRunIcon = () => {
                if (backgroundColor == instanceBackgroundColor)
                    return null
                return <RunIcon
                    onClick={e => {
                        e.preventDefault()
                        this.runNode(id, false)
                    }}
                    width={fontSize}
                    height={fontSize} />
            }


            let HeaderReRunIcon = () => {
                if (backgroundColor == instanceBackgroundColor)
                    return null
                return <ReRunIcon
                    onClick={e => {
                        e.preventDefault()
                        this.runNode(id, true)
                    }}
                    width={fontSize}
                    height={fontSize} />
            }

            let HeaderLockIcon = () => {
                if (backgroundColor == instanceBackgroundColor)
                    return null
                return <LockIcon
                    id={id}
                    width={fontSize}
                    height={fontSize}
                    initlock={this._lockedNodes.has(id)}
                    onChange={isLock => {
                        this.onNodeLockChange(id, isLock)
                        this.onNodesChange(this.editorNodes)
                    }}
                />
            }

            let HeaderExportIcon = () => {
                if (backgroundColor == instanceBackgroundColor)
                    return null
                return <ExportIcon
                    width={fontSize}
                    height={fontSize}
                    onClick={async e => {
                        let preCheckCache = this._runCheckCache
                        try {
                            this._exportRet = []
                            this._exportingCodeNodeId = id
                            this._runCheckCache = false
                            this._exportIndent = ""
                            await this.runNode(id)
                            this._codeEditorValueCache = this._getExportedCodeText()
                            this._outputText(this._codeEditorValueCache)
                            let nodeId = this._exportingCodeNodeId
                            this._saveCode = () => {
                                this._writeToExportCell(nodeId)
                            }
                            let preValue = this._readExportedData(nodeId) || ""
                            this._setUseDiffEditor(true)
                            this._setshowCodeEditor(true)
                            setTimeout(() => {
                                let firstLineEndIndex = preValue.indexOf("\n")
                                if (firstLineEndIndex >= 0) {
                                    preValue = preValue.slice(firstLineEndIndex + 1, preValue.length)
                                }
                                this._setDiffCodeEditorValue(preValue, this._codeEditorValueCache)
                            }, 0);
                        } finally {
                            this._exportingCodeNodeId = null
                            this._runCheckCache = preCheckCache
                        }
                    }}
                />
            }

            return <div style={{
                backgroundColor,
                display: "flex",
                alignItems: "center",
                color: "white",
            }}>
                <div style={{ fontSize }}>
                    <HeaderDeleteIcon />
                    <HeaderLockIcon />
                    <HeaderExportIcon />
                    <HeaderReRunIcon />
                    <HeaderRunIcon />
                </div>
                <span style={{ flex: 1, textAlign: "center", fontSize }}>
                    {currentNodeType.label}
                </span>
            </div>
        }

        let ret: any = this._headRenderCache[id]
        if (!ret) {
            ret = <Ret />
            this._headRenderCache[id] = ret
        }

        return ret
    }

    outOptions(options) {
        this.editorOptions = {
            ...this.editorOptions,
            ...options
        }
    }

    updateNodeConnections(nodeId) {
        let recalculateStageRect = this.editorOptions["recalculateStageRect"]
        if (recalculateStageRect)
            recalculateStageRect()
        const updateConnections = this.editorOptions[`updateNodeConnections_${nodeId}`]
        if (updateConnections)
            updateConnections()
    }

    setInputing(value) {
        if (this._containerRef.current) {
            const element = this._containerRef.current as unknown as HTMLDivElement
            element.setAttribute("data-inputing", `${value}`)
        }
    }

    cellInsert(index) {
        const model = this._context.model.sharedModel
        model.insertCell(index, { cell_type: 'code' })
    }

    cellRemove(index) {
        const model = this._context.model.sharedModel
        model.deleteCell(index)
    }

    cellUndo() {
        const model = this._context.model.sharedModel
        if (model.canUndo()) {
            model.undo()
        }
    }

    cellRedo() {
        const model = this._context.model.sharedModel
        if (model.canRedo()) {
            model.redo()
        }
    }

    cellGet(index) {
        return this._context.model.cells.get(index)
    }

    async onContextMenuFilter(
        filter: string,
        options: any[] = [],
        setOptions,
        filterOptions,
        from
    ) {
        switch (from) {
            case "stage": {
                await this._filterNodeTypes(filter, options, setOptions, filterOptions)
            } return
            case "codeEditor": {
                await this._filterCell(filter, options, setOptions, filterOptions)
            } return
        }
    }

    async onOptionSelected(option) {
        if (option.label.charAt(0) == ".") {
            this._loadNodes(option.data)
            return
        }

        let addNode = this.editorOptions["addNode"]
        if (addNode) {
            addNode(option)
        }
    }

    async onMenuStateChange(menuOpen, hideFilter, from) {
        this._stopCreateNodeType = !menuOpen
        this._stopFilterCell = !menuOpen
        if (menuOpen) {
            this._commonFilterKeys()
        } else {
            this.keyEventFilter.clear()
        }
    }

    async buildNodeTypesFromCompleteReply(
        reply: KernelMessage.ICompleteReplyMsg
            | undefined, filter: string,
        options: any[] | null = null,
        setOptions: any = null,
        filterOptions: any = null
    ) {
        let ret: any[] = []
        if (reply?.content.status != "ok") {
            return ret
        }

        let matches = reply.content.metadata._jupyter_types_experimental as []
        for (let index = 0; index < matches.length; index++) {
            if (!this._loadingNodes && this._stopCreateNodeType) {
                return ret
            }
            let node_types = await this.buildNodeTypeByCompleteMatch(matches[index], filter)
            for (const node_type of node_types) {
                ret.push(node_type)
                if (options && setOptions && filterOptions) {
                    let has_opt = false
                    for (const opt of options) {
                        if (opt.value == node_type.type) {
                            has_opt = true
                            break
                        }
                    }
                    if (!has_opt) {
                        options.push(generateMenuOption(node_type))
                    }
                    try {
                        if (this.editorConfig[node_type.type])
                            this.editorConfig.removeNodeType(node_type.type)
                        this.editorConfig.addNodeType(node_type)
                    } catch (error) { }
                    options = filterOptions(filter, options) as any[]
                    setOptions(options)
                }
            }
        }
        return ret
    }

    async buildNodeTypeByCompleteMatch(match, filter: string) {
        let node_types: any[] = []
        let node_type_name = ""
        let filters = filter.split(".")
        if (filters.length > 1) {
            filters.pop()
            for (const f of filters) {
                node_type_name = node_type_name + "." + f.trim()
            }
            node_type_name = node_type_name + "." + match.text.trim()
            node_type_name = node_type_name.slice(1, node_type_name.length)
        } else {
            node_type_name = match.text.trim()
        }
        switch (match.type) {
            case "instance": {
                let target_type = ""
                let target_value = "None"
                try {
                    // 1.获取instance的数据类型和值
                    await this._getInstanceInfo(node_type_name, (msg) => {
                        if (KernelMessage.isStreamMsg(msg)) {
                            let info = JSON.parse(msg.content.text as string)
                            let getTypeRet = /<class '(.*)'>/g.exec(info.type)
                            if (getTypeRet) {
                                target_type = getTypeRet[1]
                                if (info.value === null) {
                                    info.value = "None"
                                }
                                target_value = info.value
                            }
                        }
                    })

                    // 2.构建节点类型
                    node_types = this._buildInstanceNodeTypes(
                        node_type_name,
                        target_type,
                        target_value
                    )

                    // 3.记录下来
                    this._nodeTypes[node_type_name] = {
                        type: "instance",
                        node_type_name,
                        target_type,
                        target_value
                    }
                } catch (error) { }
            } break;
            case "function": {
                // 1.解析signature (a:int, b, c:str= "123", *args, **kwargs)
                let in_ports: any[] = this._buildInputPortsFromSignature(match.signature)
                // 2.构建nodeType
                node_types = this._buildFunctionNodeTypes(node_type_name, in_ports)
                // 3.记录下来
                this._nodeTypes[node_type_name] = {
                    type: "function",
                    node_type_name,
                    in_ports,
                }
            } break;
            case "module": { } break;
            case "class": { } break;
            case "keywork": { } break;
        }
        return node_types
    }

    private _buildInputPortsFromSignature(signature: String) {
        signature = signature.trim()
        signature = signature.slice(1, signature.length - 1)
        // 2.用 ", "分割
        let segs = signature.split(",")
        // 3.解析参数和默认值
        let in_ports: any[] = []
        for (let seg of segs) {
            seg = seg.trim()
            if (!seg) {
                continue
            }

            let arg_name: string = "/"
            let arg_type: string = "any"
            let arg_default: any = "None"
            if (seg.charAt(0) == "/") {
                in_ports.push({
                    arg_name,
                    arg_type,
                    arg_default
                })
                continue
            }
            let ret = /\*{2}\s*([_\w]+)/g.exec(seg)
            if (ret) {
                try { arg_name = "**" + ret[1].trim() + "(dict)" } catch (error) { }
                arg_type = "dict"
            } else {
                ret = /\*\s*([_\w]+)/g.exec(seg)
                if (ret) {
                    try { arg_name = "*" + ret[1].trim() + "(tuple)" } catch (error) { }
                    arg_type = "tuple"
                } else {
                    ret = /([_\w]+)\s*(:\s*([_\w]+)){0,1}\s*(=(.*)){0,1}/g.exec(seg)
                    if (ret) {
                        try { arg_name = ret[1].trim() } catch (error) { }
                        try { arg_type = ret[3].trim() } catch (error) { }
                        try {
                            let dvalue = ret[5].trim()
                            // 判断是什么类型
                            // 字符串
                            if ((dvalue.charAt(0) == "\"" && dvalue.charAt(dvalue.length - 1) == "\"")
                                || (dvalue.charAt(0) == "\'" && dvalue.charAt(dvalue.length - 1) == "\'")) {
                                arg_type = "str"
                                arg_default = eval(dvalue)
                            } else {
                                let ret = /[\d\.]+/g.exec(dvalue)
                                if (ret) {
                                    arg_type = "int"
                                    arg_default = Number(dvalue)
                                } else {
                                    arg_default = dvalue
                                }
                            }
                        } catch (error) { }
                    }
                }
            }

            if (arg_name.length > 0) {
                in_ports.push({
                    arg_name,
                    arg_type,
                    arg_default
                })
            }
        }

        return in_ports
    }

    private _buildFunctionNodeTypes(node_type_name, in_ports) {
        let type_name = "function@" + node_type_name
        let node_types: any[] = []
        let nodetype = {
            type: type_name,
            label: node_type_name,
            description: node_type_name,
            initialWidth: buildNodeWidth(node_type_name, headerFontsize, nodeMinWidth, nodeMaxWidth),
            inputs: ports => (inputData, connections, executionContext: NodeEditorWidget, nodeId) => {
                let ret: any[] = [
                    get_port_func("control")(ports),
                ]
                for (const in_port of in_ports) {
                    if (in_port.arg_name == "/") {
                        continue
                    }
                    let f = get_port_func(in_port.arg_type)
                    let port = f(
                        ports,
                        in_port.arg_name,
                        in_port.arg_name,
                        in_port.arg_default
                    )
                    ret.push(port)
                }
                return ret
            },
            outputs: common_out
        }
        node_types.push(nodetype)
        return node_types
    }

    private _buildInstanceNodeTypes(node_type_name, target_type, target_value): any[] {
        let node_types: any[] = []
        if (target_type == "") {
            return node_types
        }
        let port_func: any = null
        let type_name = "instance@set@" + node_type_name
        let label = node_type_name + "@set"
        port_func = get_port_func(target_type)
        let nodetype = {
            type: type_name,
            label,
            description: node_type_name + "@" + target_type,
            initialWidth: buildNodeWidth(label, headerFontsize, nodeMinWidth, nodeMaxWidth),
            inputs: ports => (inputData, connections, executionContext: NodeEditorWidget, nodeId) => {
                let port = port_func(ports, node_type_name, node_type_name, target_value)
                return [get_port_func("control")(ports), port]
            },
            outputs: ports => (inputData, connections, executionContext: NodeEditorWidget, nodeId) => {
                let port = port_func(ports, node_type_name, node_type_name, target_value)
                return [get_port_func("control")(ports), port]
            }
        }
        node_types.push(nodetype)
        type_name = "instance@get@" + node_type_name
        label = node_type_name + "@get"
        nodetype = {
            type: "instance@get@" + node_type_name,
            label,
            description: node_type_name + "@" + target_type,
            initialWidth: buildNodeWidth(label, headerFontsize, nodeMinWidth, nodeMaxWidth),
            inputs: ports => (inputData, connections, executionContext: NodeEditorWidget, nodeId) => {
                return []
            },
            outputs: ports => (inputData, connections, executionContext: NodeEditorWidget, nodeId) => {
                let port = port_func(ports, node_type_name, node_type_name, target_value)
                return [port]
            }
        }
        node_types.push(nodetype)
        return node_types
    }

    private async _getInputValue(input, node) {
        // 分两种情况
        let connection = node.connections.inputs[input.name]
        // 1.没有对应的连接，需要解析control的值
        if (!connection) {
            return await this._getPortValue(
                input.type, node.inputData[input.name] || {}, input.name)
        }
        // 2.有连接，需要递归解析连接的节点
        else {
            // 1.获取该连接的信息
            let { nodeId, portName } = connection[0]
            // 2.运行该节点，变量值
            this._setRunningNode(nodeId)
            this.refreshNodeBoxShadow()
            let target_node_ret = await this._runNode(nodeId)
            this._setRunningNode(node.id)
            this.refreshNodeBoxShadow()
            if (!target_node_ret) {
                return
            }
            // 3.根据返回的值，提取结果
            this._runCache[nodeId] = target_node_ret
            return target_node_ret[portName]
        }
    }

    private async _getPythonValueIsTrue(value) {
        await this._runCode(`______jupyterlab_get_boolean_value__(${value})`, (msg) => {
            if (KernelMessage.isExecuteResultMsg(msg)) {
                let data = msg.content.data as any
                data = data["text/plain"].trim()
                value = data == "True"
            }
        })
        return value
    }

    private async _getNodeInputs(node) {
        let inputs = this.editorConfig.nodeTypes[node.type].inputs;
        if (typeof inputs === 'function') {
            inputs = inputs(node.inputData, node.connections, this, node.id);
        }
        return inputs
    }

    private async _getNodeInputValue(node, inputs, input_name) {
        for (const input of inputs) {
            if (input.name == input_name)
                return await this._getInputValue(input, node)
        }
    }

    private async _runNode(id) {
        if (this._interruptingKernel) {
            this._setRunningNode(id, true)
            this.refreshNodeBoxShadow()
            const errorMsg = "内核中断"
            this._outputText(errorMsg)
            throw errorMsg
        }

        // 1.获取该节点
        let node = this.editorNodes[id]
        if (!node) {
            console.error("节点不存在")
            return
        }

        if (this._runCheckCache) {
            let ret = this._runCache[id]
            if (ret) {
                return ret
            }
        }

        // 2.获取所有的输入端口
        let inputs = await this._getNodeInputs(node)

        // 3.判断是否是分支节点
        let inputValues = {}
        if (node.type == "if") {
            // 1.解析value的真值
            let condition_ret = await this._getNodeInputValue(node, inputs, "value")
            if (this._exportingCodeNodeId) {
                let out_var_name = this._get_out_var_name(id)
                this._exportCode(`if ${condition_ret}:`)
                this._exportAddIndent()
                let ret = await this._getNodeInputValue(node, inputs, "true")
                this._exportCode(`${out_var_name}=${ret}`)
                this._exportRemoveIndent()
                this._exportCode(`else:`)
                this._exportAddIndent()
                ret = await this._getNodeInputValue(node, inputs, "false")
                this._exportCode(`${out_var_name}=${ret}`)
                this._exportRemoveIndent()
                return {
                    out: out_var_name
                }
            }
            else {
                // 2.执行python代码，查看该值是true还是false
                condition_ret = await this._getPythonValueIsTrue(condition_ret)
                // 3.根据解析的value值执行true或者false的分支
                inputValues["out"] = await this._getNodeInputValue(node, inputs,
                    condition_ret ? "true" : "false")
            }

        }
        else if (node.type == "loop") {
            if (this._exportingCodeNodeId) {
                await this._getNodeInputValue(node, inputs, "control")
                this._exportCode("while True:")
                this._exportAddIndent()
                let ret = await this._getNodeInputValue(node, inputs, "value")
                this._exportCode(`if not ${ret}:`)
                this._exportAddIndent()
                this._exportCode(`break`)
                this._exportRemoveIndent()
                await this._getNodeInputValue(node, inputs, "loop")
                this._exportRemoveIndent()
                return {
                    out: "None"
                }
            } else {
                // 1.先执行准备数据的run接口
                await this._getNodeInputValue(node, inputs, "control")
                let condition_ret
                while (true) {
                    // 2.清除循环节点前面连接节点的运行缓存
                    let exceptNames = new Set(["control"])
                    let linkedNodeIds = await this._getNodeInputLinkedNodes(node.id, exceptNames)
                    for (const linkedNodeId of linkedNodeIds) {
                        delete this._runCache[linkedNodeId]
                    }
                    // 3.解析value的真值    
                    condition_ret = await this._getNodeInputValue(node, inputs, "value")
                    // 4.执行python代码，查看该值是true还是false
                    condition_ret = await this._getPythonValueIsTrue(condition_ret)
                    // 5.判断condition,是否执行循环体
                    if (!condition_ret) break
                    // 6.执行循环体
                    await this._getNodeInputValue(node, inputs, "loop")
                }
            }
        }
        else {
            // 1.遍历每个端口，解析它
            for (const input of inputs) {
                inputValues[input.name] = await this._getInputValue(input, node)
            }
        }

        // 4.运行该节点
        // 1.检测节点是变量还是函数
        let match_ret = /(.*?)@(.*)/g.exec(node.type)
        if (match_ret) {
            switch (match_ret[1]) {
                // 1.节点是变量
                case "instance":
                    // 获取变量所执行的方法，get 或者 set
                    match_ret = /(get|set)@(.*)/g.exec(match_ret[2])
                    if (!match_ret) {
                        console.error("instance没有get或set")
                        return
                    }
                    switch (match_ret[1]) {
                        // 1.如果是set,需要执行set的python代码
                        case "set":
                            // 1.根据输入的值，执行代码
                            for (const varName in inputValues) {
                                if (varName == "control") {
                                    continue
                                }
                                let code = `${varName} = ${inputValues[varName]}`
                                if (this._exportingCodeNodeId) {
                                    this._exportCode(code)
                                } else {
                                    await this._runCode(code)
                                }
                            }
                        // 2.如果是get，直接返回该变量的名称
                        case "get":
                            return { [match_ret[2]]: match_ret[2] }
                    }
                    return inputValues
                // 2.节点是函数
                case "function":
                    let no_keyword_arguments = false
                    let type_cache = this._nodeTypes[match_ret[2]]
                    if (type_cache) {
                        for (const port of type_cache.in_ports) {
                            no_keyword_arguments = port.arg_name == "/"
                        }
                    }
                    // 1.构建参数字符串
                    let args_string = ""
                    for (const input of inputs) {
                        let name = input.name as string
                        let first_xing = name.charAt(0) == "*"
                        let second_xing = name.charAt(1) == "*"
                        // 1.检测是否是**开头
                        if (first_xing && second_xing) {
                            args_string += `, **${inputValues[name]}`
                        }
                        // 2.检测是否是*开头
                        else if (first_xing) {
                            args_string += `, *${inputValues[name]}`
                        }
                        // 3.正常的参数
                        else if (input.type != "control") {
                            if (!no_keyword_arguments) {
                                args_string += `, ${name}=${inputValues[name]}`
                            }
                            else {
                                args_string += `, ${inputValues[name]}`
                            }
                        }
                    }
                    // 2.去除开头的,
                    args_string = args_string.slice(1, args_string.length)
                    // 3.构建代码
                    let out_var_name = this._get_out_var_name(id)
                    let code = `${out_var_name} = ${match_ret[2]}(${args_string})`
                    // 4.运行代码
                    if (this._exportingCodeNodeId) {
                        this._exportCode(code)
                    } else {
                        await this._runCode(code)
                    }
                    return {
                        out: out_var_name
                    }
                default: break
            }
        } else {
            switch (node.type) {
                case "video":
                case "image": {
                    let out_var_name = this._get_out_var_name(id)

                    if (this._exportingCodeNodeId) {
                        this._exportRet.push(`${out_var_name}=${inputValues["urls"]}`)
                    } else {
                        let code = `
                        ${out_var_name}=${inputValues["urls"]}
                        ______jupyterlab_node_editor_get_urls_(${out_var_name})
                        `
                        await this._runCode(code, (msg) => {
                            if (KernelMessage.isExecuteResultMsg(msg)) {
                                let data = msg.content.data as any
                                data = eval(data["text/plain"])
                                let urls = JSON.parse(data)
                                setImageUrls(id, urls)
                            }
                        })
                    }

                    let ret = { urls: out_var_name }
                    return ret
                }
                case "tuple": {
                    let out_var_name = this._get_out_var_name(id)
                    let code = ""
                    let maxV = get_tuple_max_index(inputValues)
                    for (let index = 0; index <= maxV; index++) {
                        code += `${inputValues[tuple_value_name(index)]},`
                    }
                    code = `${out_var_name} = (${code})`

                    if (this._exportingCodeNodeId) {
                        this._exportCode(code)
                    } else {
                        await this._runCode(code)
                    }

                    return {
                        out: out_var_name
                    }
                }
                case "dict": {
                    let out_var_name = this._get_out_var_name(id)
                    let code = ""
                    for (const key in inputValues) {
                        let ret = parse_dict_name(key)
                        if (ret) {
                            code += `'${ret[1]}':${inputValues[key]},`
                        }
                    }
                    code = `${out_var_name} = {${code}}`

                    if (this._exportingCodeNodeId) {
                        this._exportCode(code)
                    } else {
                        await this._runCode(code)
                    }

                    return {
                        out: out_var_name
                    }
                }
                case "bool":
                case "string":
                case "any": {
                    let out_var_name = this._get_out_var_name(id)
                    let code = `${out_var_name} = ${inputValues["value"]}`
                    if (this._exportingCodeNodeId) {
                        this._exportCode(code)
                    } else {
                        await this._runCode(code)
                    }
                    return {
                        out: out_var_name
                    }
                }
                case "int": {
                    let out_var_name = this._get_out_var_name(id)
                    let code = `${out_var_name} = int(${inputValues["value"]})`
                    if (this._exportingCodeNodeId) {
                        this._exportCode(code)
                    } else {
                        await this._runCode(code)
                    }
                    return {
                        out: out_var_name
                    }
                }
                case "float": {
                    let out_var_name = this._get_out_var_name(id)
                    let code = `${out_var_name} = float(${inputValues["value"]})`
                    if (this._exportingCodeNodeId) {
                        this._exportCode(code)
                    } else {
                        await this._runCode(code)
                    }
                    return {
                        out: out_var_name
                    }
                }
                case "if": {
                    let out_var_name = this._get_out_var_name(id)
                    let code = `${out_var_name} = ${inputValues["out"]}`
                    await this._runCode(code)
                    return {
                        out: out_var_name
                    }
                }
                case "loop": {
                    return {
                        out: "None"
                    }
                }
                case "operator": {
                    let out_var_name = this._get_out_var_name(id)
                    let yiyuan_operator = ["not", "~"]
                    let operator = inputValues["operator"]["operator"]
                    let code
                    if (!yiyuan_operator.includes(operator)) {
                        code = `${out_var_name} = ${inputValues["value1"]} ${operator} ${inputValues["value2"]}`
                    } else {
                        code = `${out_var_name} = ${operator} ${inputValues["value1"]}`
                    }
                    if (this._exportingCodeNodeId) {
                        this._exportCode(code)
                    } else {
                        await this._runCode(code)
                    }
                    return {
                        out: out_var_name
                    }
                }
            }
        }
    }

    private async _runCell(
        cell: CodeCellModel,
        translator: ITranslator | null) {
        translator = translator || nullTranslator;
        const trans = translator.load('jupyterlab');
        if (!await this._checkSessionAndKernel(translator)) {
            return false
        }

        let sessionContext = this._context.sessionContext
        const model = cell;
        const code = model.sharedModel.getSource();
        if (!code.trim() || !(sessionContext.session && sessionContext.session.kernel)) {
            model.clearExecution();
            return false;
        }
        const cellId = { cellId: model.id };
        const deletedCells = this._context.model.deletedCells || []
        let metadata = {
            deletedCells,
            recordTiming: true
        }
        metadata = Object.assign(Object.assign(Object.assign({}, model.metadata), metadata), cellId);
        model.clearExecution();
        model.trusted = true;

        let stopOnError = true;
        const content = {
            code,
            stop_on_error: stopOnError
        };
        let ret = sessionContext.session.kernel.requestExecute(content, false, metadata)
        // 注册结果获取函数
        ret.onIOPub = (msg) => {
            this._onKernelMsg(msg)
            if (KernelMessage.isStreamMsg(msg)) {
                let m = msg.content as IOutput
                m.output_type = msg.header.msg_type
                model.outputs.add(m)
            } else if (KernelMessage.isExecuteResultMsg(msg)) {
                let m = msg.content as IOutput
                m.output_type = msg.header.msg_type
                model.outputs.add(m)
            }
        }

        let reply = await ret.done
        deletedCells.splice(0, deletedCells.length)
        if (!reply) {
            return true
        }

        if (reply.content.status === 'ok') {
            const content = reply.content;
            if (content.payload && content.payload.length) {
                console.log(content.payload)
            }
            return true;
        }

        throw new KernelError(reply.content);
    }

    private async _runCode(
        code: string,
        onIOPub: (msg: KernelMessage.IIOPubMessage<KernelMessage.IOPubMessageType>) => void
            | PromiseLike<void> = (msg) => { },
        translator: ITranslator | null = nullTranslator) {
        translator = translator || nullTranslator;
        const trans = translator.load('jupyterlab');
        if (!await this._checkSessionAndKernel(translator)) {
            return false
        }
        let sessionContext = this._context.sessionContext
        try {
            let stopOnError = true;
            const content = {
                code,
                stop_on_error: stopOnError
            };

            if (!code.trim() || !(sessionContext.session && sessionContext.session.kernel)) {
                return false;
            }

            // 注册结果获取函数s
            let ret = sessionContext.session.kernel.requestExecute(content, false, {})
            ret.onIOPub = (msg) => {
                this._onKernelMsg(msg)
                if (onIOPub != null) {
                    onIOPub(msg)
                }
            }
            let reply = await ret.done
            if (!reply) {
                return true
            }
            if (reply.content.status === 'ok') {
                const content = reply.content;
                if (content.payload && content.payload.length) {
                    console.log(content.payload)
                }
                return true;
            }
            else {
                // console.log("执行代码异常", reply)
                throw new KernelError(reply.content);
            }
        }
        catch (e) {
            throw e;
        }
    }

    private _loadNodesFromAllCell() {
        let ret: any[] = []
        for (let index = 0; index < this._context.model.cells.length; index++) {
            const cell = this.cellGet(index);
            if (cell.type == "code") {
                let data: any = this._get_node_data(cell as CodeCellModel)
                if (!data) {
                    continue
                }
                ret.push(data)
            }
        }
        return ret
    }

    private async _saveNodes(nodes: NodeMap) {
        if (!this._isSaveNodes) return
        if (this._curNodesId == "") {
            this._curNodesId = uuidv4()
        }
        let save_data = {
            id: this._curNodesId,
            name: this.curNodeName,
            nodes,
            nodeTypes: {},
            locked: [...this._lockedNodes],
            runCache: this._runCache
        }

        // 检查并保存所有用到的nodetypes
        for (const key in nodes) {
            let type_name = nodes[key].type
            // 1.判断是instance 还是 function
            let ret = /instance@(get|set)@(.*)/g.exec(type_name)
            if (ret) {
                save_data.nodeTypes[ret[2]] = this._nodeTypes[ret[2]]
            }
            else {
                ret = /function@(.*)/g.exec(type_name)
                if (ret) {
                    save_data.nodeTypes[ret[1]] = this._nodeTypes[ret[1]]
                }
            }
        }

        this.setEditorNodes(nodes)
        let nodes_string = JSON.stringify(save_data)
        let nodes_reg_exp = new RegExp(`#\\[nodes_${this._curNodesId}\\]`, "g")
        let data = `#[nodes_${this._curNodesId}][${this.curNodeName}]${nodes_string}`
        this._writeDataToCell(nodes_reg_exp, data)
    }

    private _get_node_data(cell: CodeCellModel) {
        let nodes_reg_exp = /#\[nodes_(.*?)\]\[(.*?)\]([\s\S]*)/g
        let ret = nodes_reg_exp.exec(cell.sharedModel.getSource())
        if (!ret) {
            return null
        }
        return {
            id: ret[1].trim(),
            name: ret[2].trim(),
            data: JSON.parse(ret[3])
        }
    }

    private async _loadNodes(data) {
        if (this._curNodesId == data.id) {
            return
        }
        this._loadingNodes = true
        this._isSaveNodes = false
        try {
            // 1.读取保存的nodetypes
            this._nodeTypes = {
                ...this._nodeTypes,
                ...data.nodeTypes
            }
            for (const name in data.nodeTypes) {
                let type_data = data.nodeTypes[name]
                let node_types: any[] = []
                if (type_data.type == "instance") {
                    node_types = this._buildInstanceNodeTypes(
                        type_data.node_type_name,
                        type_data.target_type,
                        type_data.target_value)
                }
                else if (type_data.type == "function") {
                    node_types = this._buildFunctionNodeTypes(
                        type_data.node_type_name,
                        type_data.in_ports)
                }

                for (const node_type of node_types) {
                    try {
                        if (this.editorConfig[node_type.type])
                            this.editorConfig.removeNodeType(node_type.type)
                        this.editorConfig.addNodeType(node_type)
                    } catch (error) { }
                }
            }

            // 2.根据保存的nodes构建nodetypes
            for (const node_id in data.nodes) {
                const node = data.nodes[node_id];
                if (this.editorConfig.nodeTypes[node.type]) {
                    continue
                }
                let got_node_type = false
                let ret = /(.*)?@(.*)/g.exec(node.type)
                if (ret) {
                    let reply = await this._requestCompleter(ret[2], ret[2].length)
                    if (reply) {
                        let node_types = await this.buildNodeTypesFromCompleteReply(reply, ret[2])
                        for (const node_type of node_types) {
                            try {
                                this.editorConfig.addNodeType(node_type)
                            } catch (error) { }
                            if (node_type.type == node.type) {
                                got_node_type = true
                            }
                        }
                    }
                }

                if (!got_node_type) {
                    return false
                }
            }

            // 3.锁定的节点
            if (data.locked) {
                this._lockedNodes = new Set([...data.locked])
            }

            // 4.运行缓存
            await this._readRunCache(data)

            this.setEditorConfig(this.editorConfig)
            // 清除当前数据
            this._clearNodes()
            // 加载node数据
            this.dispatchNodes({ type: "RE_INIT", nodes: data.nodes })
            this.setEditorNodes(data.nodes)
            this.setCurNodeName(data.name)
            this._curNodesId = data.id
            this._isSaveNodes = true
            // 清除redolist
            this._clearRedoList()

            setTimeout(() => {
                this._focusToAllNodes()
            })
            return true
        } catch (error) {
        } finally {
            this._loadingNodes = false
        }
        return false
    }

    private async _checkSessionAndKernel(translator: ITranslator | null) {
        translator = translator || nullTranslator;
        const trans = translator.load('jupyterlab');
        let sessionContext = this._context.sessionContext
        // 检查是否正在打断执行
        if (sessionContext) {
            if (sessionContext.isTerminating) {
                let session_path = sessionContext.session?.path || ""
                showDialog({
                    title: trans.__('Kernel正在终止执行'),
                    body: trans.__(`${session_path}的Kernel正在终止执行,现在不能执行代码。`),
                    buttons: [Dialog.okButton({ label: trans.__('Ok') })]
                });
                return false;
            }
        }
        if (sessionContext.pendingInput) {
            void showDialog({
                title: trans.__('Cell not executed due to pending input'),
                body: trans.__('The cell has not been executed to avoid kernel deadlock as there is another pending input! Submit your pending input and try again.'),
                buttons: [Dialog.okButton({ label: trans.__('Ok') })]
            });
            return false;
        }

        if (sessionContext.hasNoKernel) {
            await this._selectKernel()
            if (sessionContext.hasNoKernel) {
                return false;
            }
        }

        if (!(sessionContext.session && sessionContext.session.kernel)) {
            void showDialog({
                title: trans.__('会话不可用'),
                body: trans.__('会话不可用'),
                buttons: [Dialog.okButton({ label: trans.__('Ok') })]
            });
            return false;
        }

        return true
    }

    private async _requestCompleter(code: string, cursor_pos: number) {
        this._showMsgToNotebook = false
        return await this._context.sessionContext.session?.kernel?.requestComplete({
            code,
            cursor_pos
        })
    }

    private async _inspectRequest(code: string, cursor_pos: number) {
        return await this._context.sessionContext.session?.kernel?.requestInspect({
            code,
            cursor_pos,
            detail_level: 0
        })
    }

    private _checkReady(isShowDialog: boolean = true) {
        if (!this._isReady) {
            if (isShowDialog) {
                showDialog({
                    title: "加载失败，重新运行笔记本",
                    body: "加载失败，重新运行笔记本",
                    buttons: [Dialog.okButton({ label: 'Ok' })]
                });
            }
            return false
        }
        return true
    }

    private async _initPython() {
        let code = `
import json
def ______jupyterlab_node_editor_get_instance_info(v):
    t = type(v)
    d = None
    if isinstance(v,int) or isinstance(v,float) or isinstance(v,str) or isinstance(v, bool):
        d = v
    return json.dumps({"type":str(t), "value":d})

def ______jupyterlab_node_editor_get_urls_(urls):
    if isinstance(urls, str):
        try:
            ret = json.loads(urls)
            if not isinstance(ret, list):
                raise TypeError('Expecting a list') 
            return json.dumps(ret)
        except ValueError as e:
            return json.dumps([urls])
        except TypeError as e:
            raise TypeError('Invalid input type')
    elif isinstance(urls, list):
        return json.dumps(urls)
    elif isinstance(urls, dict):
        return json.dumps(list(urls.values()))
    else:
        raise TypeError('Invalid input type')

def ______jupyterlab_get_boolean_value__(v):           
    if v:
        return True
    else:
        return False

def ______jupyterlab_node_editor_hasVars(vars):
    vars = json.loads(vars)
    print(vars)
    ret = {}
    for v in vars:
        ret[v] = v in globals()
    return json.dumps(ret)
`
        return await this._runCode(code)
    }

    private async _getInstanceInfo(
        instanceName,
        onIOPub: (
            msg: KernelMessage.IIOPubMessage<KernelMessage.IOPubMessageType>) => void
            | PromiseLike<void>) {
        let code = `print(______jupyterlab_node_editor_get_instance_info(${instanceName}))`
        return await this._runCode(code, onIOPub)
    }

    private async _getPortValue(portType: String, data: Object, name) {
        switch (portType) {
            case "any":
                for (const key in data) {
                    return data[key]
                }
                return "None"
            case 'string':
                for (const key in data) {
                    return `'${data[key]}'`
                }
                return `''`
            case 'jsstring':
                for (const key in data) {
                    return data[key]
                }
                return ""
            case 'boolean':
                for (const key in data) {
                    if (data[key]) {
                        return "True"
                    } else {
                        return "False"
                    }
                }
                return "False"
            case 'number':
                for (const key in data) {
                    return `${data[key]}`
                }
                return '0'
            case "image":
                return data["image"]
            case "tuple":
                return "()"
            case "dict":
                return "{}"
            case "control":
                return ""
            default:
                return data
        }
    }


    private _getCellIndex(reg: RegExp) {
        for (let index = 0; index < this._context.model.cells.length; index++) {
            const cell = this.cellGet(index);
            if (cell.type == "code") {
                if (reg.exec(cell.sharedModel.getSource()))
                    return index
                reg.lastIndex = 0
            }
        }
        return null
    }

    private _getNodesCellIndex(id) {
        let nodes_reg_exp = new RegExp(`nodes_${id}`, 'g');
        return this._getCellIndex(nodes_reg_exp)
    }

    private _clearNodes() {
        this.dispatchNodes({ type: "CLEAR", nodes: this.editorNodes })
        let refreshCache = this.editorOptions["refreshCache"]
        if (refreshCache) refreshCache()
    }

    private _outputText(text) {
        this._outputArea.model.add({
            output_type: "stream",
            name: "stdout",
            text
        })
    }

    private _onKernelMsg(msg) {
        let outputMsg: any = null
        if (KernelMessage.isExecuteInputMsg(msg)) {
            console.log(msg.content.code)
        }
        else if (KernelMessage.isStreamMsg(msg)) {
            console.log(msg.content.text)
            outputMsg = {
                output_type: "stream",
                ...msg.content
            }
        }
        else if (KernelMessage.isErrorMsg(msg)) {
            console.error(msg.content.ename)
            console.error(msg.content.evalue)
            let errMsg = ""
            for (const traceback of msg.content.traceback) {
                errMsg += traceback + "\n"
            }
            console.error(errMsg)
            this._setRunningNode(this._runningNodeId, true)
            this.refreshNodeBoxShadow()
            outputMsg = {
                output_type: "error",
                ...msg.content
            }
        }
        else if (KernelMessage.isExecuteResultMsg(msg)) {
            console.log(msg.content.data)
            outputMsg = {
                output_type: "execute_result",
                ...msg.content
            }
        }
        else if (KernelMessage.isStatusMsg(msg)) {
            let state = kernelStateMap[msg.content.execution_state]
            if (state) {
                this._setKernelState(state)
            }
        }

        if (outputMsg) {
            let curCellModel = this._getCurNodeCellModel()
            if (this._showMsgToNotebook
                && curCellModel
                && !KernelMessage.isExecuteInputMsg(msg)) {
                curCellModel.outputs.add(outputMsg)
            }

            if (this._outputArea) {
                this._outputArea.model.add(outputMsg)
            }
        }
    }

    private _get_out_var_name(nodeId) {
        let out_var_name = `_${nodeId}_out`
        return out_var_name.replace(/-/g, "")
    }

    private _addRedo(action) {
        // 1.将this._redoListIndex以后的全部删除
        this._redoList.splice(this._redoListIndex, this._redoList.length - this._redoListIndex)
        this._redoList.push(action)
        // 2.检测redolist是否超长
        if (this._redoList.length > this._redoListMaxLength) {
            // 1.移除前面的数据
            this._redoList.splice(0, this._redoList.length - this._redoListMaxLength)
        }
        // 3.重新设定index
        this._redoListIndex = this._redoList.length
    }

    private _setMenuOpen(filter) {
        let setMenuCoordinates = this.editorOptions["setMenuCoordinates"]
        let setMenuOpen = this.editorOptions["setMenuOpen"]
        let pos = { x: this._mouseMove.clientX, y: this._mouseMove.clientY }
        setTimeout(() => {
            setMenuCoordinates(pos);
            setMenuOpen(true);
            setTimeout(() => {
                let inputElement = document.querySelector('[data-flume-component="ctx-menu-input"]') as HTMLInputElement
                inputElement.value = filter
                inputElement.selectionEnd = inputElement.value.length;
                setTimeout(() => {
                    let setFilter = this.editorOptions["setFilter"]
                    setFilter(inputElement.value)
                }, 100);
            })
        })
    }

    private _startDrag() {
        if (!this._dragging) {
            let draggableRef = this.editorOptions["draggableRef"]
            if (this._isDraggableFocus()) {
                this._dragging = true
                draggableRef.current.style.cursor = "grab"
            }
        }
    }

    private _drag(e: MouseEvent) {
        if (!this._dragging) {
            return
        }

        const draggableRef = this.editorOptions["draggableRef"]
        if (!draggableRef.current) {
            return
        }

        const translateWrapper = this.editorOptions["translateWrapper"]
        if (!translateWrapper.current) {
            return
        }

        if (this._dragStartPos == null) {
            this._dragStartPos = e
            return
        }

        const translate = this.editorOptions["stagetTranslate"]
        this._dragXDistance = this._dragStartPos.clientX - e.clientX;
        this._dragYDistance = this._dragStartPos.clientY - e.clientY;
        translateWrapper.current.style.transform =
            `translate(${-translate.x - this._dragXDistance}px, ${-translate.y - this._dragYDistance}px)`;
    }

    private _stopDrag() {
        let draggableRef = this.editorOptions["draggableRef"]
        draggableRef.current.style.cursor = ""
        const translate = this.editorOptions["stagetTranslate"]
        const dispatchStageState = this.editorOptions["dispatchStageState"]
        dispatchStageState({
            type: "SET_TRANSLATE",
            translate: {
                x: translate.x + this._dragXDistance,
                y: translate.y + this._dragYDistance
            }
        });
        this._dragging = false
        this._dragStartPos = null
        this._dragXDistance = 0
        this._dragYDistance = 0
    }

    private _startScale() {
        if (!this._scaling) {
            let draggableRef = this.editorOptions["draggableRef"]
            if (this._isDraggableFocus()) {
                this._scaling = true
                draggableRef.current.style.cursor = "grab"
            }
        }
    }

    private _scale(e: MouseEvent) {
        // 判断是否正在进行缩放操作
        if (!this._scaling) {
            return
        }

        // 获取真个Draggable组件
        const draggableRef = this.editorOptions["draggableRef"]
        if (!draggableRef.current) {
            return
        }

        // 获取用于控制缩放的组件
        const scaleWrapper = this.editorOptions["scaleWrapper"]
        if (!scaleWrapper.current) {
            return
        }

        // 获取用于位移的组件
        const translateWrapper = this.editorOptions["translateWrapper"]
        if (!translateWrapper.current) {
            return
        }

        // 设置一个缩放起始
        if (this._scaleStartPos == null) {
            this._scaleStartPos = e
            return
        }

        // 获取当前的位移数据
        const wrapperRect = draggableRef.current.getBoundingClientRect();
        const currentTranslate = this.editorOptions["stagetTranslate"]

        // 计算新的缩放值
        const scale = this.editorOptions["stagetScale"]
        let dX = e.clientX - this._scaleStartPos.clientX;
        this._scaleDistance = dX
        let newScale = Math.max(scale + this._scaleDistance * this.scaleSpeed, 0.001)

        // 设定恢复缩放函数
        const byOldScale = (no) => no * (1 / scale);
        const byNewScale = (no) => no * (1 / newScale);

        // 获取【上上】层组件的中心点(上上层不会变)
        const parentCenterX = wrapperRect.x + wrapperRect.width / 2
        const parentCenterY = wrapperRect.y + wrapperRect.height / 2

        // 获取缩放前的this._scaleStartPos 相对于 上层组件的 坐标
        const xOld = byOldScale(this._scaleStartPos.clientX - parentCenterX + currentTranslate.x);
        const yOld = byOldScale(this._scaleStartPos.clientY - parentCenterY + currentTranslate.y);

        // 获取缩放后的this._scaleStartPos 相对于 上层组件的 坐标
        const xNew = byNewScale(this._scaleStartPos.clientX - parentCenterX + currentTranslate.x);
        const yNew = byNewScale(this._scaleStartPos.clientY - parentCenterY + currentTranslate.y);

        // 获取位移数据
        this._scaleXDistance = (xOld - xNew) * newScale;
        this._scaleYDistance = (yOld - yNew) * newScale;

        // 设定缩放
        scaleWrapper.current.style.transform = `scale(${newScale})`

        // 设定位移
        translateWrapper.current.style.transform =
            `translate(${-currentTranslate.x - this._scaleXDistance}px, ${-currentTranslate.y - this._scaleYDistance}px)`;
    }

    private _stopScale() {
        let draggableRef = this.editorOptions["draggableRef"]
        draggableRef.current.style.cursor = ""
        const scale = this.editorOptions["stagetScale"]
        const translate = this.editorOptions["stagetTranslate"]
        const dispatchStageState = this.editorOptions["dispatchStageState"]
        dispatchStageState({
            type: "SET_TRANSLATE_SCALE",
            scale: Math.max(scale + this._scaleDistance * this.scaleSpeed, 0.1),
            translate: {
                x: translate.x + this._scaleXDistance,
                y: translate.y + this._scaleYDistance
            }
        });
        this._scaling = false
        this._scaleDistance = 0
        this._scaleStartPos = null
        this._scaleXDistance = 0;
        this._scaleYDistance = 0;
    }

    private _resetView() {
        const dispatchStageState = this.editorOptions["dispatchStageState"]
        dispatchStageState({
            type: "SET_TRANSLATE_SCALE",
            scale: 1,
            translate: {
                x: 0,
                y: 0
            }
        });
    }

    private _focusToNodes(nodeIds) {
        // 计算最小的X，最大的X，最小的y，最大的y
        let minX = Number.MAX_SAFE_INTEGER
        let minY = Number.MAX_SAFE_INTEGER
        let maxX = Number.MIN_SAFE_INTEGER
        let maxY = Number.MIN_SAFE_INTEGER
        let node
        let element: HTMLDivElement
        for (const nodeId of nodeIds) {
            node = this.editorNodes[nodeId]
            if (minX >= node.x) {
                minX = node.x
            }
            if (minY >= node.y) {
                minY = node.y
            }

            element = this.editorOptions[`nodeDraggable_${nodeId}`].current as HTMLDivElement
            if (maxX <= node.x + element.clientWidth) {
                maxX = node.x + element.clientWidth
            }

            if (maxY <= node.y + element.clientHeight) {
                maxY = node.y + element.clientHeight
            }
        }

        // 计算节点的宽高
        const width = maxX - minX
        const height = maxY - minY

        // 计算中心点
        const centerX = width / 2 + minX
        const centerY = height / 2 + minY

        // 计算应该缩放的大小
        const container = this._editorContainerRef.current
        let rect = container.getBoundingClientRect()
        let scale = Math.min(rect.width / width, rect.height / height)
        scale = Math.min(1, scale)

        // 更新位移和缩放
        const dispatchStageState = this.editorOptions["dispatchStageState"]
        dispatchStageState({
            type: "SET_TRANSLATE_SCALE",
            scale: scale,
            translate: {
                x: centerX * scale,
                y: centerY * scale,
            }
        });
    }

    private _focusToAllNodes() {
        const nodeIds: any[] = []
        for (const nodeId in this.editorNodes) {
            nodeIds.push(nodeId)
        }
        if (nodeIds.length == 0) {
            return
        }
        this._focusToNodes(nodeIds)
    }

    private _focusToSelectedNodes() {
        if (this.selectedNodes.size == 0) {
            return
        }
        this._focusToNodes(this.selectedNodes)
    }

    private _isDraggableFocus() {
        let draggableRef = this.editorOptions["draggableRef"]
        return draggableRef.current == document.activeElement
            || this._containerRef.current == document.activeElement
            || this._containerRef.current.parentElement == document.activeElement

    }

    private _removeSelectedNodes() {
        if (this._isDraggableFocus() && this.selectedNodes.size > 0) {
            this.dispatchNodes({
                type: "REMOVE_NODES",
                nodeIds: this.selectedNodes
            })
        }
    }

    private _genNodeId() {
        const nanoid = this.editorOptions["nanoid"]
        if (nanoid) return nanoid(10)
    }

    private _copySelectedNodes() {
        if (!this._isDraggableFocus() || this.selectedNodes.size == 0) {
            return
        }

        const nodes = {}
        // 创建副本
        for (const id of this.selectedNodes) {
            const node = this.editorNodes[id]
            if (!node) continue
            const newNode = cloneDeep(node)
            newNode.newId = this._genNodeId()
            nodes[id] = newNode
        }

        // 重新构建连接
        const refreshConnection = (node, target) => {
            let puts = node.connections[target]
            for (const portName in puts) {
                let put = puts[portName][0]
                if (put) {
                    let targetNode = nodes[put.nodeId]
                    if (targetNode) {
                        put.nodeId = targetNode.newId
                    } else {
                        delete puts[portName]
                    }
                }
            }
        }


        let node
        this._copyedNodes = []
        for (const oldId in nodes) {
            node = nodes[oldId]
            // 替换连接中的ID为新的ID
            refreshConnection(node, "inputs")
            refreshConnection(node, "outputs")
            node.id = node.newId
            // delete node.newId
            this._copyedNodes.push(node)
        }
    }

    private _pasteSelectedNodes() {
        if (!this._copyedNodes || !this._mouseMove) {
            return
        }

        this.dispatchNodes({
            type: "ADD_NODES",
            nodes: this._copyedNodes
        })

        // 选择所有粘贴的节点
        setTimeout(() => {
            this.selectedNodes.clear()
            for (const node of this._copyedNodes) {
                this.selectedNodes.add(node.id)
            }
            this.refreshNodeBoxShadow()
        });
    }

    private _selectAllNodes() {
        for (const id in this.editorNodes) {
            this.selectedNodes.add(id)
        }
        this.refreshNodeBoxShadow()
    }

    private _getStageDraggableZuobiao(clientX, clientY) {
        const translateWrapper = this.editorOptions["translateWrapper"]
        const rect = translateWrapper.current.getBoundingClientRect()
        const scale = this.editorOptions["stagetScale"]
        return {
            x: (clientX - rect.x) / scale,
            y: (clientY - rect.y) / scale
        }
    }

    private _startDrawSelect() {
        this._showSelectRect = true
        if (this._selectRectRef == null) {
            const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            svg.setAttribute("class", SvgContainerStyle);
            svg.setAttribute("style", "z-index:100;");
            const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
            path.setAttribute("stroke", "rgb(185, 186, 189)");
            path.setAttribute("stroke-width", "3");
            path.setAttribute("stroke-linecap", "round");
            path.setAttribute("fill", "rgba(255,255,255,0.2)");
            path.setAttribute("d", "");
            svg.appendChild(path)
            this._selectRectRef = path
            const editorId = this.editorOptions["editorId"]
            let container = GetSvgContainerRef(editorId)
            container.appendChild(svg)
        }
    }

    private _calcSelctRect(e: MouseEvent) {
        if (!this._drawStartPos) {
            return {
                x: 0,
                y: 0,
                width: 0,
                height: 0
            }
        }

        const startPos = this._getStageDraggableZuobiao(this._drawStartPos.clientX, this._drawStartPos.clientY)
        const curPos = this._getStageDraggableZuobiao(e.clientX, e.clientY)

        // 计算长宽
        const width = curPos.x - startPos.x
        const height = curPos.y - startPos.y

        return {
            ...startPos,
            width,
            height
        }
    }

    private _setDrawRect(d) {
        const element = this._selectRectRef as SVGPathElement
        element.setAttribute("d", `M ${d.x} ${d.y} h ${d.width} v ${d.height} h ${-d.width} Z`)
    }

    private _drawSelect(e: MouseEvent) {
        if (!this._showSelectRect) {
            return
        }

        if (!this._drawStartPos) {
            this._drawStartPos = e
            return
        }

        const d = this._calcSelctRect(e)
        this._setDrawRect(d)
    }

    private _stopDrawSelect() {
        if (!this._showSelectRect) {
            return
        }

        function getDuiJiaoZuoBiao(rect) {
            let x1 = Math.min(rect.x, rect.x + rect.width);
            let y1 = Math.min(rect.y, rect.y + rect.height);
            let x2 = Math.max(rect.x, rect.x + rect.width);
            let y2 = Math.max(rect.y, rect.y + rect.height);
            return { x1, x2, y1, y2 }
        }

        function rectsIntersect(rect1, rect2) {
            let duijiao1 = getDuiJiaoZuoBiao(rect1)
            let duijiao2 = getDuiJiaoZuoBiao(rect2)
            return duijiao1.x1 < duijiao2.x2
                && duijiao1.x2 > duijiao2.x1
                && duijiao1.y1 < duijiao2.y2
                && duijiao1.y2 > duijiao2.y1
        }

        // 获取矩形数据
        const d = this._calcSelctRect(this._mouseMove)

        // 根据矩形数据，选择nodes
        this.selectedNodes.clear()
        for (const nodeId in this.editorNodes) {
            const node = this.editorNodes[nodeId]
            const element = document.getElementById(nodeId)
            if (element) {
                let rect = element.getBoundingClientRect()
                if (rectsIntersect(d, {
                    x: node.x,
                    y: node.y,
                    width: rect.width,
                    height: rect.height
                })) {
                    this.selectedNodes.add(nodeId)
                }
            }
        }

        // 刷新选择
        this.refreshNodeBoxShadow()


        // 清除矩形
        const element = this._selectRectRef as SVGPathElement
        element.setAttribute("d", ``)
        this._showSelectRect = false
        this._drawStartPos = null
    }

    private _refreshSelectedNodes() {
        // 刷新选择
        const remove_list: any[] = []
        for (const id of this.selectedNodes) {
            if (!this.editorNodes[id]) {
                remove_list.push(id)
            }
        }

        // 删除已经移除的节点
        for (const id of remove_list) {
            this.selectedNodes.delete(id)
        }

        // 刷新选择表现
        let element: HTMLElement | null
        for (const id in this.editorNodes) {
            if (!this.selectedNodes.has(id)) {
                continue
            }

            element = document.getElementById(id)
            if (!element) {
                continue
            }

            this._setNodeBoxShadow(id, nodeSelectedBoxShadow)
        }
    }

    private async _setNodePortControlInputValue(nodeId, portName, controlName, value) {
        // 获取NODE
        const node = this.editorNodes[nodeId]
        if (!node) {
            return
        }

        // 获取inputs数据
        let inputs = await this._getNodeInputs(node)
        let portType: any = null
        for (const input of inputs) {
            if (input.name != portName) {
                continue
            }

            portType = input.type
            break
        }

        switch (portType) {
            case "number": {
                const ret = document.evaluate(
                    `//input[@data-node-id="${nodeId}"][@data-port-name="${portName}"][@data-name="${controlName}"]`,
                    document,
                    null,
                    XPathResult.FIRST_ORDERED_NODE_TYPE,
                    null)
                let element = ret.singleNodeValue
                if (!element) {
                    return
                }
                (element as HTMLInputElement).value = value
            } break
            case "jsstring":
            case "string":
            case "any": {
                const ret = document.evaluate(
                    `//textarea[@data-node-id="${nodeId}"][@data-port-name="${portName}"][@data-name="${controlName}"]`,
                    document,
                    null,
                    XPathResult.FIRST_ORDERED_NODE_TYPE,
                    null)
                let element = ret.singleNodeValue
                if (!element) {
                    return
                }
                (element as HTMLTextAreaElement).innerText = value
            } break
            default: return
        }
    }

    private _updateHeaderCache() {
        const remove_list: any[] = []
        for (const nodeId in this._headRenderCache) {
            if (!this.editorNodes[nodeId]) {
                remove_list.push(nodeId)
            }
        }
        for (const nodeId of remove_list) {
            delete this._headRenderCache[nodeId]
        }
    }

    private _lockSelectedNodes() {
        if (this.selectedNodes.size == 0) {
            return
        }

        for (const nodeId of this.selectedNodes) {
            // 如果已经锁住了
            if (this._lockedNodes.has(nodeId)) {

            }
        }
    }

    private async _getNodeInputLinkedNodes(nodeId, exceptNames = new Set()) {
        let node = this.editorNodes[nodeId]
        if (!node) {
            return []
        }
        let ret: any[] = []
        let inputs = await this._getNodeInputs(node)
        for (const input of inputs) {
            if (exceptNames.has(input.name)) {
                continue
            }

            let connection = node.connections.inputs[input.name]
            if (!connection) {
                continue
            }
            let connectionData = connection[0]
            ret.push(connectionData.nodeId)
            let tmpret = await this._getNodeInputLinkedNodes(connectionData.nodeId)
            ret = [...ret, ...tmpret]
        }
        return ret
    }

    private _getCellModelByregExp(exp: RegExp) {
        let target_cell: null | CodeCellModel = null
        for (let index = 0; index < this._context.model.cells.length; index++) {
            const cell = this.cellGet(index);
            if (cell.type == "code") {
                let ret = exp.exec(cell.sharedModel.getSource())
                if (ret) {
                    target_cell = cell as CodeCellModel
                    break
                }
                exp.lastIndex = 0
            }
        }
        return target_cell
    }

    private _writeDataToCell(exp, data) {
        // 查找nodes保存的cell
        let target_cell = this._getCellModelByregExp(exp)

        // 如果没有找到，添加一个cell用于保存节点
        if (!target_cell) {
            this.cellInsert(0)
            target_cell = this.cellGet(0) as CodeCellModel
        }

        target_cell.sharedModel.setSource(data)
    }

    private _getCurNodeCellModel() {
        let nodes_reg_exp = new RegExp(`#\\[nodes_${this._curNodesId}\\]`, "g")
        return this._getCellModelByregExp(nodes_reg_exp)
    }

    private _clearCurOutput() {
        let model = this._getCurNodeCellModel()
        if (model) {
            model.outputs.clear()
        }
    }

    private _clearRunCache() {
        if (!this._isDraggableFocus()) {
            return
        }
        this._runCache = {}
        this._saveNodes(this.editorNodes)
    }

    private async _readRunCache(data) {
        this._runCache = data.runCache || {}

        let cache
        let args: any[] = []
        for (const nodeId in this._runCache) {
            cache = this._runCache[nodeId]
            for (const portName in cache) {
                args.push(cache[portName])
            }
        }

        let argsStr = JSON.stringify(args)
        let ret: any = null
        await this._runCode(`______jupyterlab_node_editor_hasVars('${argsStr}')`, msg => {
            if (KernelMessage.isExecuteResultMsg(msg)) {
                let retString = eval(msg.content.data["text/plain"] as string)
                ret = JSON.parse(retString)
            }
        })

        if (!ret) {
            return
        }

        const removeList: any[] = []
        let outName
        for (const nodeId in this._runCache) {
            cache = this._runCache[nodeId]
            for (const portName in cache) {
                outName = cache[portName]
                if (!ret[outName]) {
                    removeList.push(nodeId)
                }
            }
        }

        for (const nodeId of removeList) {
            delete this._runCache[nodeId]
        }
    }


    private _toggleOutputArea() {
        if (this._showOutputArea) {
            ReactWidget.detach(this._outputArea)
        }
        this._setShowOutputArea(!this._showOutputArea)

    }

    private _onOutputModelChanged() {
        if (!this._outputAreaContainerRef.current) {
            return
        }

        if (this._showOutputArea && this._outputAreaAutoScroll) {
            const element = this._outputAreaContainerRef.current as unknown as HTMLElement
            element.scrollTop = element.scrollHeight - element.clientHeight;
        }
    }

    private _setNodeBoxShadow(nodeId, boxShadow) {
        const element = document.getElementById(nodeId)
        if (!element) {
            return
        }
        element.style.boxShadow = boxShadow
    }

    private _refreshRunningNode() {
        let element: HTMLElement | null
        for (const id in this.editorNodes) {
            if (this._runningNodeId != id) {
                continue
            }
            element = document.getElementById(id)
            if (!element) {
                continue
            }

            this._setNodeBoxShadow(id,
                this._runningError ? nodeErrorBoxShadow : nodeRunningBoxShadow
            )
        }
    }

    private _setRunningNode(nodeId, error = false) {
        this._runningNodeId = nodeId
        this._runningError = error
    }

    private _exportCode(code) {
        this._exportRet.push(`${this._exportIndent}${code}`)
    }

    private _exportAddIndent(count = 1) {
        this._exportIndent
        for (let index = 0; index < count; index++) {
            this._exportIndent = `${this._exportIndent}    `
        }
    }

    private _exportRemoveIndent(count = 1) {
        this._exportIndent = this._exportIndent.slice(0, this._exportIndent.length - count * 4)
    }


    private _getExportedCodeText() {
        let text = ""
        for (const line of this._exportRet) {
            text = `${text}\n${line}`
        }
        return text
    }

    private _writeToExportCell(nodeId) {
        let reg = new RegExp(`#\\[export_${nodeId}\\]`, "g")
        if (this._codeEditorValueCache.length > 0) {
            this._writeDataToCell(reg, `#[export_${nodeId}]\n${this._codeEditorValueCache}`)
        }
        else {
            let index = this._getCellIndex(reg)
            if (index != null) {
                this.cellRemove(index)
            }
        }
    }


    private _readExportedData(nodeId) {
        let reg = new RegExp(`#\\[export_${nodeId}\\]`, "g")
        let cell = this._getCellModelByregExp(reg)
        if (!cell) {
            return null
        }
        return cell.sharedModel.getSource()
    }

    private _onCodeEditorChange(value: string | undefined, event: monaco.editor.IModelContentChangedEvent) {
        if (value == undefined) {
            return
        }
        this._codeEditorValueCache = value
        if (this._curEditingCellIndex >= 0) {
            let cell = this.cellGet(this._curEditingCellIndex)
            if (!cell) {
                this.cellInsert(this._curEditingCellIndex)
                cell = this.cellGet(this._curEditingCellIndex)
            }
            cell.sharedModel.setSource(value)
        }
    }

    private _openCellEditor() {
        this._setUseDiffEditor(false)
        this._setshowCodeEditor(true)
        setTimeout(() => {
            this._editCell(0)
        }, 0);
    }

    private _editCell(index) {
        this._curEditingCellIndex = index
        const cell = this.cellGet(index)
        let text = ""
        if (cell) {
            text = cell.sharedModel.getSource()
        }

        if (this._codeEditor) {
            this._codeEditor.setValue(text)
            this._codeEditor.pushUndoStop()
        }

        if (this._cellIndexInputRef.current) {
            const element = this._cellIndexInputRef.current as unknown as HTMLInputElement
            element.value = `${this._curEditingCellIndex}`
        }
    }

    private async _filterNodeTypes(filter: string,
        options: any[] = [],
        setOptions,
        filterOptions) {
        filter = filter.trim()
        if (!filter.trim()) return
        filter = filter.replace(/。/g, ".")
        if (filter.charAt(0) == ".") {
            let nodes = this._loadNodesFromAllCell()
            let options = filterOptions(filter, this._internal_options)
            for (const node of nodes) {
                options.push({
                    label: "." + node.name,
                    description: "加载节点" + node.name + node.id,
                    ...node
                })
            }
            setOptions(filterOptions(filter, options))
            return
        }

        this._stopCreateNodeType = true
        if (!this._checkReady(true)) {
            return
        }

        // 请求
        let reply = await this._requestCompleter(filter, filter.length)
        this._stopCreateNodeType = false
        // 构建options 和 nodeTypes
        await this.buildNodeTypesFromCompleteReply(
            reply, filter, options, setOptions, filterOptions)
    }

    private async _filterCell(filter: string,
        options: any[] = [],
        setOptions,
        filterOptions) {
        filter = filter.trim()
        if (!filter.trim()) return

        this._stopFilterCell = true
        // 等待一帧
        await nextFrame()
        this._stopFilterCell = false

        options = []
        const desc_len = 50
        let reg = new RegExp(filter, 'g')
        for (let index = 0; index < this._context.model.cells.length; index++) {
            if (this._stopFilterCell) {
                return
            }
            const cell = this.cellGet(index);
            const cellText = cell.sharedModel.getSource()
            if (cell.type != "code"
                || cellText.startsWith("#[nodes")
            ) {
                continue
            }

            const lines = cellText.split("\n")

            let rets = await findAll(cellText, reg, async () => {
                await nextFrame()
                return !this._stopFilterCell
            })

            for (const ret of rets) {
                let line = lines[ret[1] - 1]
                options.push({
                    label: `Cell_${index}`,
                    value: {
                        cellIndex: index,
                        startLine: ret[1],
                        startColumn: ret[2],
                        endLine: ret[3],
                        endColumn: ret[4]
                    },
                    description: line.slice(ret[2], line.length)
                })
            }
            setOptions([...options])
        }

    }

    private _onSelectedCodeEditorOption(option) {
        this._editCell(option.value.cellIndex)
        setTimeout(() => {
            if (this._codeEditor) {
                this._codeEditor.revealPositionInCenter({
                    lineNumber: option.value.startLine,
                    column: option.value.startColumn
                })
                this._codeEditor.setSelection({
                    startLineNumber: option.value.startLine,
                    startColumn: option.value.startColumn + 1,
                    endLineNumber: option.value.endLine,
                    endColumn: option.value.endColumn + 1,
                })
            }
        }, 0);
    }

    private async _codeEditorprovideCompletionItems(model: monaco.editor.ITextModel, position: monaco.Position) {
        // 获取光标的相对于文本开头的绝对位置
        var lines = model.getLinesContent();
        var total = 0;
        for (var i = 0; i < position.lineNumber - 1; i++) {
            total += lines[i].length + 1;
        }
        total += position.column - 1;
        // 请求completer
        const code = model.getValue()
        if (total > code.length) {
            total = code.length
        }

        let reply = await this._requestCompleter(code, total)

        // 获取位置
        var word = model.getWordUntilPosition(position);
        var range = {
            startLineNumber: position.lineNumber,
            endLineNumber: position.lineNumber,
            startColumn: word.startColumn,
            endColumn: word.endColumn,
        };

        // 构建返回值
        var suggestions: monaco.languages.CompletionItem[] = [];

        if (reply?.content.status == "ok") {
            let matches: any[] = reply.content.metadata._jupyter_types_experimental as []
            for (const match of matches) {
                let suggestion: any = null
                switch (match.type) {
                    case "instance": {
                        suggestion = {
                            label: match.text,
                            kind: monaco.languages.CompletionItemKind.Variable,
                            insertText: match.text,
                            range: range,
                        }
                    } break;
                    case "function": {
                        suggestion = {
                            label: match.text,
                            kind: monaco.languages.CompletionItemKind.Function,
                            insertText: match.text,
                            range: range,
                        }
                    } break;
                    case "module": {
                        suggestion = {
                            label: match.text,
                            kind: monaco.languages.CompletionItemKind.Module,
                            insertText: match.text,
                            range: range,
                        }
                    } break;
                    case "class": {
                        suggestion = {
                            label: match.text,
                            kind: monaco.languages.CompletionItemKind.Class,
                            insertText: match.text,
                            range: range,
                        }
                    } break;
                    case "keywork": {
                        suggestion = {
                            label: match.text,
                            kind: monaco.languages.CompletionItemKind.Keyword,
                            insertText: match.text,
                            range: range,
                        }
                    } break;
                }

                if (suggestion) {
                    suggestions.push(suggestion)
                }
            }
        }

        return { suggestions: suggestions };
    }

    private _setDiffCodeEditorValue(original, current) {
        if (!this._codeDiffEditor) {
            return
        }
        const originalModel = monaco.editor.createModel(
            original,
            "python"
        );
        const modifiedModel = monaco.editor.createModel(
            current,
            "python"
        );

        modifiedModel.onDidChangeContent(e => {
            this._onCodeEditorChange(modifiedModel.getValue(), e)
        })

        this._codeDiffEditor.setModel({
            original: originalModel,
            modified: modifiedModel,
        });
    }

    private _commonFilterKeys() {
        this.keyEventFilter.add(" ")
        this.keyEventFilter.add("s")
        this.keyEventFilter.add("a")
    }

    private _editorRun() {
        if (this._codeEditor) {
            let cell = this.cellGet(this._curEditingCellIndex)
            if (!cell) {
                return
            }
            this._runCell(cell as CodeCellModel, nullTranslator)
        }
        else if (this._codeDiffEditor) {
            const model = this._codeDiffEditor.getModel()
            if (model) {
                this._runCode(model.modified.getValue())
            }
        }
    }

    private _clearOutputArea() {
        if (this._outputArea) {
            this._outputArea.model.clear()
        }
    }

    private _interuptKernel() {
        this._context.sessionContext.session?.kernel?.interrupt()
        this._interruptingKernel = true
    }

    private async _selectKernel() {
        let dialog = new SessionContextDialogs()
        await dialog.selectKernel(this._context.sessionContext);
        if (!this._context.sessionContext.hasNoKernel) {
            await this._initPython()
        }
    }

    private _restartKernel() {
        showDialog({
            title: "确定要重启内核吗？",
            body: "确定要重启内核吗？",
            buttons: [Dialog.cancelButton({ label: "取消" }),
            Dialog.okButton({ label: '确定' })]
        }).then(ret => {
            if (ret.button.label != "确定") {
                return
            }
            this._context.sessionContext.session?.kernel?.restart()
            if (!this._context.sessionContext.hasNoKernel) {
                this._initPython()
            }
        })
    }

    private _renameNodes() {
        showDialog({
            title: "重命名",
            body: <input type="text" onChange={e => {
                this._renameCache = e.target.value
            }}></input>,
            buttons: [Dialog.cancelButton({ label: "取消" }),
            Dialog.okButton({ label: '确定' })]
        }).then(ret => {
            if (ret.button.label != "确定") {
                return
            }
            this.setCurNodeName(this._renameCache)
            setTimeout(() => { this.onNodesChange(this.editorNodes) })
        })
    }

    private _clearRedoList() {
        this._redoListIndex = 0
        this._redoList = []
    }

    private _createCommand(id, desc, execute) {
        const { commands } = this._app
        const category = "node-editor"
        if (commands.hasCommand(id)) {
            return
        }

        commands.addCommand(id, {
            label: `${id}(${desc})`,
            execute
        })
        this._palette.addItem({
            command: id,
            category
        })
    }

    private _setKernelState(value) {
        const elements = document.querySelectorAll("[data-name='node-editor-kernel-state-label']")
        for (const element of elements) {
            (element as HTMLLabelElement).innerText = value
        }
    }

    private _createCommands() {
        try {
            this._createCommand("nd-load", "加载", () => {
                if (this._isDraggableFocus())
                    this._setMenuOpen(".")
            })
            this._createCommand("nd-create", "创建", () => this.createNewNodes())
            this._createCommand("nd-delete", "删除", () => this.deleteNodes())
            this._createCommand("nd-rename", "重命名", () => this._renameNodes())
            this._createCommand("nd-run-all-cells", "执行所有的cell", () => this.runAllCells())
            this._createCommand("nd-clear-run-cache", "清楚运行缓存", () => this._clearRunCache())
            this._createCommand("nd-undo", "恢复", () => this.redo(-1))
            this._createCommand("nd-redo", "重做", () => this.redo(1))
            this._createCommand("nd-reset-viewport", "重置视口", () => this._focusToAllNodes())
            this._createCommand("nd-toggle-output-area", "切换输出面板", () => this._toggleOutputArea())
            this._createCommand("nd-clear-output-area", "清空输出面板", () => {
                this._clearOutputArea()
                this._clearCurOutput()
            })
            this._createCommand("nd-open-code-editor", "打开编辑器", () => this._openCellEditor())
            this._createCommand("nd-kernel-interrupt", "中断内核", () => this._interuptKernel())
            this._createCommand("nd-kernel-restart", "重启内核", () => this._restartKernel())
            this._createCommand("nd-kernel-change", "更换内核", () => this._selectKernel())
            this._createCommand("nd-select-all", "选中所有节点", () => this._selectAllNodes())
            this._createCommand("nd-delete-selected-nodes", "删除选中的节点", () => this._removeSelectedNodes())
            this._createCommand("nd-copy-selected-nodes", "复制选中的节点", () => this._copySelectedNodes())
            this._createCommand("nd-paste-selected-nodes", "粘贴选中的节点", () => this._pasteSelectedNodes())
            this._createCommand("nd-focus-to-selected-nodes", "聚焦选中的节点", () => this._focusToSelectedNodes())
            this._createCommand("nd-close-image-viewer", "关闭图片浏览器", () => this.setShowImg(false))

            this._createCommand("nd-run-cucrrent-cell", "nd-run-cucrrent-cell(运行当前的Cell)", () => this._editorRun())
            this._createCommand("nd-insert-cell", "nd-insert-cell(插入Cell)", () => {
                this.cellInsert(this._curEditingCellIndex)
                this._editCell(this._curEditingCellIndex)
            })
            this._createCommand("nd-delete-cell", "nd-delete-cell(删除Cell)", () => {
                this.cellRemove(this._curEditingCellIndex)
                let index = this._curEditingCellIndex - 1
                if (index < 0) {
                    index = 0
                }
                this._editCell(this._curEditingCellIndex)
            })

            this._createCommand("nd-cell-undo", "nd-cell-undo(恢复Cell)", () => {
                this.cellUndo()
                this._editCell(this._curEditingCellIndex)
            })

            this._createCommand("nd-cell-redo", "nd-cell-redo(重做Cell)", () => {
                this.cellRedo()
                this._editCell(this._curEditingCellIndex)
            })

            this._createCommand("nd-edit-pre-cell", "nd-edit-pre-cell(编辑上一个Cell)", () => {
                this._editCell(Math.max(this._curEditingCellIndex - 1, 0))
            })

            this._createCommand("nd-edit-next-cell", "nd-edit-next-cell(编辑下一个Cell)", () => {
                const cells = this._context.model.cells
                this._editCell(Math.min(this._curEditingCellIndex + 1, cells.length - 1))
            })

        } catch (error) {

        }
    }
}

const NOTEBOOK_PANEL_TOOLBAR_CLASS = 'jp-NotebookPanel-toolbar';
// 用于承载节点编辑器控件
export class NodeEditorDocumentWidget
    extends DocumentWidget<NodeEditorWidget, NodeBookModel>{
    constructor(options: DocumentWidget.IOptions<NodeEditorWidget, NodeBookModel>) {
        super(options);
        this.toolbar.addClass(NOTEBOOK_PANEL_TOOLBAR_CLASS);
    }
    dispose(): void {
        this.content.dispose();
        super.dispose();
    }
};