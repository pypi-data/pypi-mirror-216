from gi.repository import Gtk, Gdk, GdkPixbuf, GLib

import logging

from time import sleep

import time

from OpenRadio.core.ModuleClass import ModuleClass
from OpenRadio.core.Localizer import ModuleLocalizer

DOMAIN = "builtin.clock"

localizer = ModuleLocalizer(DOMAIN)
translator = localizer.get_translator()
_ = translator.gettext

MODULE_CLASS_NAME = "ClockModule"

format_map = {
    (True, True): "%H:%M:%S",
    (True, False): "%H:%M",
    (False, True): "%I:%M:%S %p",
    (False, False): "%I:%M %p",
}


# Simple module to show the clock
class ClockModule(ModuleClass):
    # Some parts of this code originates from https://gist.github.com/olisolomons/b7b924628881a044638e68adb6982fd1. A few changes were made to improve compatibility.
    NAME = "Clock"
    DOMAIN = DOMAIN

    USES_GUI = True
    USES_HTTP = False
    USES_CONFIG = True
    USES_FAVORITES = False

    def __init__(self):
        self.ICON = self.core.IconHelper.get_icon("globe-symbolic")
        self.show_seconds = True
        self.metric_time = True

    def return_to_main_menu(self, widget, ignore=None):
        self.on_clear()
        self.core.Window.show_menu()

    def return_settings(self, button, settings, switch_seconds, switch_hour):
        if switch_seconds.get_active():
            self.show_seconds = True
        else:
            self.show_seconds = False

        if switch_hour.get_active():
            self.metric_time = True
        else:
            self.metric_time = False

        config = self.core.Settings.get_config(self.DOMAIN)

        config["show_seconds"] = self.show_seconds
        config["metric_time"] = self.metric_time

        self.core.Settings.save_config(self.DOMAIN, config)

        self.config_box.destroy()
        settings.show_settings()

    def update_time(self):
        if self.quit:
            return False

        time_format = format_map[(self.metric_time, self.show_seconds)]
        time_text = time.strftime(time_format)

        self.clock.set_text(time_text)

        return True

    def on_quit(self, ignore=None):
        self.quit = True

    def on_clear(self):
        self.quit = True

        self.style_context.remove_provider_for_screen(self.screen, self.provider)

        self.button.destroy()

        self.core.Window.disconnect(self.exit_signal_id)

    def on_config(self, settings):
        show_seconds_label = Gtk.Label(label=_("Show seconds:"))
        show_seconds = Gtk.Switch()

        seconds_grid = Gtk.Grid()
        seconds_grid.attach(show_seconds_label, 0, 0, 1, 1)
        seconds_grid.attach(show_seconds, 1, 0, 1, 1)
        seconds_grid.set_halign(Gtk.Align.CENTER)

        hour_label = Gtk.Label(label=_("Metric time:"))
        hour_switch = Gtk.Switch()

        hour_grid = Gtk.Grid()
        hour_grid.attach(hour_label, 0, 0, 1, 1)
        hour_grid.attach(hour_switch, 1, 0, 1, 1)
        hour_grid.set_halign(Gtk.Align.CENTER)

        if self.show_seconds:
            show_seconds.set_active(True)
        if self.metric_time:
            hour_switch.set_active(True)

        back_button = self.core.UIHelper.back_button(
            self.return_settings, settings, show_seconds, hour_switch
        )
        back_button.set_vexpand(False)
        back_button.set_hexpand(False)

        back_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        back_box.pack_start(back_button, False, False, 0)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.pack_start(back_box, False, False, 5)
        main_box.pack_start(seconds_grid, False, False, 5)
        main_box.pack_start(hour_grid, False, False, 5)

        self.core.Window.add(main_box)
        self.core.Window.show_all()

        self.config_box = main_box

    def on_show(self):
        self.quit = False

        config = self.core.Settings.get_config(self.DOMAIN)

        self.show_seconds = config.get("show_seconds", False)
        self.metric_time = config.get("metric_time", False)

        self.exit_signal_id = self.core.Window.connect(
            "key-press-event", self.return_to_main_menu
        )

        self.screen = Gdk.Screen.get_default()
        self.provider = Gtk.CssProvider()
        self.style_context = Gtk.StyleContext()

        self.style_context.add_provider_for_screen(
            self.screen, self.provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        css = b"""
        #clock_label {
            font-size: 500%;
        }
        """
        self.provider.load_from_data(css)

        self.grid = Gtk.Grid()

        self.clock = Gtk.Label()
        self.clock.set_name("clock_label")
        self.clock.set_hexpand(True)
        self.clock.set_vexpand(True)

        self.update_time()

        self.grid.attach(self.clock, 0, 0, 1, 1)

        self.button = Gtk.Button()
        self.button.add(self.grid)
        self.button.connect("clicked", self.return_to_main_menu)

        self.core.Window.add(self.button)

        self.core.Window.show_all()

        GLib.timeout_add(500, self.update_time)
