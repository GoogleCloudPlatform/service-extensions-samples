// Copyright 2023 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// [START serviceextensions_plugin_read_only_body]
#include "proxy_wasm_intrinsics.h"

class MyHttpContext : public Context {
 public:
  explicit MyHttpContext(uint32_t id, RootContext* root) : Context(id, root) {}

  FilterDataStatus onRequestBody(size_t body_length,
                                 bool end_of_stream) override {
    WasmDataPtr body =
        getBufferBytes(WasmBufferType::HttpRequestBody, 0, body_length);
    return FilterDataStatus::Continue;
  }

  FilterDataStatus onResponseBody(size_t body_length,
                                  bool end_of_stream) override {
    WasmDataPtr body =
        getBufferBytes(WasmBufferType::HttpResponseBody, 0, body_length);
    return FilterDataStatus::Continue;
  }
};

static RegisterContextFactory register_StaticContext(
    CONTEXT_FACTORY(MyHttpContext), ROOT_FACTORY(RootContext));
// [END serviceextensions_plugin_read_only_body]