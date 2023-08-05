# Copyright 2023 Ross J. Duff MSc 
# The copyright holder licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
config_files = [
    '__init__.py',
    'backports.py',
    'buffer.py',
    'loop.py',
    'malloc.py',
    'mixin.py',
    'sequence.py',
    'tailcall.py',
]
foreach file: config_files
 stub_files += file+'i'
endforeach
python_files += files(config_files)
if get_option('dev').enabled()
foreach file: config_files
fs.copyfile(file)
endforeach endif
