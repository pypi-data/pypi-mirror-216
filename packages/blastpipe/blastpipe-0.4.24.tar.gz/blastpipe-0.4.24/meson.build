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
project('blastpipe', default_options: ['warning_level=3'], license: 'LICENSE', 
 license_files: ['LICENSE.txt'], meson_version: '>=1.1.0', version: run_command(
  'python3', # scm_version_snip
  ['-c', 'from setuptools_scm import get_version;print(get_version(normalize=False))'], 
  check:true
 ).stdout().strip()
)
env             = environment()
source_root     = meson.current_source_dir()
build_root      = meson.current_build_dir()
fs              = import('fs')
pymod           = import('python')
project_name    = get_option('project-name'   ).auto()? meson.project_name() : 'todo'
build_dir       = get_option('build-dir'      ).auto()? fs.stem(build_root)  : 'todo'
source_to_build = get_option('source-to-build').auto()? configuration_data() : 'todo'
docs_source     = get_option('docs-source'    ).auto()? 'subprojects/docs'   : 'todo'
test_source     = get_option('test-source'    ).auto()? 'tests'              : 'todo'
dev  = subproject('dev')
foreach var : get_option('variables')
 name = var.replace('-', '_')
 set_variable(name, dev.get_variable(name))
endforeach
scm_version = run_command(python, ['-c', scm_version_snip], check:true).stdout().strip()
semantic_version = meson.project_version().split('.')
maj_version = semantic_version.get(0)
min_version = semantic_version.get(1)
pat_version = semantic_version.get(2)
configure_file(input: 'pyproject.toml', output: 'pyproject.toml', 
 configuration: configuration_data({
  'PROJECT_NAME' : project_name,
  'MESON_DIST_FALLBACK_VERSION' : '.'.join(maj_version, min_version, pat_version),
 }))
foreach source : ['README.rst', 'CHANGELOG.md', 'NOTICE.md', 'LICENSE.txt']
 fs.copyfile(source)
endforeach
python_files = []
stub_files = []
foreach dir : [project_name, test_source]
 subdir(dir)
endforeach
foreach file : python_files
 python.install_sources(file)
endforeach
# TODO: documentation build imports are broken for dist
# docs = subproject('docs')
# TODO: stub build imports are broken for dist
# stubs = custom_target('stubs', install: true, install_dir: get_option('prefix'),
#  output: stub_files,
#  command: [find_program('pyright', required: true), '--createstub', project_name])
foreach dir : ['prefix', 'bindir', 'libdir', 'datadir', 'localedir', 'python.install_env', 
                'python.platlibdir', 'python.purelibdir']
  summary({'📁 '+dir : get_option(dir)}, section: '〽️ meson install -C @0@'.format(build_dir))
endforeach