from Decorators.task import task

BASECOMMANDS_DESCRIPTION = 'Holds essential commands to use the bot'
BASECOMMANDS_CREDITS = 'Created by @MII#0255 (<https://github.com/MarkTheF4rth/BaseCommands>)'

@task(run_time='init')
async def base_commands_startup(self):
    self.module_info.update({'BaseCommands':(BASECOMMANDS_DESCRIPTION,BASECOMMANDS_CREDITS)})
