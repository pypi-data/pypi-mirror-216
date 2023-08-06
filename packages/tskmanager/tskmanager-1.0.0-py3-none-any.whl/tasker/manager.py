from typing import TextIO
import threading
from .task import Task
from .attached_stream import AttachedStream

class Manager:
    def __init__(self, *tasks, attach_output=True) -> None:
        self.tasks : Task = tasks
        self.attached_stream = None
        if attach_output:
            self.attached_stream = AttachedStream(self)
            for task in self.tasks:
                task.manager = self
    def run_task(self, task : Task, *args, **kwargs):
        task.run(*args, **kwargs, attached_stream=
            (self.attached_stream.by_task(task) if self.attached_stream != None else None)
        )
    def run_all(self, *args, **kwargs):
        for task in self.tasks:
            self.run_task(task)
        self.run_attached_stream()
    def run_attached_stream(self):
        thread = threading.Thread(target=self.attached_stream.serve)
        thread.start()
        return thread
    
    @property
    def instances(self):
        instances = []
        for task in self.tasks:
            instances += task._instances
        return instances
    
    @property
    def running_instances(self):
        running = []
        for instance in self.instances:
            if instance.running:
                running.append(instance)
        return running
    
    @property
    def failed_instances(self):
        failed = []
        for instance in self.instances:
            if instance.failed:
                failed.append(instance)
        return failed
    
    @property
    def succeeded_instances(self):
        succeeded = []
        for instance in self.instances:
            if (not instance.running) and (not instance.failed):
                succeeded.append(instance)
        return succeeded