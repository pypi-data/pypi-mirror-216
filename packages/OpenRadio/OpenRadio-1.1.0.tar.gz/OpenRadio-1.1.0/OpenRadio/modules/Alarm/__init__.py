from gi.repository import Gtk, GdkPixbuf, GLib, Gdk
from OpenRadio.core.ModuleClass import ModuleClass
from OpenRadio.core.const import LOG_LEVEL, LOG_HANDLER
import logging
from .TimeWidget import TimeWidget
from .AlarmScheduler import AlarmScheduler
from .UI import UI
from .const import DOMAIN

MODULE_CLASS_NAME = "Alarm"

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOG_LEVEL)
LOGGER.addHandler(LOG_HANDLER)


# Alarm main class
class Alarm(ModuleClass):
    NAME = "Alarm"
    DOMAIN = DOMAIN

    USES_GUI = True
    USES_HTTP = False
    USES_CONFIG = True
    USES_FAVORITES = False

    ENABLED = True

    def __init__(self):
        self.ICON = self.core.IconHelper.get_icon("alarm-symbolic", force_backup=True)
        self.alarm_scheduler = AlarmScheduler(self)
        self.UI = UI(self)

    def _return(self):
        self.core.Window.show_menu()

    def set_metric_time(self, metric_time):
        config = self.core.Settings.get_config(self.DOMAIN)
        config["metric_time"] = metric_time
        self.core.Settings.save_config(self.DOMAIN, config)

    def get_metric_time(self):
        config = self.core.Settings.get_config(self.DOMAIN)
        return config.get("metric_time", True)

    def on_config(self, settings):
        self.UI.show_config(settings)

    def on_show(self):
        self.UI.show_main()

    def on_clear(self):
        self.UI.clear_window()
