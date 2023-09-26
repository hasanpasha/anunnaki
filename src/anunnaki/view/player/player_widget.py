from typing import Type
from PySide6.QtGui import QOpenGLContext, QCloseEvent, QKeyEvent, QEnterEvent, QMouseEvent
from PySide6.QtCore import QByteArray, Signal, QEvent
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from mpv import MPV, MpvGlGetProcAddressFn, MpvRenderContext
import ctypes
from anunnaki.view.player.abs_player_controller import MPVABSControllerWidget
from anunnaki_source.models import Video, Subtitle

def get_process_address(_, name):
    glctx =  QOpenGLContext.currentContext()
    address = glctx.getProcAddress(QByteArray(name))
    return ctypes.cast(address, ctypes.c_void_p).value

class MPVWidget(QOpenGLWidget):
    initialized = Signal()
    mpv_updated = Signal()
    fullscreen_changed = Signal(bool)

    def __init__(self, controller_cls: Type[MPVABSControllerWidget], parent=None) -> None:
        super().__init__(parent)
        
        import locale
        locale.setlocale(locale.LC_NUMERIC, "C")
        self.mpv: MPV = MPV(idle=True, keep_open=True, input_default_bindings=True, input_vo_keyboard=True)
        self.ctx: MpvRenderContext = None
        self.ctrl: MPVABSControllerWidget = controller_cls(self, self.mpv)

        self.mpv_updated.connect(self.do_update)
        self.ctrl.fullscreen_changed.connect(self.fullscreen_changed)

        self.setMouseTracking(True)
        self.setUpdateBehavior(QOpenGLWidget.UpdateBehavior.PartialUpdate)

    def initializeGL(self) -> None:
        self.ctx = MpvRenderContext(
            self.mpv, 'opengl',
            opengl_init_params={
                'get_proc_address': MpvGlGetProcAddressFn(get_process_address)
            },    
        )

        if self.ctx:
            self.ctx.update_cb = self.mpv_updated.emit
            self.frameSwapped.connect(self.ctx.report_swap)
            self.initialized.emit()

    def paintGL(self) -> None:
        if self.ctx:
            fbo = self.defaultFramebufferObject()
            self.ctx.render(flip_y=True, opengl_fbo={'w': self.width(), 'h': self.height(), 'fbo': fbo})

        if self.ctrl is not None:
            self.ctrl.setGeometry(self.rect())

    def do_update(self):
        self.update()
        if self.ctrl is not None:
            self.ctrl.update()

    def play(self, videos: list[Video], subtitles: list[Subtitle] = None):
        self.ctrl.set_videos(videos)
        self.ctrl.set_subtitles(subtitles if subtitles is not None else [])

    def _handle_fullscreen(self, v):
        self.showFullScreen() if v else self.showNormal()

    def closeEvent(self, event: QCloseEvent) -> None:
        """free mpv_context and terminate player brofre closing the widget"""
        self.ctx.free()
        self.mpv.terminate()
        event.accept()

    ### Pass all of mouse events to the controller ###
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.ctrl.mouseDoubleClickEvent(event)
        
    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.ctrl.mousePressEvent(event)
        
    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.ctrl.keyPressEvent(event)
        
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.ctrl.mouseMoveEvent(event)
        
    def enterEvent(self, event: QEnterEvent) -> None:
        self.ctrl.enterEvent(event)
        
    def leaveEvent(self, event: QEvent) -> None:
        self.ctrl.leaveEvent(event)