# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
FROM service-callout-common-python

# Copy over example specific files.
COPY extproc/example/add_header/*.py ./

# Set up communication ports.
EXPOSE 443
EXPOSE 8080
EXPOSE 80

# Start the service.
CMD [ "/usr/bin/python3", "-um", "service_callout_example" ]