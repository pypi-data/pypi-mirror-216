from OpenRadio.core.ModuleClass import ModuleClass
from gi.repository import Gtk, GLib
import html
from datetime import datetime

size_fmt_time = """<span size="500%" >{}</span>"""
size_fmt_name = """<span size="200%" >{}</span>"""
size_fmt_stop = """<span size="200%" >{}</span>"""


# Widget while Ringing
class RingUI:
    def __init__(self, parent):
        self.parent = parent
        self.core = parent.core
        self.container = None
        self.exit = False
        self.ringing = False
        self.playing_module = None

    def cleanup(self):
        self.exit = True
        self.ringing = False
        if self.container:
            self.container.destroy()
            self.container = None

    def on_done(self, button, *args):
        self.cleanup()
        if self.playing_module:
            self.playing_module.on_stop_favorite(*args)
        self.core.Window.show_previous_module()

    def on_error(self, *ignore):
        self.cleanup()
        self.core.Window.show_previous_module()

    def update_time(self, label):
        if self.exit:
            return False
        current_time = datetime.now()

        if self.parent.get_metric_time():
            time_str = current_time.strftime("%H:%M")
        else:
            time_str = current_time.strftime("%I:%M")
        label.set_markup(size_fmt_time.format(time_str))
        label.show()
        return True

    def play_module(self, alarm_name, module: ModuleClass, *args):
        self.exit = False

        if self.ringing:
            return False

        self.ringing = True

        name_escaped = html.escape(alarm_name)
        grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        time_label = Gtk.Label()
        time_label.set_margin_top(50)
        time_label.set_vexpand(False)
        time_label.set_hexpand(True)
        time_label.set_halign(Gtk.Align.CENTER)
        time_label.set_valign(Gtk.Align.START)

        name_label = Gtk.Label()
        name_label.set_markup(size_fmt_name.format(name_escaped))
        name_label.set_vexpand(True)
        name_label.set_hexpand(True)
        name_label.set_halign(Gtk.Align.CENTER)
        name_label.set_valign(Gtk.Align.START)

        stop_label = Gtk.Label()
        stop_label.set_markup(size_fmt_stop.format("Stop"))

        stop_button = Gtk.Button()
        stop_button.connect("clicked", self.on_done, *args)
        stop_button.add(stop_label)
        stop_button.set_margin_bottom(50)
        stop_button.set_margin_top(50)
        stop_button.set_halign(Gtk.Align.CENTER)
        stop_button.set_valign(Gtk.Align.END)

        grid.attach(time_label, 1, 0, 1, 1)
        grid.attach(name_label, 1, 1, 1, 1)
        grid.attach(stop_button, 1, 3, 1, 1)
        self.update_time(time_label)
        GLib.timeout_add(1000, self.update_time, time_label)
        self.container = grid

        self.playing_module = module

        error = module.on_play_favorite(self.on_done, self.on_error, *args)
        if error:
            self.core.Window.show_previous_module()
            return
        self.core.Window.add(grid)
        self.core.Window.show_all()
        return
