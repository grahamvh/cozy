from typing import List, Callable
import traceback

import gi

gi.require_version('Gdk', '4.0')

from gi.repository import Gdk, GLib


class EventSender:
    _listeners: List[Callable]

    def __init__(self):
        self._listeners = []

    def emit_event(self, event, message=None):
        if type(event) is tuple and not message:
            message = event[1]
            event = event[0]
        if str(event) == "view":
            print("emit_event(" + str(event) + ", " + str(message) + ")")
            print("listeners:" + str(len(self._listeners)))
            traceback.print_stack()
        
        for function in self._listeners:
            function(event, message)

    def emit_event_main_thread(self, event: str, message=None):
        GLib.MainContext.default().invoke_full(GLib.PRIORITY_DEFAULT_IDLE, self.emit_event, (event, message))

    def add_listener(self, function: Callable[[str, object], None]):
        self._listeners.append(function)

    def destroy_listeners(self):
        self._listeners = []
