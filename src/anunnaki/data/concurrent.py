import sys
import time
from PySide6.QtCore import Qt, QRunnable, QThreadPool, Signal, QObject, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QProgressBar
from queue import Queue

class WorkerSignals(QObject):
    finished = Signal()
    progress = Signal(int)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            result = None
            print(e)
        finally:
            self.signals.finished.emit()

class CustomThreadPool(QThreadPool):
    def __init__(self):
        super(CustomThreadPool, self).__init__()
        self.worker_queue = Queue()
        self.worker_timer = QTimer(self)
        self.worker_timer.timeout.connect(self.process_queue)
        self.worker_timer.setInterval(100)  # Adjust the interval as needed
        self.worker_timer.start()
        self.total_tasks = 0
        self.completed_tasks = 0

    def start_worker(self, fn, *args, **kwargs):
        self.total_tasks += 1
        self.worker_queue.put((fn, args, kwargs))

    def process_queue(self):
        if not self.worker_queue.empty():
            fn, args, kwargs = self.worker_queue.get()
            worker = Worker(fn, *args, **kwargs)
            worker.signals.finished.connect(self.worker_finished)
            worker.signals.progress.connect(self.worker_progress)
            self.start(worker)

    def worker_finished(self):
        self.completed_tasks += 1
        if self.completed_tasks == self.total_tasks:
            print("All tasks finished")
            self.completed_tasks = 0
            self.total_tasks = 0

    def worker_progress(self, value):
        print(f"Progress: {value}%")

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_tasks)
        self.layout.addWidget(self.start_button)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.threadpool = CustomThreadPool()

    def start_tasks(self):
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(5)

        for i in range(5):
            self.threadpool.start_worker(self.do_work, i)

    def do_work(self, task_id):
        for i in range(1, 11):
            time.sleep(0.5)
            self.progress_bar.setValue(i * 10)
            self.threadpool.worker_progress(i * 10)  # Emit progress for the current task
        return task_id

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("Custom QThreadPool Example")
    window.setGeometry(100, 100, 400, 200)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
