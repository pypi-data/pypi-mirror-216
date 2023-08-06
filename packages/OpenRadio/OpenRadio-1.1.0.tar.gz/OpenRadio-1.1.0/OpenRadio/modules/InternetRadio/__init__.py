import pyradios
from gi.repository import Gtk, GdkPixbuf, GLib

from OpenRadio.core.ModuleClass import ModuleClass
from OpenRadio.core.const import LOG_LEVEL, LOG_HANDLER, DEFAULT_ICON_SIZE
from OpenRadio.core.Localizer import ModuleLocalizer

from .UI import UI

from urllib.parse import urlparse

import logging


import socket

DOMAIN = "builtin.internetradio"

MODULE_CLASS_NAME = "InternetRadio"

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOG_LEVEL)
LOGGER.addHandler(LOG_HANDLER)


# Class implementing a simple internet radio
class InternetRadio(ModuleClass):
    NAME = "InternetRadio"
    DOMAIN = DOMAIN

    USES_GUI = True
    USES_CONFIG = False
    USES_HTTP = False
    USES_FAVORITES = True

    ENABLED = True

    def __init__(self):
        self.ICON = self.core.IconHelper.get_icon("applications-internet")

        self.browser = None

        self.UI = UI(self, LOGGER)

    def _return_error(self, button):
        self.error_grid.destroy()
        self.core.Window.show_menu()

    def _create_browser(self):
        try:
            browser = pyradios.RadioBrowser()
            self.browser = browser
        except socket.gaierror:
            self.browser = None

            return False
        return True

    def on_clear(self):
        self.browser = None
        self.UI._clean_up()

    def on_get_favorites(self):
        config = self.core.Settings.get_config(self.DOMAIN)
        return config

    def on_set_favorite(self, station):
        current_favorites = self.core.Settings.get_config(self.DOMAIN)
        current_favorites[f"""{station["name"]} ({self.NAME})"""] = [
            station["stationuuid"]
        ]
        self.core.Settings.save_config(self.DOMAIN, current_favorites)

    def on_remove_favorite(self, station):
        current_favorites = self.core.Settings.get_config(self.DOMAIN)
        current_favorites.pop(f"""{station["name"]} ({self.NAME})""")
        self.core.Settings.save_config(self.DOMAIN, current_favorites)

    def on_play_favorite(self, on_end, on_error, station_uuid):
        if not self.browser:
            internet = self._create_browser()
            if not internet:
                return True

        station = self.browser.station_by_uuid(station_uuid)[0]
        self.UI._play_station(
            None, station, is_gui=False, on_end=on_end, on_error=on_error
        )
        return False

    def on_stop_favorite(self, station_uuid):
        self.core.AudioPlayer.stop()

    def on_show(self):
        LOGGER.debug("Showing Main menu")
        if not self.browser:
            internet = self._create_browser()

            if not internet:
                grid = self.core.UIHelper.error_message(
                    "No Internet connection", self._return_error
                )

                self.core.Window.add(grid)
                self.core.Window.show_all()

                self.error_grid = grid
                return

        self.UI.show_main_menu()
