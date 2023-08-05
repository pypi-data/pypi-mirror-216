import os
import pathlib

class _ProjectGenerator:
    """Project generator class
        protected for internal used only 
    """

    def __init__(
            self, 
            env: str, 
            project_name: str, 
            parent_dir: str = '.'
        ) -> None:

        
        self._project_name = project_name
        self._env = env

        self._parent_dir = os.path.join(parent_dir, self._project_name)
        if not os.path.exists(self._parent_dir): 
            os.mkdir(self._parent_dir)

        self._optipack_path = os.environ.get('OPTIPACK_PATH', '')
        assert self._optipack_path, 'Cannot find path to Optipack package'

        self.__connection_files = ['CONNECTION_CONFIG', 'HYPERPARAM_CONFIG'] # REWORK THIS!
        self.__code_files = ['CODE_PATH_CONFIG']
        self.__cfg_gen_mapper = {
            'CONNECTION_CONFIG': self.__generate_connection_configs, 
            'HYPERPARAM_CONFIG': self.__generate_hyperparam_configs,  
            'RUN_CONFIG': self.__copy_file
        }

    def __structure_existed(self):  
        for k in self._folder_structure: 
            if isinstance(k, dict): 
                continue
            path = os.path.join(self._parent_dir, k)
            if os.path.exists(path):
                # logger
                print(f'Exist inner path {path}')
                return True 
        return False

    def _generate_folder_structure(self): 
        
        from optipack.core.fileio.reader_misc import read_yaml

        proj_struct_cfg_path = os.environ.get('PROJECT_STRUCTURE', '')
        assert proj_struct_cfg_path, 'Empty project structure path'
        
        self._structure_dir = os.path.join(self._optipack_path, proj_struct_cfg_path)
        fs = read_yaml(self._structure_dir)
        self._folder_structure = fs.get('project_structure', [])
        # check to see if we need generation 
        if self.__structure_existed():
            return True
        
        self.__recursive_gen_folder(self._parent_dir, self._folder_structure)
        return False

    def __recursive_gen_folder(self, parent_dir: str, folder_structure: list): 
        if not folder_structure:
            # print('End of folder tree...')
            return

        fs = folder_structure.pop()
        folder = fs

        if isinstance(fs, dict):
            folder = str(list(fs.keys())[0])
            new_dir = os.path.join(parent_dir, folder)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            self.__recursive_gen_folder(new_dir, fs[folder])

        else:     
            new_dir = os.path.join(parent_dir, folder)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
        self.__recursive_gen_folder(parent_dir, folder_structure)

    def _generate_configs_files(self): 
        
        from optipack.core.fileio.reader_misc import read_yaml
        
        for path in self.__cfg_gen_mapper: 
            cfg_path = os.environ.get(path, '')    
            assert cfg_path, f'Empty {path} config path'
            cfg_path = os.path.join(self._optipack_path, cfg_path)
            cfg_dict = read_yaml(cfg_path)
            func = self.__cfg_gen_mapper.get(path)
            # print(f'Writing {path}')
            func(cfg_dict)

    def __generate_connection_configs(self, cfg_dict): 

        from optipack.core.fileio.reader_misc import write_yaml
        
        root_dir = os.path.join(self._parent_dir, cfg_dict.get('root_dir', ''))
        assert root_dir, 'Empty connection root dir'
        folder = cfg_dict.get('folder', '')
        assert folder, 'Empty connection folder'

        cfg_dir = os.path.join(root_dir, folder)
        if not os.path.exists(cfg_dir): 
            os.mkdir(cfg_dir)
        
        configurations = cfg_dict.get('config', {})
        assert configurations, 'Empty connection configuration'
        for cfg_name in configurations: 
            inner_cfg_path = os.path.join(cfg_dir, f'{cfg_name}.yaml')
            cfg = configurations[cfg_name]
            out_cfg = self.__generate_tooling_configs(
                cfg_dict = cfg, 
                tool_name = cfg_name, 
                key_list = ['host', 'search_index', 'branch']
            )
            write_yaml(inner_cfg_path, out_cfg) 
    
    def __generate_tooling_configs(self, cfg_dict, tool_name, key_list: list = []):
        out_dict = {}
        for key in key_list: 
            if not key in cfg_dict:
                continue
            inner_dict = cfg_dict.get(key)
            assert inner_dict, f'Empty {tool_name} {key}'
            out_dict[key] = inner_dict.get(self._env)
            del cfg_dict[key]
        out_dict.update(cfg_dict)
        return out_dict
    
    def __generate_hyperparam_configs(self, cfg_dict): 
        from optipack.core.fileio.reader_misc import write_yaml
        
        root_dir = os.path.join(self._parent_dir, cfg_dict.get('root_dir', ''))
        assert root_dir, 'Empty hyperparameters root dir'
        folder = cfg_dict.get('folder', '')
        assert folder, 'Empty hyperparameters folder'

        cfg_dir = os.path.join(root_dir, folder)
        if not os.path.exists(cfg_dir): 
            os.mkdir(cfg_dir)
        
        hyperparam_cfg = cfg_dict.get('config', {})
        assert hyperparam_cfg, 'Empty hyperparameters config'
        
        for cfg_name in hyperparam_cfg: 
            cfg_path = os.path.join(cfg_dir, f'{cfg_name}.yaml')
            cfg = hyperparam_cfg.get(cfg_name, {})
            assert cfg, f'Empty {cfg_name} configs'
            write_yaml(cfg_path, cfg)
    
    def __copy_file(self, cfg_dict): 
        from optipack.core.fileio.writer_misc import write_yaml

        root_dir = os.path.join(self._parent_dir, cfg_dict.get('root_dir', ''))
        assert root_dir, 'Empty run config root dir'
        
        cfg_dir = os.path.join(root_dir, f'run_config.yaml')
        cfg = cfg_dict.get('config', {})
        assert cfg, 'Empty run config'

        write_yaml(cfg_dir, cfg)

    def _generate_code_files(self): 
        ...
