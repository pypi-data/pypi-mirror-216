import pkg_resources

# __version__ = pkg_resources.get_distribution('optipack').version

def start(): 
    import os
    from .cli import app
    from .internal_utils.file_util import environment_setup, environment_reset
    from .internal_utils.terminal_util import start_cli

    # 1. setup environment 
    reset = environment_setup()
    # 2. view optipack info
    start_cli()
     # 3. cli run
    app(prog_name='optipack') 
    if reset: 
        environment_reset()


start()


