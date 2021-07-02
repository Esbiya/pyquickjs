<h1 align="center">Welcome to pyquickjs 👋</h1>
<p>
</p>

## example

### simple-use

* `build script and call function`

```python
from pyquickjs import QuickJS

script = "function add(a, b) { return a + b };"

qs = QuickJS()
    
assert qs.compile(script)
ret = qs.call('add', 1, 2, buffer_length=10)
print(ret)
```

* `run script with return value`

```python

from pyquickjs import run_script


script = "function add(a, b) { return}; add(1, 2)"

ret = run_script(script)
print(ret)
```

### multi-threaded-call
```python
from pyquickjs import QuickJS
from concurrent.futures import ThreadPoolExecutor, as_completed


def test():
    script = "function add(a, b) { return a + b };"

    qs = QuickJS()
    assert qs.compile(script)
    ret = qs.call('add', 3, 6)
    ret += qs.call('add', 45, 32)
    return ret


with ThreadPoolExecutor(max_workers=4) as executor:
    tasks = [executor.submit(test, ) for _ in range(2)]
    for future in as_completed(tasks):
        print(future.result())
```

### multi-script-build

```python
from pyquickjs import QuickJS

script = "function add(a, b) { return a + b };"
script1 = "function plus(a, b) { return a * b}"

qs = QuickJS()
    
assert qs.compile(script)
ret = qs.call('add', 1, 2, buffer_length=10)
print(ret)

qs.compile(script1)
ret = qs.call('plus', 5, 8)
print(ret)
```

### return-value-length

* `call 接口函数返回值长度默认为 1024 字节, 如果你的函数返回值长度大于 1024 字节, 请将 buffer_length 设置得更大一些, 否则接口会抛出异常, 并且 python 无法捕捉到; 如果你的函数返回值长度小于 1024 字节, 你也可以将 buffer_length 设置的更小, 以节省并发状态下的内存消耗。总之, 请务必保证 buffer_length 大于你的函数返回值长度, 以保证缓冲区有足够的长度接收函数返回值`

* `The length of the return value of the call interface function is 1024 bytes by default. If the length of the return value of your function is greater than 1024 bytes, please set buffer_length to a larger value, otherwise the interface will throw an exception and python cannot catch it; if the length of the return value of your function is less than 1024 bytes, you can also set the buffer_length smaller to save memory consumption in the concurrent state. In short, please ensure that buffer_length is greater than the length of the return value of your function to ensure that the buffer has enough length to receive the return value of the function`

```python
from pyquickjs import QuickJS

script = "function add(a, b) { return a + b };"
script1 = "function plus(a, b) { return a * b}"

qs = QuickJS()
    
assert qs.compile(script)
ret = qs.call('add', 1, 2, buffer_length=81920)
print(ret)

qs.compile(script1)
ret = qs.call('plus', 5, 8, buffer_length=10)
print(ret)
```

### dynamic-library-handle

* `你可以主动调用 free 接口释放动态库句柄, 但是如果使用了 QuickJS 类, 请保证 free 释放动作在类销毁之后, 否则将会抛出异常, 且 python 无法捕捉到(完全可以将动态库句柄交给系统管理, python gc 将会回收它)`

* `The lib provide an interface for users to actively release. If you used QuickJS class, please ensure that call free interface after the QuickJS class destroyed. however, the user can completely hand over the handle to the system management, because the python gc will recycle it`

```python
from pyquickjs import free

# free the dll handle
free()
```

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_