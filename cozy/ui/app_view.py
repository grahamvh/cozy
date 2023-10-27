from gi.repository import Gtk, Adw

from cozy.ext import inject
from cozy.view_model.app_view_model import AppViewModel
from cozy.view import View
import inspect

LIBRARY = "main"
EMPTY_STATE = "no_media"
PREPARING_LIBRARY = "import"
BOOK_DETAIL = "book_overview"

LIBRARY_FILTER = "filter"
LIBRARY_BOOKS = "books"


class AppView:
    _view_model: AppViewModel = inject.attr(AppViewModel)

    def __init__(self, builder: Gtk.Builder):
        self._builder = builder

        self._get_ui_elements()
        self._connect_view_model()
        self._connect_ui_elements()

        self._update_view_model_view(None, None)

    def _get_ui_elements(self):
        self._main_stack: Gtk.Stack = self._builder.get_object("main_stack")
        self._library_leaflet: Adw.Leaflet = self._builder.get_object("library_leaflet")

    def _connect_ui_elements(self):
        self._main_stack.connect("notify::visible-child", self._main_stack_visible)
        self._library_leaflet.connect("notify::folded", self._leaflet_folded)
        self._library_leaflet.connect("notify::visible-child", self._leaflet_visible)

    def _connect_view_model(self):
        self._view_model.bind_to("view", self._on_view_changed)

    def _on_view_changed(self):
        view = self._view_model.view
        print('view changed')

        if view == View.EMPTY_STATE:
            print('empty state')
            self._main_stack.set_visible_child_name(EMPTY_STATE)
        elif view == View.PREPARING_LIBRARY:
            print('Prep library')
            self._main_stack.set_visible_child_name(PREPARING_LIBRARY)
        elif view == View.LIBRARY:
            print('view library')
            self._main_stack.set_visible_child_name(LIBRARY)
            self._library_leaflet.set_visible_child_name(LIBRARY_FILTER)
        elif view == View.LIBRARY_FILTER:
            print('view filter library')
            self._main_stack.set_visible_child_name(LIBRARY)
            self._library_leaflet.set_visible_child_name(LIBRARY_FILTER)
        elif view == View.LIBRARY_BOOKS:
            print('view view lib book')
            self._main_stack.set_visible_child_name(LIBRARY)
            self._library_leaflet.set_visible_child_name(LIBRARY_BOOKS)

    def _main_stack_visible(self, thing1,thing2):
        print("main: notify::visible-child")
        self._update_view_model_view(thing1,thing2)

    def _leaflet_folded(self, thing1,thing2):
        print("notify::folded")
        self._update_view_model_view(thing1,thing2)

    def _leaflet_visible(self, thing1,thing2):
        print("notify::visible-child")
        self._update_view_model_view(thing1,thing2)

    def _update_view_model_view(self, _, __):
        page = self._main_stack.props.visible_child_name
        library_folded = self._library_leaflet.props.folded
        library_page = self._library_leaflet.props.visible_child_name
        #print(library_folded)
        #print(library_page)
        #print(self._library_leaflet.props.visible-child-name)
        print(inspect.getmembers(self._library_leaflet.props))

        if page == EMPTY_STATE:
            self._view_model.view = View.EMPTY_STATE
        elif page == PREPARING_LIBRARY:
            self._view_model.view = View.PREPARING_LIBRARY
        elif page == BOOK_DETAIL:
            self._view_model.view = View.BOOK_DETAIL
        elif page == LIBRARY:
            if library_folded and library_page == LIBRARY_FILTER:
                self._view_model.view = View.LIBRARY_FILTER
            elif library_folded and library_page == LIBRARY_BOOKS:
                self._view_model.view = View.LIBRARY_BOOKS
            elif not library_folded:
                self._view_model.view = View.LIBRARY
