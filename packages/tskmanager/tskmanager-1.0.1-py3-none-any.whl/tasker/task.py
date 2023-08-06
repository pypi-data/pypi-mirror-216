from .instance import TaskInstance

class Task:
    def __init__(self, function, name : str = ...) -> None:
        self.function = function
        self.name = name
        if name == ...:
            self.name = function.__name__
        self._instances : list[TaskInstance] = []
    
    @property
    def running_instances(self):
        running = []
        for instance in self._instances:
            if instance.running:
                running.append(instance)
        return running
    
    @property
    def failed_instances(self):
        failed = []
        for instance in self._instances:
            if instance.failed:
                failed.append(instance)
        return failed
    
    @property
    def succeeded_instances(self):
        succeeded = []
        for instance in self._instances:
            if (not instance.running) and (not instance.failed):
                succeeded.append(instance)
        return succeeded

    def run(self, *args, attached_stream, **kwargs):
        new_instance = TaskInstance(self, args, kwargs, attach_output=attached_stream)
        self._instances.append(new_instance)
        return new_instance