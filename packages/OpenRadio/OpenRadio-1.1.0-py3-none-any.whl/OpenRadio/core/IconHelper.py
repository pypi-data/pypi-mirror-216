from .const import BACKUP_ICONS, DEFAULT_ICON_SIZE, LOG_LEVEL, LOG_HANDLER
import logging
from gi.repository import Gtk, GdkPixbuf
import os
import os.path as path

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOG_LEVEL)
LOGGER.addHandler(LOG_HANDLER)


# Helper for retrieving Icons
class IconHelper:
    def __init__(self, core):
        self.core = core

    def _get_force_backup(self):
        config = self.core.Settings.get_config("core")
        return config.get("force_backup", False)

    def _set_force_backup(self, state):
        config = self.core.Settings.get_config("core")
        config["force_backup"] = state
        return self.core.Settings.save_config("core", config)

    def _get_backup_icon(self, name, size, subdir=""):
        icon_search_path = os.path.join(BACKUP_ICONS, subdir)
        icon = Gtk.Image()

        width, height = size, size

        if isinstance(size, Gtk.IconSize):
            exists, width, height = Gtk.IconSize.lookup(size)

        for path in os.listdir(icon_search_path):
            file_name = os.path.splitext(path)[0]
            if file_name == name:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    os.path.join(icon_search_path, path), width, height, True
                )
                icon.set_from_pixbuf(pixbuf)
                break
        return icon

    def _get_theme_icon(self, name, size):
        default_size = Gtk.IconSize.MENU
        if type(size) == Gtk.IconSize:
            default_size = size

        icon = Gtk.Image.new_from_icon_name(name, size)

        if type(size) != Gtk.IconSize:
            icon.set_pixel_size(size)

        return icon

    def get_icon(
        self,
        name: str,
        size: int | Gtk.IconSize = DEFAULT_ICON_SIZE,
        backup_subdir: str = "",
        force_backup: bool = False,
    ) -> Gtk.Image:
        if self._get_force_backup():
            force_backup = True

        icon_theme = Gtk.IconTheme.get_default()

        if icon_theme.has_icon(name) and not force_backup:
            icon = self._get_theme_icon(name, size)
        else:
            icon = self._get_backup_icon(name, size, backup_subdir)
        return icon
