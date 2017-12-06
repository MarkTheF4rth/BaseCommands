from Decorators.command import command

@command(description='Displays the modules being run in the current bot')
def info(self, message, ctx):
    '''Puts together a message that informs the user what modules they are using'''

    output = ['**__A list of loaded modules and a short description of what they do:__**']

    for module_name, module_info in sorted(self.module_info.items()):
        description = '**`{}`** : {}'.format(module_name, module_info[0])
        credits = '**----Credits :** {}\n'.format(module_info[1])
        add_string = '\n'.join([description, credits])

        if module_name == 'Foundation': # put foundation description first
            output.insert(1, add_string)

        else:
            output.append(add_string)
            

    self.message_printer('\n'.join(output), message.channel)
