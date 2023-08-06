# run_cmd

This code is a simple wrapper for Popen to run shell commands from python. The required version of python is 3.8 or above.

## Installation:

### pip

You can install it via pip:

```
pip install run-cmd
```
### poetry

To install this code, you will need to first install Poetry (https://python-poetry.org/docs/#installation). Poetry is a dependency manager for Python that will allow you to easily install this code and its dependencies.

Once you have Poetry installed, you can install this code by running the following command from the root directory of this code:

```
poetry add run-cmd
```

This will install this code and all of its dependencies.

# Usage:

To use this code, you can simply import the run_cmd function:

```python
from run_cmd.run_cmd import run_cmd

print(run_cmd('ls'))

output:
LICENSE  README.md  log/  poetry.lock  pyproject.toml  run_cmd/
```

Then, you can call the run_cmd function with a shell command as a string:


If an error thrown it caught, and logged before, erroring out.

You can also specify whether you want the output to be returned as a list or a string:

run_cmd('ls', split=True)

This will output the result as a list, with each element being one line of output.

# Script



```python
        script = Scripts()
        script.cmds = """
                        ls
                        echo "an"
                       """
        script()
```
