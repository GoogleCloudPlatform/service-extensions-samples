load("//:plugins.bzl", "proxy_wasm_plugin_cpp", "proxy_wasm_plugin_rust", "proxy_wasm_tests")

licenses(["notice"])  # Apache 2

proxy_wasm_plugin_rust(
    name = "plugin_rust.wasm",
    srcs = ["plugin.rs"],
    deps = [
        "@crate_index//:log",
        "@crate_index//:proxy-wasm",
        "@crate_index//:regex",
    ],
)

# Blocked on emscripten update to fix Abseil/RE2 compatibility:
# https://github.com/proxy-wasm/proxy-wasm-cpp-sdk/pull/157
# NOTE: Plugins can be built using that PR -- it's blocked on Envoy.
#proxy_wasm_plugin_cpp(
#    name = "plugin_cpp.wasm",
#    srcs = ["plugin.cc"],
#    deps = [
#        "@com_google_re2//:re2",
#        "@proxy_wasm_cpp_sdk//contrib:contrib_lib",
#    ],
#)

proxy_wasm_tests(
    name = "tests",
    plugins = [
        #":plugin_cpp.wasm",
        ":plugin_rust.wasm",
    ],
    tests = ":tests.textpb",
)
