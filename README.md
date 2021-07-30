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
ret = qs.call('add', 1, 2)
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

assert qs.compile(script1)
ret = qs.call('plus', 5, 8)
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