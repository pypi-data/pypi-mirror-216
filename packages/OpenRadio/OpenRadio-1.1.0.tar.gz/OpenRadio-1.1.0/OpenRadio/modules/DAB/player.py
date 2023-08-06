from gi.repository import Gtk
from OpenRadio.core.Localizer import ModuleLocalizer
from .const import DOMAIN

localizer = ModuleLocalizer(DOMAIN)
translator = localizer.get_translator()
_ = translator.gettext


# Class handling the playing of dab stations
class dab_player:
    def __init__(self, parent):
        self.parent = parent
        self.core = parent.core
        self.dab_helper = self.parent.dab_helper
        self.program_map = {}
        self.container = None
        self.gui_active = False

    def _delete_entry(self, entry):
        entry.destroy()

    def _reset_play_field(self):
        if self.gui_active:
            self.favorite_button.set_sensitive(False)
            self.favorite_button.set_active(False)
            self.dab_image.clear()
            self.dab_title.set_text("")

    def cleanup(self):
        if self.container:
            self.container.destroy()
            self.container = None
        if self.program_map:
            self.program_map = {}
        if self.gui_active:
            self.gui_active = False

    def return_menu(self, *ignore):
        self.cleanup()
        self.dab_helper.exit()
        self.core.Window.show_menu()

    def add_favorite(self):
        if not self.favorite_button.get_sensitive():
            return

        row = self.program_list.get_selected_row()

        band, channel, name = self.program_map[row]

        self.parent._add_favorite(band, channel, name)

    def remove_favorite(self):
        if not self.favorite_button.get_sensitive():
            return

        row = self.program_list.get_selected_row()

        band, channel, name = self.program_map[row]

        self.parent._remove_favorite(band, channel, name)

    def rescan(self, *ignore):
        self._reset_play_field()
        self.program_list.foreach(self._delete_entry)
        self.parent._clear_config()
        self.dab_helper.scan()

    def add_program(self, band, channel, name):
        program_list_label = Gtk.Label(label=name)
        program_list_row = Gtk.ListBoxRow()
        program_list_row.add(program_list_label)
        band_int = int(band)

        if (band_int, channel, name) in self.program_map.values():
            return False

        self.program_list.add(program_list_row)

        self.program_map[program_list_row] = (band_int, channel, name)

        self.core.Window.show_all()
        return True

    def add_saved_programs(self, stations):
        for station_name in stations:
            band, channel = stations[station_name]
            self.add_program(band, channel, station_name)

    def play_station(self, box, row):
        band, channel, name = self.program_map[row]

        self._reset_play_field()

        if self.parent._is_favorite(band, channel, name):
            self.favorite_button.set_active(True)

        self.favorite_button.set_sensitive(True)

        self.dab_helper.play_station(band, channel, name)

    def show_info(self, markup):
        self.info_label.set_markup(markup)
        return False

    def show_title(self, markup):
        self.dab_title.set_markup(markup)
        return False

    def show_image(self, pixbuf):
        self.dab_image.set_from_pixbuf(pixbuf)
        self.dab_image.show()
        return False

    def show_error(self, markup):
        go_back_button = self.core.UIHelper.back_button(self.return_menu)

        error_label = Gtk.Label()
        error_label.set_markup(markup)
        error_label.set_vexpand(True)
        error_label.set_hexpand(True)
        grid = Gtk.Grid()
        grid.attach(go_back_button, 0, 0, 1, 1)
        grid.attach(error_label, 1, 1, 1, 1)

        self.container = grid

        self.core.Window.add(grid)
        self.core.Window.show_all()

    def show_menu(self):
        self.cleanup()
        self.gui_active = True

        program_scrolled = Gtk.ScrolledWindow()

        self.program_list = Gtk.ListBox()
        self.program_list.connect("row-activated", self.play_station)

        program_scrolled.add(self.program_list)

        self.rescan_button = Gtk.Button(label=_("Rescan"))
        self.rescan_button.connect("clicked", self.rescan)
        self.rescan_button.set_hexpand(False)
        self.rescan_button.set_vexpand(False)

        self.dab_image = Gtk.Image()

        self.favorite_button, self.favorite_image = self.core.UIHelper.favorite_button(
            self.add_favorite, self.remove_favorite, False
        )
        self.favorite_button.set_sensitive(False)

        self.dab_title = Gtk.Label()
        self.dab_title.set_line_wrap(True)

        self.info_label = Gtk.Label()

        back_button = self.core.UIHelper.back_button(self.return_menu)

        VBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        HBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        control_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        dab_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        image_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        image_box.pack_start(self.dab_title, False, False, 1)
        image_box.pack_start(self.dab_image, True, True, 1)

        dab_box.pack_start(self.info_label, False, False, 1)
        dab_box.pack_start(program_scrolled, True, True, 1)
        dab_box.pack_start(self.rescan_button, False, False, 1)

        control_box.pack_start(back_button, False, False, 1)
        control_box.pack_end(self.favorite_button, False, False, 1)

        HBox.pack_start(dab_box, True, True, 1)
        HBox.pack_start(image_box, True, False, 1)

        VBox.pack_start(control_box, False, False, 1)
        VBox.pack_start(HBox, True, True, 1)

        self.container = VBox

        self.core.Window.add(VBox)
        self.core.Window.show_all()
