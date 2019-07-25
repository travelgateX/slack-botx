from app.common.slack_models import BaseModel,CommandModelIn
from app.tasks.base_tasks import Task, Event,Command,NonImplementedTask
import logging
import importlib
import pkgutil
from app.common.config import Config


import contrib.plugins.commands
import contrib.plugins.events



Config.init_config()
logger = logging.getLogger(__name__)
logger.info("factory start")


# Command pattern: https://python-3-patterns-idioms-test.readthedocs.io/en/latest/FunctionObjects.html
# An object that holds commands:

def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

command_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in iter_namespace(contrib.plugins.commands)
}

event_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in iter_namespace(contrib.plugins.events)
}

class Macro:
    def __init__(self):
        self.tasks = []
    def add(self, task:Task):
        self.tasks.append(task)
    async def run(self):
        for c in self.tasks:
            await c.execute()

def _create_task_instance(task_object:object, data) -> Task:
    logger.info(f"Creating instance:[{task_object}]")
    class_ = getattr(task_object, "Task")
    return class_(data)
    
# Create based on class name:
def event_factory(task_name:str, data:BaseModel) -> Event:
    try:
        return _create_task_instance(event_plugins["contrib.plugins.events."+task_name], data)
    except KeyError as err:
      logger.error(f"Exception create Event instance[{err}]")
    return NonImplementedTask(data)

def command_factory(task_name:str, data:CommandModelIn) -> Command:
    try:
        return _create_task_instance(command_plugins["contrib.plugins.commands."+task_name], data)
    except KeyError as err:
        logger.error(f"Exception create Command instance[{err}]")
    return NonImplementedTask(data)