# import atexit
import os, sys, sysconfig
import _ctypes, ctypes, json
import json

name = "pyquickjs"


if sys.version_info[0] < 3:
    UNICODE_TYPE = unicode  # noqa: F821
else:
    from typing import Any, Optional

    UNICODE_TYPE = str
    
    
def is_unicode(value):
    """Check if a value is a valid unicode string.
    >>> is_unicode(u'foo')
    True
    >>> is_unicode(u'✌')
    True
    >>> is_unicode(b'foo')
    False
    >>> is_unicode(42)
    False
    >>> is_unicode(('abc',))
    False
    """
    return isinstance(value, UNICODE_TYPE)


def _get_libc_name():
    target = sysconfig.get_config_var("HOST_GNU_TYPE")
    if target is not None and target.endswith("musl"):
        return "muslc"
    return "glibc"


p = os.path.dirname(os.path.abspath(__file__))
_os = sys.platform

if _os == "darwin":
    dll = ctypes.CDLL(f"{p}/lib/macos/libquickjs.dylib")
elif _os == "linux":
    if _get_libc_name() == "glibc":
        dll = ctypes.CDLL(f"{p}/lib/centos/libquickjs.so")
    else:
        dll = ctypes.CDLL(f"{p}/lib/alpine/libquickjs.so")
elif _os == "win32":
    dll = ctypes.CDLL(f"{p}/lib/win64/libquickjs.dll")
else:
    raise Exception("unsupport systerm! ")


class Value(ctypes.Structure):
    _fields_ = [
        ("ptr", ctypes.c_char_p),
        ("length", ctypes.c_size_t),
    ]
    
    def to_string(self):
        return self.ptr[:self.length].decode('utf-8')
    
    def __del__(self):
        dll.free_value(self)
    

dll.init_runtime.restype = ctypes.c_void_p

dll.new_context.argtypes = [ctypes.c_void_p]
dll.new_context.restype = ctypes.c_void_p

dll.free_context.argtypes = [ctypes.c_void_p]

dll.free_runtime.argtypes = [ctypes.c_void_p]

dll.free_value.argtypes = [Value]

dll.compile.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
dll.compile.restype = bool

dll.eval.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
dll.eval.restype = Value

dll.run_script.argtypes = [ctypes.c_char_p]
dll.run_script.restype = Value


def init_runtime() -> ctypes.c_void_p:
    """
    初始化运行时
    :return quickjs 运行时 JSRuntime*
    """
    return dll.init_runtime()


def free_runtime(rt: ctypes.c_void_p):
    """
    释放运行时
    @params rt: quickjs 运行时
    :return
    """
    dll.free_runtime(rt)


def new_context(rt: ctypes.c_void_p) -> ctypes.c_void_p:
    """
    初始化上下文
    @params rt: quickjs 运行时
    :return quickjs 上下文 JSContext*
    """
    return dll.new_context(rt)


def free_context(ctx: ctypes.c_void_p):
    """
    释放上下文
    @params ctx: quickjs 上下文
    :return
    """
    dll.free_context(ctx)
    

# @atexit.register
def free():
    """
    释放dll 句柄
    :return
    """
    if os.platform == "win32":
        _ctypes.FreeLibrary(dll._handle)
    else:
        _ctypes.dlclose(dll._handle)


def run_script(script: str):
    """
    执行 js 脚本, 无 console 对象, 如需要请在脚本中自行添加
    @params script: 待执行 js 脚本
    :return 结果字符串
    """
    out = dll.run_script(script.encode('utf-8'))
    return out.to_string()


class QuickJS:
    
    def __init__(self):
        self.rt = dll.init_runtime()
        self.ctx = dll.new_context(self.rt)
    
    def compile(self, script: str) -> bool:
        """
        预编译 js 脚本
        @params script: 预编译脚本
        :return 编译是否通过: bool
        """
        if not dll.compile(self.ctx, script.encode('utf-8')):
            return False
        return True
    
    def execute(self, expr):
        wrapped_expr = u"JSON.stringify((function(){return (%s)})())" % expr
        ret = self.eval(wrapped_expr)
        if not is_unicode(ret):
            raise ValueError(u"Unexpected return value type {}".format(type(ret)))
        return json.loads(ret)
        
    def call(self, expr, *args):
        """
        调用函数
        :param expr: 
        :param args: 
        """
        json_args = json.dumps(args, separators=(',', ':'))
        js = u"{expr}.apply(this, {json_args})".format(expr=expr, json_args=json_args)
        return self.execute(js)

    def eval(self, script: str) -> str:
        """
        eval 脚本
        :param script: 脚本字符串
        :return 脚本返回值: str
        """
        out = dll.eval(self.ctx, script.encode('utf-8'))
        return out.to_string()
    
    def __del__(self):
        dll.free_context(self.ctx)
        dll.free_runtime(self.rt)
