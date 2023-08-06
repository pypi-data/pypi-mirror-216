# Tasker
Task manager for python
## Quickstart
```python
import sys
import time
from tasker.manager import Manager
from tasker.task import Task

if __name__ == "__main__":
    def example1(attached_outstream = sys.stdout):
        print("1", file=attached_outstream)
        time.sleep(1)
        print("2", file=attached_outstream)
        time.sleep(1)
        print("3", file=attached_outstream)
    def example2(attached_outstream = sys.stdout):
        print("console 2", file=attached_outstream)
    manager = Manager()
    manager.run_attached_stream()
    manager.run_task(Task(example1))
    time.sleep(1)
    manager.run_task(Task(example2))
```