import sys
from climy.command import Command
from climy.option import Option


class Application(Command):
    def __init__(
            self,
            name: str,
            description: str,
            title: str = '',
            version: str = '0.0.0',
            option_default_separator: Option.Separators = Option.Separators.EQUAL,
    ):
        super().__init__(name=name, description=description, title=title)
        self.version = version
        self.workdir: str = ''
        self.option_default_separator = option_default_separator

    def add_command(
            self,
            command: 'Command',
            *,
            name: str = ''
    ):
        command.set_app(self)
        super().add_command(command=command, name=name)

    def generate_help(self, text: str = ''):
        text += "\033[1m{title}\033[0m (version {version})".format(title=self.title, version=self.version)
        text = super().generate_help(text=f'{text}\r\n\r\n')
        return text

    def run(self):
        self.args = [*sys.argv]
        self.workdir = self.args.pop(0)
        super().run()
