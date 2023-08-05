import os
from rich.tree import Tree
from rich.text import Text

def init(
    env: str = '',
    project_name: str = '',
    parent_dir: str = '',
):
    from optipack.sdk.optipack_project_generator import _ProjectGenerator
    from optipack.sdk.optipack_utils import visualize_folder_tree

    assert env, 'Empty environment'
    assert project_name, 'Empty project name'

    # TODO: make project gen to be optional 
    # scenario: user init in-code while running experiments. 
    project_gen = _ProjectGenerator(
        env = env, 
        project_name = project_name, 
        parent_dir = parent_dir
    )
    # 1. generate folder structure 
    project_existed = project_gen._generate_folder_structure()

    if not project_existed: 
        # 2. generate configuration files: 
        project_gen._generate_configs_files()
        # 3. generate code files 
        project_gen._generate_code_files()
 
    vis_dir = os.path.join(parent_dir, project_name)
    visualize_folder_tree(vis_dir, project_name)

    # 5. provide tools init -> move to setup! 