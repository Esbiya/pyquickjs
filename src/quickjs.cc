#include "stdarg.h"
#include "string.h"
#include <string>
#include "quickjs/quickjs.h"

using namespace std;

#ifdef WIN32
#define EXPORT __declspec(dllexport)
extern "C"
{
    void* init_runtime();
    void free_runtime(void* rt);
    void* new_context(void* rt);
    void free_context(void* ctx);

    bool compile(void* ctx, const char *script);
    size_t call(void* ctx, const char *funcName, char *out, const char* args);
    size_t run_script(const char *script, char *out);
}
#else
extern "C"
{
    void* init_runtime();
    void free_runtime(void* rt);
    void* new_context(void* rt);
    void free_context(void* ctx);

    bool compile(void* ctx, const char *script);
    size_t call(void* ctx, const char *funcName, char *out, const char* args);
    size_t run_script(const char *script, char *out);
}
#endif

void* init_runtime() {
    void* rt = (void*) JS_NewRuntime();
    return rt;
}

void free_runtime(void* rt) {
    if (rt == nullptr) {
        return;
    }
    JS_FreeRuntime((JSRuntime*)rt);
}

void* new_context(void* rt) {
    if (rt == nullptr) {
        return nullptr;
    }
    void* ctx = (void*) JS_NewContext((JSRuntime*) rt);
    return ctx;
}

void free_context(void* ctx) {
    JS_FreeContext((JSContext*)ctx);
}

bool compile(void* ctx, const char *script) {
    JSContext* _ctx = (JSContext*) ctx;
    JSValue v = JS_Eval(_ctx, script, strlen(script), "", 0);
    if (JS_IsException(v)) {
        js_std_dump_error(_ctx);
        JS_FreeValue(_ctx, v);
        return false;
    }
    JS_FreeValue(_ctx, v);
    return true;
}

size_t call(void* ctx, const char *funcName, char *out, const char* args) {
    JSContext* _ctx = (JSContext*) ctx;

    string script = funcName;
    script.append(args);

    JSValue v = JS_Eval(_ctx, script.c_str(), script.length(), "", 0);

    if (JS_IsException(v)) {
        js_std_dump_error(_ctx);
        JS_FreeValue(_ctx, v);
        return 0;
    }

    const char *ret = JS_ToCString(_ctx, v);
    size_t retLength = strlen(ret);

    memcpy(out, (void *)ret, retLength);

    JS_FreeValue(_ctx, v);

    return retLength;
}

size_t run_script(const char *script, char *out) {
    JSRuntime *rt = JS_NewRuntime();
    JSContext *ctx = JS_NewContext(rt);

    JSValue v = JS_Eval(ctx, script, strlen(script), "", 0);

    if (JS_IsException(v)) {
        js_std_dump_error(ctx);
        JS_FreeValue(ctx, v);
        return 0;
    }

    const char *ret = JS_ToCString(ctx, v);
    size_t retLength = strlen(ret);

    memcpy(out, (void *)ret, retLength);

    JS_FreeValue(ctx, v);
    JS_FreeContext(ctx);
    JS_FreeRuntime(rt);

    return retLength;
}

int main() {
    char out[1024] = {0};
    char out1[1024] = {0};

    char script[] = "function add(a, b) { return a + b; };";

    void* rt = init_runtime();
    void* ctx = new_context(rt);
    if (compile(ctx, script)) {
        int len = call(ctx, "add", out, "(1,2)");

        printf("%s\n", (char *)out);

        int len1 = call(ctx, "add", out, "(3,43)");

        printf("%s\n", (char *)out);
    } else {
        printf("build fail\n");
    };
    free_context(ctx);
    free_runtime(rt);
    return 0;
}
