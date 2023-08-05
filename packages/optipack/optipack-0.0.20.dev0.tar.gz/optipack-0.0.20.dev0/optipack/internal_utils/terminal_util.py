import os
from rich import print
from rich.tree import Tree
from rich.text import Text
from rich.markup import escape
from rich.filesize import decimal
from rich.console import Console
from rich.panel import Panel 
from rich.align import Align
import pathlib
# TODO: create a terminal vis class later
# NOTE: this is the utility for optipack developers! differentiate from `optipack_utils.py`
tree_vis = None

def logo_loader(img_dir: str, terminal_size: tuple, term_scale: float = 1.0) -> str:
    
    from PIL import Image

    term_width, term_height = terminal_size
    term_width = int(term_width*term_scale)
    # term_height= int(term_height*term_scale)
    
    img = Image.open(img_dir)
    img_width, img_height = img.size
    scale = img_width / term_width
    term_height = int(img_height / scale)
    term_height = term_height + 1 if term_height % 2 != 0 else term_height
    img = img.resize((term_width, term_height))
    output = ''
    
    for y in range(0, term_height, 2):
        for x in range(term_width):
            r, g, b, _ = img.getpixel((x, y))
            output = output + f'[on rgb({r},{g},{b})] [/]'

        output = output + '\n'

    return output

def start_cli():
    from optipack.core.fileio.reader_misc import read_text

    terminal_size = os.get_terminal_size()
    logo_path = os.environ.get('LARGE_LOGO_PATH')
    scale = 1.0
    if terminal_size[0]<90:
        logo_path = os.environ.get('SMALL_LOGO_PATH')
        scale = 0.5

    if terminal_size[0]>100:
        scale = 0.7

    rich_console = Console()
    optipack_path = os.environ.get('OPTIPACK_PATH', '')
    img_path = os.path.join(
        optipack_path, 
        logo_path
    )
    message_path = os.path.join(
        optipack_path, 
        os.environ.get('MESSAGE_PATH', '')
    )

    if not img_path: 
        rich_console.print(f'Invalid logo path {img_path}', style = 'bold red')
    else: 
        image_str = logo_loader(img_path, terminal_size, scale)
        rich_console.print(Align.center(image_str))

    if not message_path: 
        print(f'Invalid message path {message_path}')
        return 
    
    rich_console.rule('Welcome to Optip⍙ck')
    msg = read_text(message_path)
    rich_console.print(Align.center(Panel.fit(msg), style= 'bold yellow'))

def visualize_folder_tree(parent_dir, project_name): 
    from core.fileio.reader_misc import read_yaml
    tree_vis_dir = os.path.join(
        os.environ.get('OPTIPACK_PATH'), 
        os.environ.get('TREE_VIS_PATH')
    )
    global tree_vis
    tree_vis = read_yaml(tree_vis_dir)
    tree = Tree(f'{project_name} structure')
    tree = __recursive_dir_walk(parent_dir, tree)
    print(tree)

def __recursive_dir_walk(directory, tree): 
    paths = sorted(
        pathlib.Path(directory).iterdir(),
        key=lambda path: (path.is_file(), path.name.lower()),
    )
    for path in paths:
        if path.name.startswith('.'):
            continue
        if path.is_dir():
            style = 'dim' if path.name.startswith('__') else ''
            branch = tree.add(
                f'[bold magenta] {tree_vis.get("folder")} [link file://{path}]{escape(path.name)}',
                style=style,
                guide_style=style,
            )
            __recursive_dir_walk(path, branch)
        else:
            text_filename = Text(path.name, 'green')
            text_filename.highlight_regex(r'\..*$', 'bold red')
            text_filename.stylize(f'link file://{path}')
            file_size = path.stat().st_size
            text_filename.append(f' ({decimal(file_size)})', 'blue')
            icon = tree_vis.get('normal_file')
            if path.suffix in tree_vis: 
                icon = tree_vis.get(path.suffix)
            tree.add(Text(icon) + text_filename)
    return tree