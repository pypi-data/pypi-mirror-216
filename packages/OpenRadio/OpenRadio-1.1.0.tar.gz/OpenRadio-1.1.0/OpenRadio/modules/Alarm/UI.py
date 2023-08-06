from gi.repository import Gtk, GdkPixbuf, GLib, Gdk
from .AlarmWidget import AlarmWidget
from datetime import time
from .const import DOMAIN
from OpenRadio.core.Localizer import ModuleLocalizer

localizer = ModuleLocalizer(DOMAIN)
translator = localizer.get_translator()
_ = translator.gettext


# Class handling the UI for the Alarm module
class UI:
    def __init__(self, parent):
        self.parent = parent
        self.core = parent.core
        self.alarm_scheduler = parent.alarm_scheduler
        self.container = None
        self.metric_time = self.parent.get_metric_time()

    def clear_window(self):
        if self.container:
            self.container.destroy()
            self.container = None

    def on_return(self, *ignore):
        self.clear_window()

        self.parent._return()

    def remove_alarm(self, button, name):
        self.alarm_scheduler.remove_alarm(name)
        self.show_main()

    def save_alarm(self, alarm_widget):
        name = alarm_widget.get_name()
        hours = alarm_widget.get_hours()
        minutes = alarm_widget.get_minutes()
        favorite = alarm_widget.get_favorite()
        weekdays = alarm_widget.get_weekdays()
        inital_name = alarm_widget.get_inital_name()
        enabled = alarm_widget.get_enabled()

        if not self.check_alarm_name(name):
            alarm_widget.set_info(_("Name forbidden"))
            return

        if inital_name != name:
            self.alarm_scheduler.remove_alarm(inital_name)

        if favorite == None:
            favorite_domain = None
            favorite_args = None
            favorite_name = None
        else:
            favorite_domain, favorite_name, favorite_args = favorite

        self.alarm_scheduler.save_alarm(
            name,
            minutes,
            hours,
            weekdays,
            favorite_domain,
            favorite_name,
            favorite_args,
            enabled,
        )

        alarm_widget.remove_css()

        self.show_main()

    # This should be extended if more broken names are found
    def check_alarm_name(self, name):
        if len(name) == 0:
            return False
        return True

    def configure_alarm(
        self,
        button: Gtk.Button,
        alarm_name: str,
        can_delete=False,
        weekdays: list = [],
        favorite: str | None = None,
        minutes: int = 0,
        hours: int = 0,
        enabled: bool = False,
    ) -> None:
        self.clear_window()

        alarm_widget = AlarmWidget(
            self.save_alarm,
            self.core,
            self.remove_alarm,
            self.metric_time,
            can_delete,
            weekdays,
            favorite,
            minutes,
            hours,
            alarm_name,
            enabled,
        )

        self.container = alarm_widget

        self.core.Window.add(alarm_widget)
        self.core.Window.show_all()

    def add_alarm(self, button):
        new_alarm_name = _("Alarm ") + str(len(self.alarm_scheduler.get_alarms()))

        self.configure_alarm(None, new_alarm_name)
        pass

    def add_alarms(self, box: Gtk.Box):
        alarms = self.alarm_scheduler.get_alarms()

        for alarm_name in alarms:
            alarm = alarms[alarm_name]
            alarm_label = Gtk.Label(label=alarm_name)
            alarm_button = Gtk.Button()
            alarm_button.add(alarm_label)

            alarm_button.connect(
                "clicked",
                self.configure_alarm,
                alarm_name,
                True,
                alarm.get("weekdays", []),
                alarm.get("favorite_name", None),
                alarm.get("minutes", 0),
                alarm.get("hours", 0),
                alarm.get("enabled", False),
            )
            box.pack_start(alarm_button, False, False, 1)

    def return_settings(self, button, settings, hour_switch):
        if hour_switch.get_active():
            self.metric_time = True
        else:
            self.metric_time = False

        self.config_box.destroy()

        self.parent.set_metric_time(self.metric_time)
        settings.show_settings()

    def show_config(self, settings):
        hour_label = Gtk.Label(label=_("Metric time:"))
        hour_switch = Gtk.Switch()

        hour_grid = Gtk.Grid()
        hour_grid.attach(hour_label, 0, 0, 1, 1)
        hour_grid.attach(hour_switch, 1, 0, 1, 1)
        hour_grid.set_halign(Gtk.Align.CENTER)

        if self.metric_time:
            hour_switch.set_active(True)

        back_button = self.core.UIHelper.back_button(
            self.return_settings, settings, hour_switch
        )
        back_button.set_vexpand(False)
        back_button.set_hexpand(False)

        back_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        back_box.pack_start(back_button, False, False, 0)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.pack_start(back_box, False, False, 5)
        main_box.pack_start(hour_grid, False, False, 5)

        self.core.Window.add(main_box)
        self.core.Window.show_all()

        self.config_box = main_box

    def show_main(self, *ignore):
        self.clear_window()

        alarm_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.add_alarms(alarm_box)

        alarm_scrolled = Gtk.ScrolledWindow()
        alarm_scrolled.add(alarm_box)

        control_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        back_button = self.core.UIHelper.back_button(self.on_return)
        add_button = self.core.UIHelper.simple_button(
            self.add_alarm, "list-add-symbolic", None
        )

        control_box.pack_start(back_button, False, False, 1)
        control_box.pack_end(add_button, False, False, 1)

        main_box.pack_start(control_box, False, False, 1)
        main_box.pack_start(alarm_scrolled, True, True, 1)

        self.container = main_box

        self.core.Window.add(main_box)
        self.core.Window.show_all()
