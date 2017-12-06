from Decorators.command import command

@command(aliases=['c'], description='Confirms the bot is still alive')
def confirm(self, message, ctx):
    """prints a message when called to confirm the bot can reach the specified channel"""
    self.message_printer('**I live**', message.channel)
