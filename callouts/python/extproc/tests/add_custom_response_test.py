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

from envoy.config.core.v3.base_pb2 import HeaderMap
from envoy.config.core.v3.base_pb2 import HeaderValue
from envoy.service.ext_proc.v3 import external_processor_pb2 as service_pb2
from envoy.service.ext_proc.v3 import external_processor_pb2_grpc as service_pb2_grpc
import grpc
import pytest

from extproc.example.add_custom_response.service_callout_example import (
    CalloutServerExample as CalloutServerTest)
from extproc.tests.basic_grpc_test import (
    make_request,
    setup_server,
    get_plaintext_channel,
    plaintext_kwargs,
)


# Import the setup server test fixture.
_ = setup_server
_local_test_args = {"kwargs": plaintext_kwargs, "test_class": CalloutServerTest}


@pytest.mark.parametrize('server', [_local_test_args], indirect=True)
def test_mock_header_handling(server: CalloutServerTest) -> None:
  with get_plaintext_channel(server) as channel:
    stub = service_pb2_grpc.ExternalProcessorStub(channel)

    header_map = HeaderMap()
    header_value = HeaderValue(key="mock", raw_value=b"true")
    header_map.headers.extend([header_value])

    mock_headers = service_pb2.HttpHeaders(headers=header_map,
                                           end_of_stream=True)

    response = make_request(stub, request_headers=mock_headers)
    assert response.HasField('request_headers')
    assert any(header.header.key == "Mock-Response" for header in
               response.request_headers.response.header_mutation.set_headers)

    response = make_request(stub, response_headers=mock_headers)
    assert response.HasField('response_headers')
    assert any(header.header.key == "Mock-Response" for header in
               response.response_headers.response.header_mutation.set_headers)


@pytest.mark.parametrize('server', [_local_test_args], indirect=True)
def test_mock_body_handling(server: CalloutServerTest) -> None:
  with get_plaintext_channel(server) as channel:
    stub = service_pb2_grpc.ExternalProcessorStub(channel)

    mock_body = service_pb2.HttpBody(body=b"body-check-mock")

    response = make_request(stub, request_body=mock_body)
    assert response.HasField('request_body')
    assert response.request_body.response.body_mutation.body == b"Mocked-Body"

    response = make_request(stub, response_body=mock_body)
    assert response.HasField('response_body')
    assert response.response_body.response.body_mutation.body == b"Mocked-Body"


@pytest.mark.parametrize('server', [_local_test_args], indirect=True)
def test_header_validation_failure(server: CalloutServerTest) -> None:
  with get_plaintext_channel(server) as channel:
    stub = service_pb2_grpc.ExternalProcessorStub(channel)

    header_map = HeaderMap()
    header_value = HeaderValue(key="bad-header", raw_value=b"")
    header_map.headers.extend([header_value])

    bad_headers = service_pb2.HttpHeaders(headers=header_map,
                                              end_of_stream=True)

    with pytest.raises(grpc.RpcError) as e:
      make_request(stub, request_headers=bad_headers)
    assert e.value.code() == grpc.StatusCode.PERMISSION_DENIED
    with pytest.raises(grpc.RpcError) as e:
      make_request(stub, response_headers=bad_headers)
    assert e.value.code() == grpc.StatusCode.PERMISSION_DENIED


@pytest.mark.parametrize('server', [_local_test_args], indirect=True)
def test_body_validation_failure(server: CalloutServerTest) -> None:
  with get_plaintext_channel(server) as channel:
    stub = service_pb2_grpc.ExternalProcessorStub(channel)

    bad_body = service_pb2.HttpBody(body=b"bad-body")

    with pytest.raises(grpc.RpcError) as e:
      make_request(stub, request_body=bad_body)
    assert e.value.code() == grpc.StatusCode.PERMISSION_DENIED
    with pytest.raises(grpc.RpcError) as e:
      make_request(stub, response_body=bad_body)
    assert e.value.code() == grpc.StatusCode.PERMISSION_DENIED
