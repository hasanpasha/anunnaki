from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QBrush, QColor, QPaintEvent
from PySide6.QtCore import Qt, QRect
from PySide6.QtSvg import QSvgRenderer
from mpv import MPV
import datetime
from anunnaki.view.player.abs_player_controller import MPVABSControllerWidget

class DefaultController(MPVABSControllerWidget):
    def __init__(self, parent: QWidget, mpv: MPV) -> None:
        super().__init__(parent, mpv)
        
    def ctrl_rect(self) -> QRect:
        return self.rect().adjusted(0, self.height()-(self.height()*0.04), 0, 0)

    def left_side_rect(self) -> QRect:
        ctrl_rect = self.ctrl_rect()
        ctrl_width = ctrl_rect.width()
        ctrl_height = ctrl_rect.height()
        return ctrl_rect.adjusted(0, 0, -ctrl_width+ctrl_height*8, 0)
    
    def right_side_rect(self) -> QRect:
        ctrl_rect = self.ctrl_rect()
        ctrl_width = ctrl_rect.width()
        ctrl_height = ctrl_rect.height()
        return ctrl_rect.adjusted(ctrl_width-(ctrl_height*10), 0, 0, 0)    

    def pause_cycle_rect(self) -> QRect:
        left_rect = self.left_side_rect()
        left_width = left_rect.width()
        left_height = left_rect.height()
        return left_rect.adjusted(0, 0, -left_width+left_height*1, 0)

    def prev_btn_rect(self) -> QRect:
        left_rect = self.left_side_rect()
        left_width = left_rect.width()
        left_height = left_rect.height()
        return left_rect.adjusted(left_height*1, 0, -left_width+left_height*2, 0)

    def next_btn_rect(self) -> QRect:
        left_rect = self.left_side_rect()
        left_width = left_rect.width()
        left_height = left_rect.height()
        return left_rect.adjusted(left_height*2, 0, -left_width+left_height*3, 0)
    
    def pos_num_rect(self) -> QRect:
        left_rect = self.left_side_rect()
        left_height = left_rect.height()
        return left_rect.adjusted(left_height*4, 0, 0, 0)
    
    def fullscreen_cycle_rect(self) -> QRect:
        right_rect = self.right_side_rect()
        right_width = right_rect.width()
        right_height = right_rect.height()
        return right_rect.adjusted(right_width-right_height*1, 0, 0, 0) 

    def subs_list_btn_rect(self) -> QRect:        
        right_rect = self.right_side_rect()
        right_width = right_rect.width()
        right_height = right_rect.height()
        return right_rect.adjusted(right_height*5, 0, -right_width+right_height*6, 0) 

    def vids_list_btn_rect(self) -> QRect:
        right_rect = self.right_side_rect()
        right_width = right_rect.width()
        right_height = right_rect.height()
        return right_rect.adjusted(right_height*7, 0, -right_width+right_height*8, 0) 
        
    def remaining_num_rect(self) -> QRect:
        right_rect = self.right_side_rect()
        right_width = right_rect.width()
        right_height = right_rect.height()
        return right_rect.adjusted(0, 0, -right_width+right_height*3, 0) 

    def seekable_rect(self) -> QRect:
        left_width = self.left_side_rect().width()
        right_width = self.right_side_rect().width()
        return self.ctrl_rect().adjusted(left_width, 0, -right_width, 0)
    
    def vids_list_rect(self) -> QRect:
        vids_btn_rect = self.vids_list_btn_rect()
        return self.create_list_rect(vids_btn_rect, len(self.mpv_videos), add_width=vids_btn_rect.width())

    def subs_list_rect(self) -> QRect:
        subs_btn_rect = self.subs_list_btn_rect()
        return self.create_list_rect(subs_btn_rect, len(self.mpv_subtitles), add_width=subs_btn_rect.width())

    def loading_rect(self) -> QRect:
        rect = self.rect()
        rect_width_center = rect.width()/2
        rect_height_center = rect.height()/2
        this_width = rect.width()/20
        return self.margin_two_side(rect, -(rect_width_center-this_width), -(rect_height_center-this_width))

    def paintEvent(self, event: QPaintEvent) -> None:
        MARGIN_FACTOR = 0.15

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)

        if self.display_ctrl:
            self.paint_ctrl(p)
        
        if self.display_loading:
            loading_rect = self.loading_rect()
            loading_circle_rect = self.margin_two_side(loading_rect, -(loading_rect.width()*0.1), -(loading_rect.height()*0.1))
            loading_text_rect = self.margin_two_side(loading_circle_rect, 
                                -(loading_circle_rect.width()*0.2), -(loading_circle_rect.height()*0.2))
            p.fillRect(loading_rect, QColor("#3f1f1f1f"))
            cache_per = self.cache_per
            if cache_per:
                text = f"{cache_per}%"
                p.save()
                p.setPen(Qt.GlobalColor.white)

                # Loading circle
                p.drawPie(loading_circle_rect, (0*16), (cache_per*3.6)*16)

                # Text
                t = self.scale_text(p, loading_text_rect, text)
                p.setTransform(t)
                p.drawText(loading_text_rect, Qt.AlignmentFlag.AlignCenter, text)
                p.restore()

        p.end()

    def paint_ctrl(self, p: QPainter):
        MARGIN_FACTOR = 0.15

        # ctrl background
        p.fillRect(self.ctrl_rect(), QBrush(QColor("#7f000000")))

        # Numbers
        pos_num = self.mpv.time_pos
        if pos_num is not None:
            p.save()
            p.setPen(Qt.GlobalColor.white)
            text = str(datetime.timedelta(seconds=int(pos_num)))
            pos_rect = self.pos_num_rect()
            pos_rect_margined = self.margin_two_side(pos_rect, -pos_rect.width()*MARGIN_FACTOR/2, -pos_rect.height()*MARGIN_FACTOR/2) 
            t = self.scale_text(p, pos_rect_margined, text)
            p.setTransform(t)
            p.drawText(pos_rect, Qt.AlignmentFlag.AlignCenter, text)
            p.restore()
        
        remaining_num = self.mpv.time_remaining
        if remaining_num is not None:
            p.save()
            p.setPen(Qt.GlobalColor.white)
            remaining = str(datetime.timedelta(seconds=int(remaining_num)))
            text = f"-{remaining}"
            remaining_rect = self.remaining_num_rect()
            remaining_rect_margined = self.margin_two_side(remaining_rect, -remaining_rect.width()*MARGIN_FACTOR/2, -remaining_rect.height()*MARGIN_FACTOR/2)
            t = self.scale_text(p, remaining_rect_margined, text)
            p.setTransform(t)
            p.drawText(remaining_rect, Qt.AlignmentFlag.AlignCenter, text)
            p.restore()

        # seekable
        seekable_rect = self.seekable_rect()
        p.fillRect(seekable_rect, QBrush(QColor("#2fffffff"))) 
        pos_per = self.mpv.percent_pos
        if pos_per is not None:
            seekable_width = seekable_rect.width()
            pos_rect = seekable_rect.adjusted(0, 0,
                -seekable_width+(seekable_width*(pos_per*0.01)), 0)
            pos_rect = self.margin_all_rect(pos_rect, -2)
            p.fillRect(pos_rect, QBrush(QColor("#dfffffff")))

        # cache
        cached_time = self.mpv.demuxer_cache_time
        if cached_time:
            cache_time_per = cached_time / self.mpv.duration
            seekable_width = seekable_rect.width()
            cache_rect = seekable_rect.adjusted(seekable_width*(pos_per*0.01), 0,
                -seekable_width+(seekable_width*cache_time_per), 0)
            cache_rect = self.margin_two_side(cache_rect, -2, -cache_rect.height()*0.45)
            p.fillRect(cache_rect, QBrush(QColor("#bfffffff")))
        
        # pause cycle button
        pause_rect = self.pause_cycle_rect()
        if self.mpv.pause:
            pause_svg = QSvgRenderer("icons/pause.svg")
        else:
            pause_svg = QSvgRenderer("icons/play.svg")
        pause_svg.render(p, self.margin_two_side(pause_rect, -pause_rect.width()*MARGIN_FACTOR, 
                                                 -pause_rect.height()*MARGIN_FACTOR))

        # previous button
        prev_rect = self.prev_btn_rect()
        left_svg = QSvgRenderer("icons/left.svg")
        left_svg.render(p, self.margin_two_side(prev_rect, -prev_rect.width()*MARGIN_FACTOR, 
                                                -prev_rect.height()*MARGIN_FACTOR))

        # next button
        next_rect = self.next_btn_rect()
        right_svg = QSvgRenderer("icons/right.svg")
        right_svg.render(p, self.margin_two_side(next_rect, -next_rect.width()*MARGIN_FACTOR, 
                                                 -next_rect.height()*MARGIN_FACTOR))

        # fullscreen cycle button
        fullscreen_rect = self.fullscreen_cycle_rect()
        if self.mpv.fullscreen:
            fullscreen_svg = QSvgRenderer("icons/normal.svg")
        else:
            fullscreen_svg = QSvgRenderer("icons/fullscreen.svg")
        fullscreen_svg.render(p, self.margin_two_side(fullscreen_rect, 
                -fullscreen_rect.width()*MARGIN_FACTOR, -fullscreen_rect.height()*MARGIN_FACTOR))

        # subs list
        sub_rect = self.subs_list_btn_rect()
        sub_svg = QSvgRenderer("icons/subtitle.svg")
        sub_svg.render(p, self.margin_two_side(sub_rect, -sub_rect.width()*MARGIN_FACTOR, 
                                                -sub_rect.height()*MARGIN_FACTOR))
        if self.display_subs_menu:
            sub_list_rect = self.subs_list_rect()
            # p.fillRect(sub_list_rect, QBrush(QColor("#af1f1f1f")))
            for i, sub in enumerate(self.mpv_subtitles):
                name = f"{sub.lang} - {sub.extension.value}"
                rect = self.create_list_item_rect(sub_list_rect, i, len(self.mpv_subtitles))
                p.save()
                if self.mpv_current_subtitle == sub:
                    p.fillRect(rect, QBrush(QColor("#afffffff")))
                    p.setPen(QColor("#ff232630"))
                else:
                    p.fillRect(rect, QBrush(QColor("#9f232630")))
                    p.setPen(QColor("#afffffff"))
                
                t = self.scale_text(p, self.margin_two_side(rect, -rect.width()*0.2, -rect.height()*0.2), name)
                p.setTransform(t)
                p.drawText(rect, Qt.AlignmentFlag.AlignCenter, name)
                p.restore()

        # video list
        vid_rect = self.vids_list_btn_rect()
        video_svg = QSvgRenderer("icons/video.svg")
        video_svg.render(p, self.margin_two_side(vid_rect, -vid_rect.width()*MARGIN_FACTOR, 
                                                 -vid_rect.height()*MARGIN_FACTOR))
        if self.display_vids_menu:
            video_list_rect = self.vids_list_rect()
            # p.fillRect(video_list_rect, QBrush(QColor("#ff1f1f1f")))
            for i, vid in enumerate(self.mpv_videos):
                name = str(vid.resolution.value)
                rect = self.create_list_item_rect(video_list_rect, i, len(self.mpv_videos))
                p.save()
                if self.mpv_current_video == vid:
                    p.fillRect(rect, QColor("#afffffff"))
                    p.setPen(QColor("#ff232630"))
                else:
                    p.fillRect(rect, QColor("#9f232630"))
                    p.setPen(QColor("#afffffff"))
                
                t = self.scale_text(p, self.margin_two_side(rect, -rect.width()*0.2, -rect.height()*0.2), name)
                p.setTransform(t)
                p.drawText(rect, Qt.AlignmentFlag.AlignCenter, name)
                p.restore()