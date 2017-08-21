import discord, asyncio
from Decorators.command import command
from Decorators.task import task
from Decorators.func import func


def construct_message(output_dict, lengths):
    header = ['__**A list and brief description of each command you can use:**__'] 
    message = header # for variable name clarity
    command_length = max(lengths) 

    if len(output_dict) == 1:
        output = output_dict[list(output_dict)[0]] # don't use category headers if theres only 1 category
        return header+['**`{:<{length}} :`** {}'.format(x, y, length=command_length) for x, y in output]

    for category, commands in sorted(output_dict.items()): # sorts alphanumerically TODO: allow flexible sorting
        message.append('\n**{} Commands**:'.format(category))
        message.append('-'*20)
        message = message + ['**`{:<{length}} :`** {}'.format(x, y, length=command_length) for x, y in commands]

    return message

@command(description='Displays this message')
def help(self, message, ctx): 
    command_list = {} 
    output = {} 
    pm_output = {}
    lengths = {'regular':[], 'pm':[]}
    msg_break = '**Continued...**' 
 
    for command_name, command in self.commands.items():
        description = command.get_description(message.channel, message.author.roles)
        if (not description) or (not command.validate_role(message.channel.id, message.author.roles)):
            continue
        command_name = '/'.join(command.aliases)
        command_category = command.get_category(message.channel)

        if 'pm_help' in command.flags: 
            output_dict = pm_output
            lengths['pm'].append(len(command_name))
        else: 
            output_dict = output
            lengths['regular'].append(len(command_name))

        if command_category not in output_dict:
            output_dict[command_category] = []
        output_dict[command_category].append((command_name, description))

    if output: 
        final_message_pb = construct_message(output, lengths['regular'])
        self.message_printer('\n'.join(final_message_pb), message.channel, msg_break=msg_break) 
    else: 
        self.message_printer('No help message can be displayed at this time', message.channel)    

    if pm_output: 
        final_message_pm = construct_message(pm_output, lengths['pm'])
        self.message_printer('\n'.join(final_message_pm), message.author, msg_break=msg_break) 

@command(aliases=['c'], arglen=0, description='Confirms the bot is still alive')
def confirm(self, message, ctx): 
    livemessage = self.addattr()
    self.message_printer(livemessage, message.channel)
