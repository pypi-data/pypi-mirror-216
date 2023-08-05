import typer 

''' 
Optipack can be used in 2 ways: 
    - init via cli: optipack init --env <dev/staging/prod> --project <project_name> 
    - setup in code: 

        import optipack 
        optipack.setup(env, project_name) 
'''

app = typer.Typer(no_args_is_help=True)

@app.command(help = 'Initialize workspace')
def init(
    project_name: str = typer.Argument(..., help = 'Name of the project to init, i.e. the folder'),
    env: str = typer.Argument('dev', help='Environment to generate configuration. [dev/stag/prod]'), 
    parent_dir: str = typer.Argument('.', help ='Parent directory'), 
): 
    import optipack
    print(f'Environment: {env}')
    optipack.init(env = env, project_name = project_name, parent_dir=parent_dir)

@app.command(help='Setup')
def setup(

): 
    ...

@app.command(help= 'View project structure')
def view_project(
    project_name: str = typer.Argument(..., help = 'Name of the project to view, i.e. the folder'), 
    parent_dir: str = typer.Argument('.', help ='Parent directory')
): 
    import optipack
    import os
    parent_dir = os.path.join(parent_dir, project_name)
    optipack.utils.visualize_folder_tree(parent_dir, project_name)

# @app.command(help='')
# def 