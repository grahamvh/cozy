import gi

from cozy.ext import inject

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/geigi/cozy/delete_book_dialog.ui')
class DeleteBookView(Gtk.Window):
    __gtype_name__ = 'DeleteBookDialog'

    main_window = inject.attr("MainWindow")
    delete_button: Gtk.Button = Gtk.Template.Child()
    cancel_button: Gtk.Button = Gtk.Template.Child()

    def __init__(self, view_model, book):
        super().__init__()

        self._view_model=view_model
        self.book=book
        self.delete_button.connect("clicked", self._delete_book)
        self.cancel_button.connect("clicked", self._cancel)

        self.set_modal(self.main_window.window)
        self.show()

    def _delete_book(self, _):
        self._view_model.delete_book_files(self.book)
        self._view_model.remove_book(self.book)
        self.close()

    def _cancel(self, _):
        self.close()

