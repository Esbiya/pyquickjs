import os, sys, json, _ctypes
from ctypes import CDLL, c_char_p, c_void_p, create_string_buffer
name = "pyquickjs"


p = os.path.dirname(os.path.abspath(__file__))

_os = sys.platform

if _os == "darwin":
    dll = CDLL(f"{p}/lib/macos/libquickjs.dylib")
elif _os == "linux":
    try:
        dll = CDLL(f"{p}/lib/centos/libquickjs.so")
    except:
        dll = CDLL(f"{p}/lib/alpine/libquickjs.so")
elif _os == "win32":
    dll = CDLL(f"{p}/lib/win64/libquickjs.dll")
else:
    raise Exception("unsupport systerm! ")

dll.init_runtime.restype = c_void_p

dll.new_context.argtypes = [c_void_p]
dll.new_context.restype = c_void_p

dll.free_context.argtypes = [c_void_p]

dll.free_runtime.argtypes = [c_void_p]

dll.compile.argtypes = [c_void_p, c_char_p]
dll.compile.restype = bool

dll.call.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
dll.call.restype = int

dll.run_script.argtypes = [c_char_p, c_char_p]
dll.run_script.restype = int

# default_rt = dll.init_runtime()
# default_ctx = dll.new_context(default_rt)


def init_runtime() -> c_void_p:
    """
    初始化运行时
    :return quickjs 运行时 JSRuntime*
    """
    return dll.init_runtime()


def free_runtime(rt: c_void_p):
    """
    释放运行时
    @params rt: quickjs 运行时
    :return
    """
    dll.free_runtime(rt)


def new_context(rt: c_void_p) -> c_void_p:
    """
    初始化上下文
    @params rt: quickjs 运行时
    :return quickjs 上下文 JSContext*
    """
    return dll.new_context(rt)


def free_context(ctx: c_void_p):
    """
    释放上下文
    @params ctx: quickjs 上下文
    :return
    """
    dll.free_context(ctx)

    
def compile(ctx: c_void_p, script: str) -> bool:
    """
    预编译 js 脚本
    @params ctx: quicksjs 上下文
    @params script: 预编译脚本
    :return 编译是否通过: bool
    """
    if not dll.compile(ctx, script.encode()):
        return False
    return True


def call(ctx: c_void_p, func_name: str, args: str or list = [], buffer_length: int = 1024, free: bool = False) -> str:
    """
    调用函数
    @params ctx: js 上下文
    @params func_name: 函数名
    @params args: 参数列表
    @params buffer_length: 缓冲区大小, 默认 1024 字节
    @params free: 执行完是否释放, 默认不释放, 当不再需要使用时请主动调用 dll.free_context 函数释放
    :return 函数返回值: str
    """
    out = create_string_buffer(buffer_length)

    def process_args(_args):
        if isinstance(_args, str):
            _args = [_args]
        __args = []
        for _arg in _args:
            if isinstance(_arg, str):
                __args.append("'{}'".format(_arg))
            elif isinstance(_arg, int):
                __args.append(str(_arg))
            elif isinstance(_arg, dict) or isinstance(_arg, list):
                __args.append(json.dumps(_arg))
        return __args

    _args = f'({",".join(process_args(args))})'
    _length = dll.call(ctx, func_name.encode(), out, _args.encode())
    ret = out[:_length].decode()
    out = None
    if free:
        dll.free_context(ctx)
    return ret


def free():
    """
    释放dll 句柄
    :return
    """
    # dll.free_context(default_ctx)
    # dll.free_runtime(default_rt)
    if _os == "win32":
        _ctypes.FreeLibrary(dll._handle)
    else:
        _ctypes.dlclose(dll._handle)


def run_script(script: str, length: int = 1024):
    """
    执行 js 脚本, 无 console 对象, 如需要请在脚本中自行添加
    @params script: 待执行 js 脚本
    @params length: 接收结果缓冲区大小, 默认 1024 字节
    :return 结果字符串
    """
    out = create_string_buffer(length)

    _length = dll.run_script(script.encode(), out)
    ret = out[:_length].decode()
    out = None
    return ret
