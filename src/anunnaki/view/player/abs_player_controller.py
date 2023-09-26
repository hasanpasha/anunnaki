from PySide6.QtWidgets import  QWidget
from PySide6.QtGui import QPainter, QKeyEvent, QEnterEvent, QMouseEvent, QTransform
from PySide6.QtCore import Signal, Slot, Qt, QEvent, QPoint, QRect, QMargins

from anunnaki_source.models import Video, Subtitle
from mpv import MPV

keys = {
    Qt.Key.Key_Space: {
        "name": "cycle pause",
        "signal": "mpv_cycle_pause",
    },
    Qt.Key.Key_F: {
        "name": "cycle fullscreen",
        "signal": "mpv_cycle_fullscreen",    
    },
    Qt.Key.Key_Right: {
        "name": "seek right",
        "signal": "mpv_seek",
        "args": [5]
    },
    Qt.Key.Key_Left: {
        "name": "seek left",
        "signal": "mpv_seek",
        "args": [-5]
    }
}

class MPVABSControllerWidget(QWidget):
    # property signals
    fullscreen_changed = Signal(bool)
    video_changed = Signal(Video)
    subtitle_changed = Signal(Subtitle)
    video_played = Signal()
    paused_for_cache = Signal(bool)
    cache_buffering_state_changed = Signal(int)

    # rects click signals
    ctrl_clicked = Signal(QPoint)
    pause_clicked = Signal()
    prev_clicked = Signal()
    next_clicked = Signal()
    seekable_clicked = Signal(QPoint)
    subs_clicked = Signal()
    subs_menu_clicked = Signal(QPoint)
    subs_menu_item_clicked = Signal(int)
    vids_clicked = Signal()
    vids_menu_clicked = Signal(QPoint)
    vids_menu_item_clicked = Signal(int)
    fullscreen_clicked = Signal()

    # key signals
    mpv_cycle_pause = Signal()
    mpv_cycle_fullscreen = Signal()
    mpv_seek = Signal(object)

    def __init__(self, parent: QWidget, mpv: MPV) -> None:
        super().__init__(parent)
        self.mpv = mpv

        self.setMouseTracking(True)

        self.mpv_videos: list[Video] = []
        self.mpv_current_video: Video = None
        self.mpv_subtitles: list[Subtitle] = []
        self.mpv_current_subtitle: Video = None

        self.display_vids_menu: bool = False
        self.display_subs_menu: bool = False
        self.display_ctrl: bool = False
        self.display_loading: bool = False 
        self.cache_per: int = 0
        
        self.mpv.observe_property('fullscreen', lambda _, v: self.fullscreen_changed.emit(v))
        self.mpv.observe_property('paused-for-cache', lambda _, v: self.paused_for_cache.emit(v))
        self.mpv.observe_property('cache-buffering-state',
                    lambda _, v: self.cache_buffering_state_changed.emit(v if v is not None else 100))
        self.mpv.event_callback('file-loaded')(lambda _: self.video_played.emit())
        
        self.video_played.connect(self.on_video_played)
        self.paused_for_cache.connect(self.on_pause_for_cache)
        self.cache_buffering_state_changed.connect(self.on_cache_buffering_state_changed)

        self.video_changed.connect(self.on_video_changed)
        self.subtitle_changed.connect(self.on_subtitle_changed)

        # Click signals
        self.ctrl_clicked.connect(lambda _: self.on_update())
        self.ctrl_clicked.connect(self.on_ctrl_clicked)

        self.pause_clicked.connect(self.on_pause_clicked)
        self.next_clicked.connect(self.on_next_clicked)
        self.prev_clicked.connect(self.on_prev_clicked)
        self.seekable_clicked.connect(self.on_seekable_clicked)
        
        self.vids_clicked.connect(self.set_display_vids_menu)
        self.vids_menu_clicked.connect(lambda _: self.set_display_vids_menu())
        self.vids_menu_clicked.connect(self.on_vids_menu_clicked)
        self.vids_menu_item_clicked.connect(lambda _: self.set_display_vids_menu(False))
        self.vids_menu_item_clicked.connect(self.on_vid_item_clicked)

        self.subs_clicked.connect(self.set_display_subs_menu)
        self.subs_menu_clicked.connect(lambda _: self.set_display_subs_menu())
        self.subs_menu_clicked.connect(self.on_subs_menu_clicked)
        self.subs_menu_item_clicked.connect(lambda _: self.set_display_subs_menu(False))
        self.subs_menu_item_clicked.connect(self.on_sub_item_clicked)

        self.fullscreen_clicked.connect(self.on_fullscreen_clicked)

        # key signals
        self.mpv_cycle_pause.connect(self.do_mpv_cycle_pause)
        self.mpv_cycle_fullscreen.connect(self.do_mpv_cycle_fullscreen)
        self.mpv_seek.connect(self.do_mpv_seek)

    @Slot()
    def on_update(self):
        self.update()

    def set_display_vids_menu(self, display: bool = None):
        if display is not None:
            self.display_vids_menu = display
        else:
            self.display_vids_menu ^= True

    def set_display_subs_menu(self, display: bool = None):
        if display is not None:
            self.display_subs_menu = display
        else:
            self.display_subs_menu ^= True

    def set_videos(self, videos: list[Video]):
        self.mpv_videos = videos

    def set_current_video(self, index):
        self.mpv_current_video = self.mpv_videos[index]
        self.video_changed.emit(self.mpv_videos[index])

    def set_subtitles(self, subtitles: list[Subtitle]):
        self.mpv_subtitles = subtitles

    def set_current_subtitle(self, index):
        self.mpv_current_subtitle = self.mpv_subtitles[index]
        self.subtitle_changed.emit(self.mpv_subtitles[index])
    
    def on_video_played(self):
        if self.mpv_current_subtitle:
            self.on_subtitle_changed(self.mpv_current_subtitle)

    @Slot(Video)
    def on_video_changed(self, video: Video):
        self.mpv.play(video.url)

    @Slot(Subtitle)
    def on_subtitle_changed(self, subtitle: Subtitle):
        if not self.mpv.idle_active:
            try:
                self.mpv.sub_remove() # removes the current subtitle
            except: pass
            self.mpv.sub_add(subtitle.url, title=f"{subtitle.lang} - {subtitle.extension.value}", lang=subtitle.lang)
    
    @Slot(bool)
    def on_pause_for_cache(self, state: bool):
        self.display_loading = state

    @Slot(int)
    def on_cache_buffering_state_changed(self, per: int):
        self.cache_per = per
        self.display_loading = per < 100

    @Slot(int)
    def on_vid_item_clicked(self, index):
        self.set_current_video(index)

    @Slot(int)
    def on_sub_item_clicked(self, index):
        self.set_current_subtitle(index)

    @Slot()
    def on_pause_clicked(self):
        self.mpv.cycle('pause')

    @Slot()
    def on_next_clicked(self):
        print("next clicked")

    @Slot()
    def on_prev_clicked(self):
        print("prev clicked")

    @Slot(QPoint)
    def on_seekable_clicked(self, point: QPoint):
        if not self.mpv.idle_active:
            seekable_rect = self.seekable_rect()
            x = point.x()-seekable_rect.x()
            percent = (x/seekable_rect.width())*100
            self.mpv.seek(percent, reference="absolute-percent")

    @Slot(QPoint)
    def on_vids_menu_clicked(self, point: QPoint):
        vids = self.mpv_videos
        vids_menu_rect = self.vids_list_rect()
        for i in range(len(vids)):
            rect = self.create_list_item_rect(vids_menu_rect, i, len(vids))
            if rect.contains(point):
                self.vids_menu_item_clicked.emit(i)
                break

    @Slot(QPoint)
    def on_subs_menu_clicked(self, point: QPoint):
        subs = self.mpv_subtitles
        subs_menu_rect = self.subs_list_rect()
        for i in range(len(subs)):
            rect = self.create_list_item_rect(subs_menu_rect, i, len(subs))
            if rect.contains(point):
                self.subs_menu_item_clicked.emit(i)
                break
    
    @Slot()
    def on_fullscreen_clicked(self):
        self.mpv.cycle('fullscreen')

    @Slot(QPoint)
    def on_ctrl_clicked(self, point: QPoint):
        if self.pause_cycle_rect().contains(point):
            self.pause_clicked.emit()
        if self.prev_btn_rect().contains(point):
            self.prev_clicked.emit()
        if self.next_btn_rect().contains(point):
            self.next_clicked.emit()
        if self.seekable_rect().contains(point):
            self.seekable_clicked.emit(point)
        if self.subs_list_btn_rect().contains(point):
            self.subs_clicked.emit()
        if self.vids_list_btn_rect().contains(point):
            self.vids_clicked.emit()
        if self.fullscreen_cycle_rect().contains(point):
            self.fullscreen_clicked.emit()

    def do_mpv_cycle_pause(self):
        self.mpv.cycle('pause')
    
    def do_mpv_cycle_fullscreen(self):
        self.mpv.cycle('fullscreen')

    def do_mpv_seek(self, amount):
        if not self.mpv.idle_active:
            self.mpv.seek(amount)

    def ctrl_rect(self) -> QRect:
        raise NotImplementedError()

    def pause_cycle_rect(self) -> QRect:
        raise NotImplementedError()

    def prev_btn_rect(self) -> QRect:
        raise NotImplementedError()
    
    def next_btn_rect(self) -> QRect:
        raise NotImplementedError()
        
    def pos_num_rect(self) -> QRect:
        raise NotImplementedError()
    
    def fullscreen_cycle_rect(self) -> QRect:
        raise NotImplementedError()

    def subs_list_btn_rect(self) -> QRect:        
        raise NotImplementedError()
    
    def vids_list_btn_rect(self) -> QRect:
        raise NotImplementedError()    
    
    def remaining_num_rect(self) -> QRect:
        raise NotImplementedError()
    
    def seekable_rect(self) -> QRect:
        raise NotImplementedError()
    
    def vids_list_rect(self) -> QRect:
        raise NotImplementedError()
    
    def subs_list_rect(self) -> QRect:
        raise NotImplementedError()
    
    def loading_rect(self) -> QRect:
        raise NotImplementedError()    

    def create_list_item_rect(self, rect: QRect, index: int, n: int) -> QRect:
        rect = rect.adjusted(0, index*(rect.height()/n), 0, -rect.height()+((index+1)*(rect.height()/n)))
        return self.margin_two_side(rect, -rect.height()*0.01, -rect.width()*0.01)

    def create_list_rect(self, rect: QRect, n: int, add_width: int = None):
        rect = rect.adjusted(0, -(rect.height()*n), 0, -rect.height())
        if add_width is not None:
            rect = rect.adjusted(-add_width, 0, add_width, 0)
        return rect

    def margin_all_rect(self, rect: QRect, value: int) -> QRect:
        return rect.marginsAdded(QMargins(value, value, value, value))

    def margin_two_side(self, rect: QRect, x: int, y) -> QRect:
        return rect.marginsAdded(QMargins(x, y, x, y))
        
    def scale_text(self, p: QPainter, rect: QRect, text: str) -> QTransform:
        bouding_rect = p.boundingRect(rect, Qt.AlignmentFlag.AlignCenter, text)
        sx = rect.width()*1.0/bouding_rect.width()
        sy = rect.height()*1.0/bouding_rect.height()
        s = min(sx, sy)
        t: QTransform = p.transform()
        t = t.translate(rect.center().x(), rect.center().y())
        t = t.scale(s, s)
        t = t.translate(-rect.center().x(), -rect.center().y())
        return t
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        click_point = event.position().toPoint()
        if self.ctrl_rect().contains(click_point):
            self.ctrl_clicked.emit(click_point)
        elif self.subs_list_rect().contains(click_point):
            if self.display_subs_menu:
                self.subs_menu_clicked.emit(click_point)
        elif self.vids_list_rect().contains(click_point):
            if self.display_vids_menu:
                self.vids_menu_clicked.emit(click_point)
        else:
            print("coming from mpv")
        self.update()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() in keys:
            command = keys[event.key()]
            name = command['name']
            signal_name = command['signal']
            try:
                signal = getattr(self, signal_name)
            except:
                print(f"The controller class doesn't have this signal: {signal_name}")
            else:
                args = []
                if "args" in command.keys():
                    args = command['args']
                signal.emit(*args)
        else:
            print(f"No command registered for this key {event.text()}")

        self.update()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        click_point = event.position().toPoint()
        if self.ctrl_rect().contains(click_point):
            pass
        
        else:
            if event.button() == Qt.MouseButton.LeftButton:
                self.mpv.cycle('fullscreen')
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.display_ctrl = self.ctrl_rect().contains(event.position().toPoint()) or self.display_subs_menu or self.display_vids_menu
        self.update()

    def enterEvent(self, event: QEnterEvent) -> None:
        self.display_ctrl = self.ctrl_rect().contains(event.position().toPoint()) or self.display_subs_menu or self.display_vids_menu
        self.update()

    def leaveEvent(self, event: QEvent) -> None:
        self.display_ctrl = False
        self.update()