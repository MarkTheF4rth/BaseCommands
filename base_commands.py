import discord, asyncio
from Decorators.command import command
from Decorators.task import task
from Decorators.func import func

def sort_commands(commands, message, channel):
    """Sorts given commands into those that need to be sent by PM and normally
        also returns the longest command length in each case"""

    output = {'reg':{}, 'pm':{}}
    lengths = {'reg':0, 'pm':0}
    output_ref = {'True':'pm', False:'reg'} # maps result of command.pm_help to dict key

    for command_name, command in commands.items():
        description = command.get_description(message.channel, message.author.roles)
        if (not description) or (not channel.validate_role(command_name, message.author.roles)):
            continue
        category_name = command.category_name
        full_command_name = '/'.join(command.get_aliases())

        output_type = output_ref[command.pm_help]
        lengths[output_type] = max(lengths[output_type], len(full_command_name))

        if category_name not in output[output_type]:
            output[output_type][category_name] = {}
        output[output_type][category_name].update({command_name :(full_command_name, description)})

    return output, lengths


def construct_message(output_dict, command_length):
    """Create the mesage to be sent"""
    header = ['__**A list and brief description of each command you can use:**__'] 
    message = header # for variable name clarity

    if len(output_dict) == 1:
        output = output_dict[list(output_dict)[0]] # don't use category headers if theres only 1 category
        return header+['**`{:<{length}} :`** {}'.format(x, y, length=command_length) for x, y in output]

    for category, commands in sorted(output_dict.items()): # sorts categories alphabetically 
        message.append('\n**{} Commands**:'.format(category))
        message.append('-'*20)
        message = message + ['**`{:<{length}} :`** {}'.format(x, y, length=command_length) for x, y in commands]

    return message

@command(description='Displays this message')
def help(self, message, ctx): 
    """Displayed a formatted and sorted list of commands the user has access to"""
    message_ref = {'reg':message.channel, 'pm':message.author} # connect message type to target channel
    msg_break = '**Continued...**' 
 
    channel = self.channels[message.channel.id]
    output, lengths = sort_commands(channel.commands, message, channel)

    for message_type, output_commands in output.items():
        if not output_commands:
            continue

        formatted_commands = {}

        for category, commands in output_commands.items(): # reformat and sort commands
            new_commands = []
            config_category = self.config['Categories'][category]

            if 'commands' in config_category:
                config_commands = config_category['commands']
            else:
                config_commands = []

            for command in config_commands:
                if command in commands: # fail-safe, should normally be true
                    new_commands.append(commands[command])
                    del(commands[command])


            formatted_commands[category] = new_commands + [
                command for command_name, command in sorted(commands.items())]


        final_message_pb = construct_message(formatted_commands, lengths[message_type])
        self.message_printer('\n'.join(final_message_pb), message_ref[message_type],  msg_break=msg_break) 

    if not output['reg'] and not output['pm']: # no help available
        self.message_printer('No help message can be displayed at this time', message.channel)
    elif not output['reg'] and output['pm']: # only PM available, inform channel
        self.message_printer('A list of commands has been sent to you by PM', message.channel)


@command(aliases=['c'], arglen=0, description='Confirms the bot is still alive')
def confirm(self, message, ctx): 
    """prints a message when called to confirm the bot can reach the specified channel"""
    self.message_printer('**I live**', message.channel)
