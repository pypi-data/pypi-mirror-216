from hatchling.plugin import hookimpl

from .plugin import SpecialEnvironmentCollector


@hookimpl
def hatch_register_environment_collector():
    return SpecialEnvironmentCollector
