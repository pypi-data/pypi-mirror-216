from . import (
    Settings,
    HTTPApi,
    AudioPlayer,
    IconHelper,
    ModuleHandler,
    Window,
    UIHelper,
)
from gi.repository import Gtk


# Core class containing all core functionality
class Core:
    def __init__(self, **kwargs):
        self.Settings = Settings.Settings()  # Needed by almost all modules
        self.IconHelper = IconHelper.IconHelper(self)
        self.UIHelper = UIHelper.UIHelper(self)
        self.HTTPApi = HTTPApi.HTTPApi(self)
        self.AudioPlayer = AudioPlayer.AudioPlayer(self)
        self.ModuleHandler = ModuleHandler.ModuleHandler(self)
        self.Window = Window.Window(self, **kwargs)

    def quit(self, exit_code):
        for module in self.ModuleHandler.get_all_modules().values():
            module.on_quit()
        self.HTTPApi.on_quit()
        Gtk.main_quit()
        if not isinstance(exit_code, int):
            exit_code = 0
        exit(exit_code)
