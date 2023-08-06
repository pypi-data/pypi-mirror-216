from OpenRadio.core.ModuleClass import ModuleClass
from OpenRadio.core.const import LOG_LEVEL, LOG_HANDLER

from gi.repository import Gtk

import logging

from OpenRadio.core.Localizer import ModuleLocalizer

DOMAIN = "builtin.core_settings"

localizer = ModuleLocalizer(DOMAIN)
translator = localizer.get_translator()
_ = translator.gettext

MODULE_CLASS_NAME = "CoreSettings"


# Module just for changing core settings
class CoreSettings(ModuleClass):
    NAME = "Core"
    DOMAIN = DOMAIN

    USES_GUI = False
    USES_HTTP = False
    USES_CONFIG = True

    def __init__(self):
        self.ICON = self.core.IconHelper.get_icon("emblem-system")
        self.selected_row = None

    def destroy_widget(self, widget):
        widget.destroy()

    def clear_container(self, container):
        container.foreach(self.destroy_widget)
        container.destroy()

    def save_list(self, list):
        config = self.core.Settings.get_config("core")
        config["module_order"] = list
        self.core.Settings.save_config("core", config)

    def save_fullscreen(self, state):
        config = self.core.Settings.get_config("core")
        config["fullscreen"] = state
        self.core.Settings.save_config("core", config)

    def get_fullscreen(self):
        config = self.core.Settings.get_config("core")
        return config.get("fullscreen", False)

    def save_http_port(self, port):
        http_config = self.core.Settings.get_config("core.httpapi")
        http_config["port"] = port
        self.core.Settings.save_config("core.httpapi", http_config)

    def save_force_backup_icons(self, switch):
        self.core.IconHelper._set_force_backup(switch.get_state())

    def show_settings(self, button, settings, listbox, http_entry, icon_switch):
        sorted_rows = listbox.get_children()
        sorted_list = []

        for row in sorted_rows:
            sorted_list.append(self.row_map[row])

        self.save_list(sorted_list)

        self.save_force_backup_icons(icon_switch)

        http_port = int(http_entry.get_text())
        self.save_http_port(http_port)

        listbox.foreach(self.clear_container)
        self.container.destroy()
        settings.show_settings()

    def move_up(self, button, listbox):
        row = self.selected_row
        if self.selected_row:
            index = listbox.get_children().index(self.selected_row)
            if index > 0:
                listbox.remove(row)
                listbox.insert(row, index - 1)
                listbox.select_row(row)
                self.selected_row = row

    def move_down(self, button, listbox):
        row = self.selected_row
        if row:
            index = listbox.get_children().index(row)
            if index < len(listbox.get_children()) - 1:
                listbox.remove(row)
                listbox.insert(row, index + 1)
                listbox.select_row(row)
                self.selected_row = row

    def row_selected(self, box, row):
        if not self.up_button.get_sensitive() or not self.down_button.get_sensitive():
            self.up_button.set_sensitive(True)
            self.down_button.set_sensitive(True)
        self.selected_row = row

    def module_order_box(self):
        modules = self.core.ModuleHandler.get_modules_by_tags(
            ["USES_GUI", "ENABLED"], sort=True
        )
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)

        listbox.connect("row-selected", self.row_selected)

        control_buttons = Gtk.Grid()

        up_button = self.core.UIHelper.simple_button(
            self.move_up, "go-up-symbolic", None, listbox
        )
        up_button.set_sensitive(False)

        down_button = self.core.UIHelper.simple_button(
            self.move_down, "go-down-symbolic", None, listbox
        )
        down_button.set_sensitive(False)

        self.up_button = up_button
        self.down_button = down_button

        control_buttons.attach(up_button, 0, 0, 1, 1)
        control_buttons.attach(down_button, 0, 1, 1, 1)
        control_buttons.set_valign(Gtk.Align.CENTER)

        self.row_map = {}

        for module_domain in modules:
            module = self.core.ModuleHandler.get_module_by_domain(module_domain)
            row = Gtk.ListBoxRow()
            module_grid = Gtk.Grid()
            module_image = module.ICON
            module_label = Gtk.Label(label=module.NAME)
            module_label.set_margin_left(10)
            module_grid.attach(module_image, 0, 0, 1, 1)
            module_grid.attach(module_label, 1, 0, 1, 1)
            row.add(module_grid)
            self.row_map[row] = module_domain
            listbox.add(row)

        list_scrolled = Gtk.ScrolledWindow()
        list_scrolled.add(listbox)
        list_scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        list_scrolled.set_margin_left(20)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(list_scrolled, True, True, 1)
        box.pack_start(control_buttons, False, False, 1)

        self.box = box
        return box, listbox

    def fullscreen_set(self, switch, state):
        if state:
            self.core.Window.fullscreen()
        else:
            self.core.Window.unfullscreen()

        self.save_fullscreen(state)

    def fullscreen_box(self):
        fullscreen_label = Gtk.Label(label=_("Fullscreen"))
        fullscreen_label.set_halign(Gtk.Align.START)

        fullscreen_switch = Gtk.Switch()

        if self.core.Window.FULLSCREEN:
            fullscreen_switch.set_state(True)

        fullscreen_switch.connect("state-set", self.fullscreen_set)

        fullscreen_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)

        fullscreen_box.pack_start(fullscreen_label, True, True, 0)
        fullscreen_box.pack_start(fullscreen_switch, False, False, 0)
        return fullscreen_box

    def http_port_box(self):
        http_port_label = Gtk.Label(label=_("HTTP Port"))
        http_port_label.set_halign(Gtk.Align.START)

        http_entry = Gtk.Entry()
        http_entry.set_text(str(self.core.HTTPApi.get_config_entry("port")))
        http_entry.set_alignment(1)

        http_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)

        http_box.pack_start(http_port_label, True, True, 0)
        http_box.pack_start(http_entry, False, False, 0)

        return http_box, http_entry

    def icon_box(self):
        icon_label = Gtk.Label(label=_("Only use backup icons"))
        icon_label.set_halign(Gtk.Align.START)

        icon_switch = Gtk.Switch()

        icon_switch.set_state(self.core.IconHelper._get_force_backup())

        icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)

        icon_box.pack_start(icon_label, True, True, 0)
        icon_box.pack_start(icon_switch, False, False, 0)

        return icon_box, icon_switch

    def general_settings(self):
        listbox = Gtk.ListBox()
        fullscreen_box = self.fullscreen_box()
        http_port_box, http_port_entry = self.http_port_box()
        icon_box, icon_switch = self.icon_box()

        listbox.add(fullscreen_box)
        listbox.add(icon_box)
        listbox.add(http_port_box)

        return listbox, http_port_entry, icon_switch

    def on_config(self, settings):
        module_order_box, listbox = self.module_order_box()
        general_settings_listbox, http_port_entry, icon_switch = self.general_settings()

        back_button = self.core.UIHelper.back_button(
            self.show_settings, settings, listbox, http_port_entry, icon_switch
        )
        back_button.set_halign(Gtk.Align.START)

        stack = Gtk.Stack()

        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(500)

        stack.add_titled(general_settings_listbox, "general", _("General"))
        stack.add_titled(module_order_box, "module_order", _("Module order"))

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        stack_switcher.set_halign(Gtk.Align.CENTER)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        vbox.pack_start(back_button, False, False, 0)
        vbox.pack_start(stack_switcher, False, True, 0)
        vbox.pack_start(stack, True, True, 0)

        self.container = vbox
        self.core.Window.add(vbox)
        self.core.Window.show_all()
