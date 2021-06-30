<h1 align="center">Welcome to pyquickjs 👋</h1>
<p>
</p>

## example

```python
import pyquickjs as quickjs
from concurrent.futures import ThreadPoolExecutor, as_completed


def test():
    script = "function add(a, b) { return a + b };"

    # 当使用多线程时, 需要创建新的 quickjs 运行时和上下文
    rt = quickjs.init_runtime()
    ctx = quickjs.new_context(rt)
    
    # 编译使用你新建的上下文
    if quickjs.compile(ctx, script):
        # 调用函数使用你新建的上下文
        ret = quickjs.call(ctx, "add", [1, 2])

        # 使用 free=True 时执行完自动释放创建的上下文
        # ret = call("add", [3, 43], free=True)
        # buffer_length 控制缓冲区大小 节省内存
        ret += quickjs.call(ctx, "add", [3, 43], buffer_length=10)
    else:
        print("script build error")
    
    # 使用完需要释放, 注意释放顺序, 先释放上下文再释放运行时
    quickjs.free_context(ctx)
    quickjs.free_runtime(rt)
    return ret


# 多线程运行时, 每个线程都必须绑定自己的 quickjs 运行时和上下文
with ThreadPoolExecutor(max_workers=4) as executor:
    tasks = [executor.submit(test, ) for _ in range(2)]
    for future in as_completed(tasks):
        print(future.result())


# 创建新的 quickjs 运行时和上下文, 单线程运行时可复用
rt = quickjs.init_runtime()
ctx = quickjs.new_context(rt)

script = "function add(a, b) { return a + b };"
if quickjs.compile(ctx, script):
    ret = quickjs.call(ctx, "add", [1, 2])
    ret += quickjs.call(ctx, "add", [3, 43], buffer_length=10)
    print(ret)
else:
    print("script build error")

script1 = "function plus(a, b) { return a * b };"

if quickjs.compile(ctx, script1):
    ret = quickjs.call(ctx, "plus", [1, 2])
    ret += quickjs.call(ctx, "plus", [3, 43], buffer_length=10)
    print(ret)
else:
    print("script build error")

# 使用完需要释放, 注意释放顺序, 先释放上下文再释放运行时
quickjs.free_context(ctx)
quickjs.free_runtime(rt)

# 退出整个模块时需要调用该函数释放 dll 句柄
quickjs.free()
```

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_