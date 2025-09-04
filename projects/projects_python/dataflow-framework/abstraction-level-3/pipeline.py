import yaml
import importlib
from typing import List
from processor_types import ProcessorFn

def build_pipeline(config_path: str) -> List[ProcessorFn]:
    """
    Load a list of processor functions dynamically from a YAML config file.
    Args:
        config_path (str): Path to the pipeline YAML config file.
    Returns:
        List[ProcessorFn]: List of processor functions loaded dynamically.
    Raises:
        FileNotFoundError: If the config file is not found.
        ImportError: If a specified processor cannot be imported.
        KeyError: If expected keys in YAML are missing.
    """
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    if "pipeline" not in config:
        raise KeyError("Missing 'pipeline' key in config file")
    processors: List[ProcessorFn] = []
    for step in config["pipeline"]:
        import_path = step.get("type")
        if not import_path:
            raise ValueError("Processor step missing 'type' key")

        module_path, func_name = import_path.rsplit(".", 1)
        try:
            module = importlib.import_module(module_path)
            processor = getattr(module, func_name)
            processors.append(processor)
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Failed to import '{import_path}': {e}")

    return processors
