import yaml
import importlib
import inspect
from core import stream_wrapper
from processor_types import ProcessorFn
from typing import List, Union, Callable


def is_generator_function(obj: Callable) -> bool:
    """
    Return True if obj is a generator function.
    """
    return inspect.isgeneratorfunction(obj)


def build_pipeline(config_path: str) -> List[ProcessorFn]:
    """
    Build a data processing pipeline from a YAML configuration file."""
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
            proc_obj = getattr(module, func_name)

            if isinstance(proc_obj, type):
                proc_instance = proc_obj()
            else:
                proc_instance = proc_obj

            sig = inspect.signature(proc_instance)
            if (
                callable(proc_instance)
                and not is_generator_function(proc_instance)
                and len(sig.parameters) == 1
                and sig.return_annotation in [str, inspect.Signature.empty]
            ):
                proc_instance = stream_wrapper(proc_instance)

            processors.append(proc_instance)

        except (ImportError, AttributeError) as e:
            raise ImportError(f"Failed to import '{import_path}': {e}")

    return processors
