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
 'test_backports.py',
 'test_fuzz.py',
 'test_tailcall.py',
]
python.install_sources(files(config_files), install_tag: 'python-tests')
if get_option('dev').enabled()
 foreach file: config_files
  fs.copyfile(file)
endforeach endif
if get_option('dev').enabled()
 add_test_setup('dev', is_default: true, env: env)
 env.append('TESTS_BUILDDIR', build_root)
 env.append('PYTHONPATH'    , build_root)
 pip = find_program('pip', required: false, disabler: true)
 no_check = {'check': false, 'env': env}
 opt_cov_eq_project_name = '--cov='+project_name
 build_commands = {'dev': []}
 foreach name: namespace
  add_test_setup(name, exclude_suites: get_variable(name+'_exclude_suites'))
  set_variable(name, get_option(name).enable_auto_if(get_option('dev').enabled()))
  set_variable(name+'_kwargs', {'suite': name, 'env': env})
  command_names = dev.get_variable(name+'_suite')
  foreach command: command_names
   _args = get_option('args-'+command)
   command_args = []
   test_app_args = {}
   foreach arg : _args
    if arg.startswith('@') and arg.endswith('@')
     arg = arg.strip('@')
     arg = is_variable(arg)? get_variable(arg) : arg
    endif
    command_args += arg
   endforeach
   if command not in pytest_plugins
    foreach app, args : {command: command_args}
     args = {'args': args, 'env': env, 'priority': get_option(name+'-priority'), 'suite': name}
     if app in should_fail
       args += {'should_fail': true}
     endif
     feature = get_variable(args['suite'])
     test_app = feature.enabled()? dev.get_variable(app.replace('-', '_')) : disabler()
     test_app.found() and feature.enabled()? test(app, test_app, kwargs: args) : false
    endforeach
   endif
  endforeach
 endforeach
endif
