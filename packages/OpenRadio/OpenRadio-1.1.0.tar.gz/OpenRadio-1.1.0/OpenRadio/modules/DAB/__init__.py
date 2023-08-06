from gi.repository import Gtk, GdkPixbuf, GLib, Gdk

from OpenRadio.core.ModuleClass import ModuleClass
from OpenRadio.core.const import LOG_LEVEL, LOG_HANDLER, DEFAULT_ICON_SIZE

import logging
from time import sleep

import pysimpledab

from .dab_helper import dab_helper
from .player import dab_player

from .const import *


MODULE_CLASS_NAME = "DAB"

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOG_LEVEL)
LOGGER.addHandler(LOG_HANDLER)


# Class implementing DAB audio
class DAB(ModuleClass):
    NAME = "Dab"
    DOMAIN = DOMAIN

    USES_GUI = True
    USES_HTTP = False
    USES_CONFIG = False
    USES_FAVORITES = True

    ENABLED = True

    def __init__(self):
        self.dab_helper = dab_helper(self)
        self.player = dab_player(self)
        self.ICON = self.ICON = self.core.IconHelper.get_icon(
            "network-wireless-hotspot-symbolic"
        )
        self.container = None

    def _clear_config(self):
        self._save_config({})

    def _get_config(self):
        return self.core.Settings.get_config(self.DOMAIN)

    def _save_config(self, config):
        self.core.Settings.save_config(self.DOMAIN, config)

    def _save_scanned_station(self, band, channel, name):
        current_save = self._get_config()
        if not current_save.get("stations", False):
            current_save["stations"] = {}
        name_decoded = name
        current_save["stations"][str(name_decoded)] = [str(band), channel]
        self._save_config(current_save)
        return

    def _add_favorite(self, band, channel, name):
        current_save = self._get_config()
        if (
            not current_save.get("favorites", False)
            or type(current_save["favorites"]) is not list
        ):
            current_save["favorites"] = []

        current_save["favorites"].append((str(band), channel, name))
        self._save_config(current_save)

    def _is_favorite(self, band, channel, name):
        current_save = self._get_config()
        if not current_save.get("favorites", None):
            return False
        if [str(band), channel, name] in current_save["favorites"]:
            return True
        return False

    def _remove_favorite(self, band, channel, name):
        current_save = self._get_config()

        if (
            not current_save.get("favorites", False)
            or type(current_save["favorites"]) is not list
        ):
            current_save["favorites"] = []
            return False

        if (str(band), channel, name) not in current_save["favorites"]:
            return False
        current_save["favorites"].remove((str(band), channel, name))
        self._save_config(current_save)

    def _save_scanned_station(self, band, channel, name):
        current_save = self._get_config()
        if not current_save.get("stations", False):
            current_save["stations"] = {}
        name_decoded = name
        current_save["stations"][str(name_decoded)] = [str(band), channel]
        self._save_config(current_save)
        return

    def _add_program(self, band, channel, name):
        new = self.player.add_program(band, channel, name)
        if self.dab_helper.scanning and new:
            self._save_scanned_station(band, channel, name)

    def _update_scan_status(self, channel, done=False):
        if done:
            self.player.show_info(status_done)
        elif self.dab_helper.scanning:
            self.player.show_info(status_fmt.format(channel))

    def _show_info(self, markup):
        if self.player.gui_active:
            self.player.show_info(markup)

    def _set_dab_title(self, markup):
        if self.player.gui_active:
            self.player.show_title(title_fmt.format(markup))

    def _set_dab_image(self, pixbuf):
        if self.player.gui_active:
            self.player.show_image(pixbuf)

    def _rescan(self):
        self.dab_helper.scan()

    def on_get_favorites(self):
        config = self._get_config()
        favorites = config.get("favorites", [])
        favorite_dict = {}

        for favorite in favorites:
            # This just maps: name = band,channel,name
            favorite_dict[favorite[2] + " (DAB)"] = (
                favorite[0],
                favorite[1],
                favorite[2],
            )
        return favorite_dict

    def on_play_favorite(self, on_done, on_error, band, channel, name):
        self.player.gui_active = False
        try:
            self.dab_helper.start(pysimpledab.RTLSDR, pysimpledab.BAND_III, "5C")
        except Exception as ex:
            on_error()
            return
        self.dab_helper.play_station(int(band), channel, name)

    def on_stop_favorite(self, band, channel, name):
        self.dab_helper.exit()

    def on_show(self):
        try:
            self.dab_helper.start(pysimpledab.RTLSDR, pysimpledab.BAND_III, "5C")
        except Exception as ex:
            self.player.show_error(error_fmt.format(type(ex).__name__, ex.args[0]))
            return

        self.player.show_menu()
        config = self._get_config()
        if len(config.get("stations", [])) == 0:
            self.dab_helper.scan()
        else:
            self.player.add_saved_programs(config.get("stations"))

    def on_clear(self):
        self.dab_helper.exit()
        self.player.cleanup()

    def on_quit(self):
        self.dab_helper.exit()
        self.player.cleanup()
