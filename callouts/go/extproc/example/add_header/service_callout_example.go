// Copyright 2024 Google LLC.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//	http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package add_header

import (
	extproc "github.com/envoyproxy/go-control-plane/envoy/service/ext_proc/v3"
	server "service-extensions-samples/extproc/service"
	"service-extensions-samples/extproc/utils"
)

type ExampleCalloutService struct {
	server.GRPCCalloutService
}

func NewExampleCalloutService() *ExampleCalloutService {
	service := &ExampleCalloutService{}
	service.Handlers.RequestHeadersHandler = service.HandleRequestHeaders
	service.Handlers.ResponseHeadersHandler = service.HandleResponseHeaders
	return service
}

func (s *ExampleCalloutService) HandleRequestHeaders(headers *extproc.HttpHeaders) (*extproc.ProcessingResponse, error) {

	return &extproc.ProcessingResponse{
		Response: &extproc.ProcessingResponse_RequestHeaders{
			RequestHeaders: utils.AddHeaderMutation(
				[]struct{ Key, Value string }{{Key: "header-request", Value: "Value-request"}},
				nil,
				false,
				nil,
			),
		},
	}, nil
}

func (s *ExampleCalloutService) HandleResponseHeaders(headers *extproc.HttpHeaders) (*extproc.ProcessingResponse, error) {

	return &extproc.ProcessingResponse{
		Response: &extproc.ProcessingResponse_ResponseHeaders{
			ResponseHeaders: utils.AddHeaderMutation(
				[]struct{ Key, Value string }{{Key: "header-response", Value: "Value-response"}},
				nil,
				false,
				nil,
			),
		},
	}, nil
}
