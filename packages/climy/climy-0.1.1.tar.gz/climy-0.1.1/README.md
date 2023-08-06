# climy
Do CLI applications easily.


## Instalation
```shell
$ pip install climy
```

### Basic Usage
```python
from climy import Application, Option, Command


def env_handler(comm: Command):
    print('do every thing with env')
    print(comm)
    print(comm.vars)

    
env_command = Command(
    name='env',
    description='Create a perfect environ to application',
    handler=env_handler
)

app = Application(
    name='acme',
    title='ACME App',
    description='A teste application',
    version='0.1.0',
    option_default_separator=Option.Separators.EQUAL
)
app.add_command(env_command)
app.add_option('host', 'The server allow host IP number.', short='t', var_type='str')
app.add_option('port', 'Service port.', short='p', var_type='int')
app.add_option('path', 'Execution code path.', var_type='str', var_name='path')
app.run()
```
```shell
$ acmesrv --help
ACME App (version 0.1.0)

Usage:
  acme <command> [options] [arguments]

Options:
  -h, --help                Print this help.
  -t, --host=[HOST]         The server allow host IP number.
  -p, --port=[PORT]         Service port.
  --path=[PATH]             Execution code path.

Commands:
  env                       Create a perfect environ to application
```
