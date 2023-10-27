import logging

import gi

from cozy.control.artwork_cache import ArtworkCache
from cozy.db.book import Book
from cozy.ext import inject
from cozy.ui.widgets.playback_speed_popover import PlaybackSpeedPopover
from cozy.view_model.playback_control_view_model import PlaybackControlViewModel

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk

log = logging.getLogger("Headerbar")

COVER_SIZE = 46


@Gtk.Template.from_resource('/com/github/geigi/cozy/media_controller_small.ui')
class MediaControllerSmall(Gtk.Box):
    __gtype_name__ = "MediaControllerSmall"

    play_button: Gtk.Button = Gtk.Template.Child()
    prev_button: Gtk.Button = Gtk.Template.Child()
    next_button: Gtk.Button = Gtk.Template.Child()

    cover_img: Gtk.Image = Gtk.Template.Child()

    playback_speed_button: Gtk.MenuButton = Gtk.Template.Child()

    play_img: Gtk.Image = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.playback_speed_button.set_popover(PlaybackSpeedPopover())

        self._playback_control_view_model: PlaybackControlViewModel = inject.instance(PlaybackControlViewModel)
        self._artwork_cache: ArtworkCache = inject.instance(ArtworkCache)
        self._connect_view_model()
        self._connect_widgets()

        self._on_book_changed()
        self._on_lock_ui_changed()

    def _connect_view_model(self):
        self._playback_control_view_model.bind_to("book", self._on_book_changed)
        self._playback_control_view_model.bind_to("playing", self._on_play_changed)
        self._playback_control_view_model.bind_to("lock_ui", self._on_lock_ui_changed)

    def _connect_widgets(self):
        self.play_button.connect("clicked", self._play_clicked)
        self.prev_button.connect("clicked", self._rewind_clicked)
        self.next_button.connect("clicked", self._forward_clicked)

        self._cover_img_gesture = Gtk.GestureClick()
        self._cover_img_gesture.connect("pressed", self._cover_clicked)
        self.cover_img.add_controller(self._cover_img_gesture)

        self.cover_img.set_cursor(Gdk.Cursor.new_from_name("pointer"))

    def _set_cover_image(self, book: Book):
        pixbuf = self._artwork_cache.get_cover_pixbuf(book, self.get_scale_factor(), COVER_SIZE)
        if pixbuf:
            self.cover_img.set_from_pixbuf(pixbuf)
        else:
            self.cover_img.set_from_icon_name("book-open-variant-symbolic")
            self.cover_img.props.pixel_size = COVER_SIZE

    def _on_book_changed(self):
        book = self._playback_control_view_model.book
        if book:
            visibility = True
            self._set_book()
        else:
            visibility = False

        self._show_media_information(visibility)

    def _show_media_information(self, visibility):
        self.cover_img.set_visible(visibility)

    def _set_book(self):
        book = self._playback_control_view_model.book

        self._set_cover_image(book)

    def _on_play_changed(self):
        playing = self._playback_control_view_model.playing

        play_button_img = "pause-symbolic" if playing else "play-symbolic"
        icon_size = 16 if playing else 20
        self.play_img.set_from_icon_name(play_button_img)
        self.play_img.set_pixel_size(icon_size)

    def _on_lock_ui_changed(self):
        sensitive = not self._playback_control_view_model.lock_ui
        self.prev_button.set_sensitive(sensitive)
        self.next_button.set_sensitive(sensitive)
        self.play_button.set_sensitive(sensitive)
        self.playback_speed_button.set_sensitive(sensitive)

    def _play_clicked(self, _):
        self._playback_control_view_model.play_pause()

    def _rewind_clicked(self, _):
        self._playback_control_view_model.rewind()

    def _forward_clicked(self, _):
        self._playback_control_view_model.forward()

    def _cover_clicked(self, _, __, ___, ____):
        self._playback_control_view_model.open_book_detail()
