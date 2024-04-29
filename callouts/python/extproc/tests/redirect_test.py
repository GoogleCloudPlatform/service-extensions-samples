# Copyright 2024 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import print_function
from __future__ import annotations
from envoy.config.core.v3.base_pb2 import HeaderMap
from envoy.config.core.v3.base_pb2 import HeaderValue
from envoy.type.v3.http_status_pb2 import StatusCode
from envoy.service.ext_proc.v3 import external_processor_pb2 as service_pb2
from envoy.service.ext_proc.v3 import external_processor_pb2_grpc as service_pb2_grpc
import pytest
import typing

from extproc.example.redirect.service_callout_example import (
    CalloutServerExample as CalloutServerTest,)
from extproc.service.callout_tools import header_immediate_response
from extproc.tests.basic_grpc_test import (
    setup_server,
    get_insecure_channel,
    insecure_kwargs,
    make_request,
)

# Import the setup server test fixture.
_ = setup_server
_local_test_args = {"kwargs": insecure_kwargs, "test_class": CalloutServerTest}


@pytest.mark.parametrize('server', [_local_test_args], indirect=True)
def test_header_immediate_response(server: CalloutServerTest) -> None:
  with get_insecure_channel(server) as channel:
    stub = service_pb2_grpc.ExternalProcessorStub(channel)

    # Construct the HeaderMap
    header_map = HeaderMap()
    header_value = HeaderValue(key="header", raw_value=b"value")
    header_map.headers.extend([header_value])

    # Construct HttpHeaders with the HeaderMap
    headers = service_pb2.HttpHeaders(headers=header_map, end_of_stream=True)

    response = make_request(stub, request_headers=headers)

    assert response.HasField('immediate_response')
    assert response.immediate_response == header_immediate_response(
        code=typing.cast(StatusCode, 301),
        headers=[('Location', 'http://service-extensions.com/redirect')])
