from gi.repository import Gtk, GdkPixbuf, GLib, Gdk
from .const import DEFAULT_ICON_SIZE


class UIHelper:
    def __init__(self, core):
        self.core = core
        pass

    def _delete_entry(self, entry):
        entry.destroy()

    def _favorite_callback(self, toggle_button, on_add, on_remove, *args):
        if toggle_button.get_active():
            callback = on_add

            toggle_button.foreach(self._delete_entry)
            favorite_image = self.core.IconHelper.get_icon(
                "star", size=DEFAULT_ICON_SIZE
            )
        else:
            callback = on_remove

            toggle_button.foreach(self._delete_entry)
            favorite_image = self.core.IconHelper.get_icon(
                "star-outline", size=DEFAULT_ICON_SIZE
            )

        callback(*args)

        toggle_button.add(favorite_image)
        toggle_button.show_all()

    # Generates button with a star or star outline also handles changing icon
    def favorite_button(
        self, on_add: callable, on_remove: callable, active: bool, *args
    ) -> tuple:
        favorite_button = Gtk.ToggleButton()

        if active:
            favorite_image = self.core.IconHelper.get_icon(
                "star", size=DEFAULT_ICON_SIZE
            )
        else:
            favorite_image = self.core.IconHelper.get_icon(
                "star-outline", size=DEFAULT_ICON_SIZE
            )

        favorite_button.set_active(active)

        favorite_button.add(favorite_image)
        favorite_button.connect(
            "toggled", self._favorite_callback, on_add, on_remove, *args
        )

        return (favorite_button, favorite_image)

    # A simple button with image
    def simple_button(
        self,
        callback: callable,
        icon_name: str,
        icon_size: int | Gtk.IconSize | None,
        *args,
    ) -> Gtk.Button:
        if icon_size == None:
            icon_size = Gtk.IconSize.MENU

        back_arrow = self.core.IconHelper.get_icon(icon_name, size=icon_size)
        go_back_button = Gtk.Button()
        go_back_button.add(back_arrow)
        go_back_button.connect("clicked", callback, *args)

        return go_back_button

    # A wrapper around simple button to generate a back button
    def back_button(self, callback: callable, *args) -> Gtk.Button:
        button = self.simple_button(callback, "go-previous-symbolic", None, *args)
        return button

    # Generates a grid with a markup label and a button to go back
    def error_message(self, message_markup: str, return_callback: callable) -> Gtk.Grid:
        go_back_button = self.back_button(return_callback)

        error_label = Gtk.Label()
        error_label.set_markup(message_markup)
        error_label.set_vexpand(True)
        error_label.set_hexpand(True)

        grid = Gtk.Grid()
        grid.attach(go_back_button, 0, 0, 1, 1)
        grid.attach(error_label, 1, 1, 1, 1)

        return grid
