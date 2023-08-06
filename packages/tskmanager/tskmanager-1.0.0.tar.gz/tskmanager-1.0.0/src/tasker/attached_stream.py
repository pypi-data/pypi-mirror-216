from io import TextIOBase
import curses
import os
import queue
import threading
from .task import Task

class tasked_stream(TextIOBase):
    def __init__(self, base, task) -> None:
        self.base = base
        self.task = task
    def write(self, __s: str) -> int:
        self.base.write(self.task, __s)

class AttachedStream(TextIOBase):
    inited = False

    @classmethod
    def init(cls):
        curses.initscr()
        curses.def_shell_mode()
        curses.curs_set(0)
        cls.inited = True

    @classmethod
    def destroy(cls):
        curses.reset_shell_mode()
        curses.endwin()
        cls.inited = False

    def __init__(self, manager):
        self.manager = manager
        self.windows : list[tuple[Task, curses._CursesWindow]] = []
        self.output_queue = queue.Queue()
        self.screen_lock = threading.Lock()
    def by_task(self,new_task):
        self.screen_lock.acquire()
        if not type(self).inited:
            type(self).init()
        width = (os.get_terminal_size().columns) // (len(self.windows)+1)
        offset = 0
        for task, window in self.windows:
            window.resize(os.get_terminal_size().lines - 1, width)
            window.box()
            y, x = window.getyx()
            self.name_window(window, getattr(task, "name", ""))
            window.move(y, x)
            window.refresh()
            offset += width
        new_window = curses.newwin(os.get_terminal_size().lines - 1, width, 0, offset)
        new_window.box()
        self.name_window(new_window, getattr(new_task, "name", ""))
        new_window.move(1, 1)
        self.windows.append((new_task, new_window))
        self.screen_lock.release()
        return tasked_stream(self, new_task)
    def serve(self):
        while True:
            try:
                task, s = self.output_queue.get(timeout=2)
                self.screen_lock.acquire()
                self.write_immediate(task, s)
                self.screen_lock.release()
            except queue.Empty:
                for task, _ in self.windows:
                    if isinstance(task, Task) and task.running_instances:
                        break
                else:
                    type(self).destroy()
                    break
    def name_window(self, window, name):
        height, width = window.getmaxyx()
        pos = (width // 2) - (len(name) // 2)
        if pos < 0: pos = 0
        if width >= len(name):
            to_print = name
        else:
            to_print = name[:width-3] + "..."
        window.move(0, pos)
        window.addstr(to_print)
    def write_immediate(self, task, s):
        for t, window in self.windows:
            if t == task:
                y, x = window.getyx()
                lines = s.split("\n")
                for line in lines:
                    window.move(y, x)
                    window.addstr(line)
                    y += 1
                    x = 1
                window.refresh()
                return
        raise ValueError("Task not found")
    def write(self, task, s):
        self.output_queue.put((task, s))