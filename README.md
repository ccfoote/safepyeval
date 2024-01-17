# safepyeval

`safepyeval` is a Python library designed for the safe evaluation of a restricted subset of Python expressions.
This tool is particularly useful in environments where running arbitrary Python code can pose a security risk,
such as in any application requiring controlled execution of user-submitted code.

The library specifically excludes support for loops (`for` and `while`) due to their potential for creating harmful scenarios,
such as infinite loops or overly complex computations that can drain system resources.

The controlled environment is achieved by parsing the submitted code into an Abstract Syntax Tree (AST) (using the Python ast module), allowing for a granular inspection and execution of code elements. Importantly, the Python interpreter is not used to execute the code, which completely prevents the execution of unsafe operations. Therefore it is extremely safe to use `safepyeval` in any environment.


## Installation

You can install SafePyEval using pip:

```bash
pip install safepyeval
```


## Usage

Import the library and use the evaluate function to safely execute Python code. Here's a basic example:

```python
import safepyeval

code = '''
admin_user_ids = ['admin', 'user1']
if userId in admin_user_ids:
  return True
else:
  return False
'''

result = safepyeval.evaluate(code, {'userId': 'user1'})
# result is True
```

## Capabilities

`safepyeval` supports a variety of Python features while ensuring a secure execution environment:

- Variable Assignments: You can define and use variables within the code.
- Conditional Statements: if, else, and elif statements are supported.
- Comparisons and Boolean Operations: Including ==, !=, <, <=, >, >=, and, or, and not.
- Mathematical and String Operations: Basic operations like +, -, *, /, and string manipulation.
- Data Structures: Use of lists, dictionaries, and access to their elements.

## Limitations

To maintain safety and prevent abuse, safepyeval does not implement certain parts of Python:

- Loops: for and while loops are not implemented, as they can lead to dangerous behavior like infinite loops.
- File I/O: No file reading or writing to prevent unauthorized access to the file system.
- Network Operations: Disabled to prevent network-based attacks or unauthorized data transmission.
- Importing Modules: Importing of modules is disabled.
- Executing Shell Commands: Disabled to avoid executing operating system commands.

## Advanced Example

```python
import safepyeval

code = '''
admin_user_ids = ['magland', 'admin']
max_num_cpus_for_admin = 8
max_num_cpus_for_privileged_users = 4
other_users = {
    'user3': {
        'max_num_cpus': 2
    },
    'user4': {
        'max_num_cpus': 1
    }
}
if userId in admin_user_ids and not userId == 'magland':
    if nCpus <= max_num_cpus_for_admin:
        return True
    else:
        return False
elif userId in ['user1', 'user2']:
    if nCpus <= max_num_cpus_for_privileged_users:
        return True
    else:
        return False
else:
    if userId in other_users:
        if nCpus <= other_users[userId]['max_num_cpus']:
            return True
        else:
            return False
    else:
        return False
'''

result1 = safepyeval.evaluate(code, {'userId': 'user1', 'nCpus': 4})
# result1 is True
result2 = safepyeval.evaluate(code, {'userId': 'user1', 'nCpus': 8})
# result2 is False
# etc.
```

## Size of codebase

The library is very small, consisting of a single Python file (safepyeval.py) with around 100 or so lines of code.

## License

This package is released under Apache License 2.0.

## Author

Created by Jeremy Magland
