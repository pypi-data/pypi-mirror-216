from climy.option import Option


class Command:
    def __init__(
            self,
            name: str,
            description: str,
            title: str = '',
            handler: callable = None
    ):
        self.commands: dict[str, Command] = {}
        self.options: dict[str, Option] = {}
        self.options_short: dict[str, str] = {}
        self.options_required: set[str] = set()
        self.name = name
        self.title = title
        self.description = description
        self.help_item_tabsize = 25
        self.args = ''
        self.vars = []
        self.handler = handler
        self.parent = None
        self.app = None

    def __str__(self):
        return f'{self.__class__.__name__}:{self.name}'

    def __repr__(self):
        return f'{self.__class__.__name__}:{self.name}'

    def add_command(
            self,
            command: 'Command',
            *,
            name: str = ''
    ):
        command.parent = self
        command.app = self.app
        self.commands[name or command.name] = command

    def add_option(
            self,
            name: str,
            description: str,
            *,
            short: str = '',
            var_type: str = 'bool',
            var_name: str = '',
            required: bool = False
    ):
        option = Option(name=name, description=description, short=short)
        option.var_name = var_name
        option.var_type = var_type
        option.required = required
        self.options[name] = option
        if short:
            self.options_short[short] = name
        if required:
            self.options_required.add(name)

    def run(self):
        if (not self.args and not self.handler) or (self.args and self.args[0] in ['-h', '--help', 'help']):
            text = self.generate_help()
            print(text)
            return
        if self.args:
            command = self.commands.get(self.args[0], None)
            if command:
                command.args = self.args[1:]
                command.run()
                return
        default_separator = self.app.option_default_separator
        args = iter(self.args)
        while True:
            try:
                arg = next(args)
            except Exception as e:
                break
            if default_separator == Option.Separators.EQUAL:
                pair = arg.split('=')
            else:
                pair = [arg]
            idx = 0
            if pair[0].startswith('--'):
                idx = 2
            elif pair[0].startswith('-'):
                idx = 1
            key = pair[0][idx:]
            name = self.options_short.get(key, key)
            option = self.options.get(name, None)
            if not option:
                self.vars = name
                continue
            if name in self.options_required:
                self.options_required.remove(name)
            if default_separator == Option.Separators.SPACE:
                option.value = True if option.var_type == 'bool' else next(args)
            else:
                if option.var_type == 'bool':
                    option.value = True
                else:
                    option.value = pair.pop(1) if len(pair) > 1 else None
        if self.options_required:
            print(f'\033[1;35mSome options are required: [{", ".join(self.options_required)}]')
            return
        if self.handler:
            self.handler(comm=self)

    def generate_help(self, text: str = ''):
        text += "\033[1mUsage:\033[0m\r\n  {name} <command> [options] [arguments]".format(name=self.get_name())
        if self.options:
            text += self.generate_help_options_session()
        if self.commands:
            text += "\r\n\r\n\033[1mCommands:\033[0m\r\n  {opt}".format(opt=self.generate_help_commands_session())
        return text

    @staticmethod
    def generate_help_session(name, content):
        text = "\r\n\r\n\033[1m{name}:\033[0m{content}".format(name=name, content=content)
        return text

    def generate_help_options_session(self):
        key = '-h, --help'
        desc = 'Print this help.'
        content = '\r\n  \033[36m{key: <25}\033[0m {desc}'.format(key=key, desc=desc)
        for option in self.options.values():
            key = f'-{option.short}, --{option.name}' if option.short else f'--{option.name}'
            if option.var_type != 'bool':
                var_name = option.var_name or option.name
                key += f'=[{var_name.upper()}]'
            item = '\r\n  \033[36m{key: <25}\033[0m {desc}'.format(key=key, desc=option.description)
            content += item
        text = self.generate_help_session('Options', content=content)
        return text

    def generate_help_commands_session(self):
        size = self.help_item_tabsize
        text = '\r\n  '.join([f'\033[36m{n.ljust(size)}\033[0m {c.description}' for n, c in self.commands.items()])
        return text

    def get_name(self):
        if self.parent:
            return f'{self.parent.get_name()} {self.name}'
        return self.name

    def set_app(self, app):
        self.app = app
        for command in self.commands.values():
            command.set_app(app)
