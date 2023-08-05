import json
import yaml

def write_json(fdir: str, content: dict): 
    with open(fdir, 'w') as f: 
        f.write(json.dumps(content))
        
def write_json_to_gcsfs(fs, fdir, content): 
    with fs.open(fdir, 'w') as f:
        f.write(json.dumps(content))
        
def write_stat_html(fdir: str, content):
    with open(fdir, 'w') as f: 
        f.write(content.data)
        
def write_images(fdir, content): 
    with open(fdir, 'wb') as f: 
        for r in content: 
            f.write(r)

def write_yaml(yaml_filepath: str = '', inp_dict: dict = {}):
    if not yaml_filepath: 
        raise RuntimeError('Invalid yaml path')
    
    with open(yaml_filepath, 'w') as f: 
        yaml.dump(inp_dict, f, default_flow_style=False)
