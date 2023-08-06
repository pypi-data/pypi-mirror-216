# SyslabAppSdk

[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)]()



SyslabAppSdk is an SDK that is responsible for communication interaction with the Python App and [Syslab](https://www.tongyuan.cc/product/MWorksSyslab). It mainly provides the following interface for the development of APP:

- Get variable list
- Get variable value
- Send script to Syslab for execution
- Close named pipe



## Installation

```bash
pip install -U syslabappsdk
```



## Usage

### Get variable list

``` Python
def mw_get_variables(show_modules: bool) -> (list | Literal[False])
```

| Description | Detail                                                       |
| ----------- | ------------------------------------------------------------ |
| Feature     | get a list of Syslab workspace variables                     |
| Parameter   | show_modules: whether to display a list of modules, usually False |
| Return      | False - failed to get<br>variable list - successed           |

### Get variable value

``` Python
def mw_get_value(var_name: str) -> (str | Literal[False])
```

| Description | Detail                                                       |
| ----------- | ------------------------------------------------------------ |
| Feature     | get Syslab workspace variable value                          |
| Parameter   | var_name: variable name, which can be a child variable such as a.b |
| Return      | False - failed to get<br>variable value string - successed   |

### Send script to Syslab for execution

``` Python
def mw_run_script(code: str,
                  show_code_in_repl: bool,
                  show_result_in_repl: bool) -> (str | Literal[False])
```

| Description | Detail                                                       |
| ----------- | ------------------------------------------------------------ |
| Feature     | execute the Julia script code in the Syslab workspace        |
| Parameter   | code: Julia script to run<br/>show_code_in_repl: whether to display the code in Syslab REPL<br/>show_result_in_repl: whether to display the result in Syslab REPL |
| Return      | False - failed to get<br>result of running code - successed  |

### Close named pipe

``` Python
def close_pipe() -> None
```

| Description | Detail                                                       |
| ----------- | ------------------------------------------------------------ |
| Feature     | Send a request to close the named pipe and call before closing the program |
| Parameter   | none                                                         |
| Return      | none                                                         |
