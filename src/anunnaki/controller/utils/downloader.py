from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QObject, QUrl, Signal, QTimer, QElapsedTimer
import os
import shutil
import tempfile
import logging

class FileDownloader(QObject):
    should_resume: bool
    written_bytes: int
    reply: QNetworkReply
    error: None

    progress = Signal(int)
    finished = Signal(str)
    speed = Signal(float)
    elapsed = Signal(int)
    error_occured = Signal(str)
    
    def __init__(self, parent, network_manager: QNetworkAccessManager = QNetworkAccessManager(),
                tmp_folder: str = None) -> None:
        super().__init__(parent=parent)

        self.nam = network_manager
        self.temp_path = tmp_folder
        if not self.temp_path:
            self.temp_path = tempfile.mkdtemp()

        self.error = None
        self.downloaded_bytes = 0
        self.timer = QTimer(self)
        self.elapsed_timer = QElapsedTimer()
        self.timer.timeout.connect(self.calculate_speed)

    def temp_file_path(self) -> str:
        if self.file_path:
            file_name = QUrl(self.file_path).fileName()
        else:
            file_name = QUrl(self.url).fileName()

        logging.debug(f"{file_name} {self.temp_path}")
        return os.path.join(self.temp_path, file_name)
    
    def check_resumable(self):
        if os.path.exists(self.temp_file_path()):
            self.should_resume = True
            self.written_bytes = os.path.getsize(self.temp_file_path())
        else:
            self.should_resume = False
            self.written_bytes = 0

    def prepare_request(self):
        request = QNetworkRequest(self.url)

        if self.should_resume:
            range_header_name = bytes("Range", 'utf-8')
            range_header_value = bytes(f"bytes={self.written_bytes}-", 'utf-8')
            request.setRawHeader(range_header_name, range_header_value)
            self.elapsed_timer.restart()
            self.should_resume = False
            self.error = None

        return request

    def start_download(self, url: str, file_path: str = None):
        self.url = url
        self.file_path = file_path

        self.check_resumable()
        request = self.prepare_request()
        self.reply = self.nam.get(request)
        
        self.reply.readyRead.connect(self.download_content)
        self.reply.finished.connect(self.download_finished)
        self.reply.errorOccurred.connect(self.handle_download_error)
        self.reply.downloadProgress.connect(self.download_progress)

    def stop_download(self):
        self.reply.abort()
        self.timer.stop()

    def download_progress(self, downloaded, total):
        if total:
            percent = int(((downloaded+self.written_bytes) / (total+self.written_bytes)) * 100)
            self.progress.emit(percent)

    def download_content(self):
        logging.debug("downloading content")
        if not self.timer.isActive():
            self.timer.start(1000)

        if not self.elapsed_timer.isValid():
            self.elapsed_timer.start()

        logging.debug("downloading")
        data = self.reply.readAll()
        with open(self.temp_file_path(), 'ab') as f:
            f.write(data.data())
        
        # self.downloaded_bytes += data.size()

    def calculate_speed(self):
        logging.debug("speed calculating")
        self.speed.emit(self.downloaded_bytes)
        self.elapsed.emit(self.elapsed_timer.elapsed())
        self.downloaded_bytes = 0

    def handle_download_error(self, error: QNetworkReply.NetworkError):
        logging.debug(f"error: {error}")
        self.error = error

        if self.error is not QNetworkReply.NetworkError.OperationCanceledError:
            self.error_occured.emit(str(self.error))

    def move_file(self, src, dest):
        logging.debug("moving the file")
        if shutil.copy(src, dest) == dest:
            os.remove(src)

    def download_finished(self):
        logging.debug("download finished")
        self.timer.stop()
        self.written_bytes = 0
        if not self.error:
            if self.file_path:
                self.move_file(self.temp_file_path(), self.file_path)
                self.finished.emit(self.file_path)
            else:
                self.finished.emit(self.temp_file_path())
                