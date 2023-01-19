from handlers.start_menu import HelpCommand, StartCommand

commands = (StartCommand, HelpCommand)


def register_handlers(app):
    for command in commands:
        app.add_handler(command.get_handler())
