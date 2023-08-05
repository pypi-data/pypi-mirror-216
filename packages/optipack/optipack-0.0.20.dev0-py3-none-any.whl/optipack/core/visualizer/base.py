from abc import ABC

class BaseVisualizer(ABC):
    def __init__(self,
        name: str, 
        root_dir: str, 
        run_folder: str
    ) -> None:
        self.name = name 
        self.root_dir = root_dir
        self.run_folder = run_folder
