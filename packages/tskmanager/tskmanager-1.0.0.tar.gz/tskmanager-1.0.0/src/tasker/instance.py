import threading

class TaskInstance:
    def __init__(self, task, args, kwargs, attach_output) -> None:
        self.running = False
        self.failed = False
        self.succeeded = False
        self.error : Exception | None = None
        self.result = None

        self.task = task
        if attach_output is not None:
            kwargs["attached_outstream"] = attach_output
        self.thread = threading.Thread(target=self._run, args=args, kwargs=kwargs)
        self.thread.start()
    
    def _run(self, *args, **kwargs):
        try:
            self.running = True
            result = self.task.function(*args, **kwargs)
            self.result = result
            self.succeeded = True
            self.running = False
        except Exception as e:
            self.error = e
            self.failed = True
            self.running = False