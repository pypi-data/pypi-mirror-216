from optipack.core.fileio.reader_misc import read_yaml

def environment_setup(appstart_file: str ='.config/app_start.yaml') -> bool:

    import os
    reset_after_run = False

    try: 
        import optipack
        optipack_path = optipack.__path__[0]
    except: 
        reset_after_run = True
        optipack_path = './optipack/'
        
    try: 
         # 1. update entire environ dict
        start_file = os.path.join(optipack_path, appstart_file)
        cfg = read_yaml(start_file)['app_start']
        os.environ.update(cfg)

        # 2. manually setup some env
        if not os.environ['OPTIPACK_PATH']: 
            os.environ['OPTIPACK_PATH'] = optipack_path
    except: 
        raise OSError('Cannot setup environment variables')

def environment_reset(appstart_file: str = '.config/app_start.yaml'): 
    
    import os
    
    optipack_path = os.environ['OPTIPACK_PATH']
    start_file = os.path.join(optipack_path, appstart_file)
    cfg = read_yaml(start_file)
    for k in cfg: 
        os.environ[k] = ''
    