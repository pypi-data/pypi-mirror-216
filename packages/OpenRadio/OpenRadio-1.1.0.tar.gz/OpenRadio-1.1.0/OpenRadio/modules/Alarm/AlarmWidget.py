from gi.repository import Gtk, Gdk
from .TimeWidget import TimeWidget
from OpenRadio.core.Localizer import ModuleLocalizer

localizer = ModuleLocalizer("builtin.alarm")
translator = localizer.get_translator()
_ = translator.gettext


# Widget for alarm configuration
class AlarmWidget(Gtk.ScrolledWindow):
    favorite_map = {}

    def __init__(
        self,
        back_callback: callable,
        core: callable,
        remove_callback: callable,
        metric_time: bool,
        can_delete: bool = False,
        weekdays: list = [],
        favorite: str | None = None,
        minutes: int = 0,
        hours: int = 0,
        name: str = "",
        enabled: bool = False,
    ):
        self.core = core

        super().__init__()
        self.set_policy(Gtk.PolicyType.NEVER,Gtk.PolicyType.AUTOMATIC)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.weekday_to_name = [
            _("Monday"),
            _("Tuesday"),
            _("Wednesday"),
            _("Thursday"),
            _("Friday"),
            _("Saturday"),
            _("Sunday"),
        ]

        self._load_css()

        back_button = self.core.UIHelper.back_button(self._exit, back_callback, self)

        time_widget = TimeWidget(hours, minutes, metric_time)

        favorites_combo_box = Gtk.ComboBoxText()
        self.add_favorites_combobox(favorites_combo_box, favorite)

        if len(self.favorite_map) == 0:
            favorites_combo_box.set_sensitive(False)

        favorites_combo_box.set_size_request(10, -1)

        favorites_frame = Gtk.Frame(label=_("Favorite"))
        favorites_frame.add(favorites_combo_box)
        favorites_frame.set_margin_left(10)
        favorites_frame.set_margin_right(10)

        weekday_buttons = []
        weekday_box = Gtk.FlowBox()
        weekday_box.set_min_children_per_line(2)
        weekday_box.set_halign(Gtk.Align.CENTER)
        weekday_box.set_vexpand(False)
        weekday_box.set_selection_mode(Gtk.SelectionMode.NONE)

        for x, day in enumerate(self.weekday_to_name):
            radio_button = Gtk.CheckButton(label=day)
            weekday_buttons.append(radio_button)
            weekday_box.add(radio_button)
            if x in weekdays:
                radio_button.set_active(True)

        weekday_frame = Gtk.Frame(label=_("Repeat"))
        weekday_frame.add(weekday_box)
        weekday_frame.set_margin_left(10)
        weekday_frame.set_margin_right(10)

        name_entry = Gtk.Entry()
        name_entry.set_text(name)

        name_frame = Gtk.Frame(label=_("Name"))
        name_frame.add(name_entry)
        name_frame.set_margin_left(10)
        name_frame.set_margin_right(10)

        info_label = Gtk.Label()

        enable_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        enable_switch = Gtk.Switch()

        if enabled:
            enable_switch.set_state(True)

        enable_label = Gtk.Label(_("Enable"))
        enable_box.pack_start(enable_label, False, False, 1)
        enable_box.pack_end(enable_switch, False, False, 1)
        enable_box.set_margin_left(10)
        enable_box.set_margin_right(10)

        if can_delete:
            delete_button = self.core.UIHelper.simple_button(
                remove_callback, "user-trash-symbolic", None, name
            )

        control_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        control_box.pack_start(back_button, False, False, 1)

        if can_delete:
            control_box.pack_end(delete_button, False, False, 1)

        additional_settings_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        additional_settings_frame = Gtk.Frame(label=_("Additional Settings"))

        additional_settings_frame.set_shadow_type(Gtk.ShadowType.OUT)

        additional_settings_box.pack_start(enable_box, False, False, 10)
        additional_settings_box.pack_start(name_frame, False, False, 10)
        additional_settings_box.pack_start(favorites_frame, False, False, 10)
        additional_settings_box.pack_start(weekday_frame, False, False, 10)

        additional_settings_box.pack_start(info_label, False, False, 10)

        additional_settings_frame.add(additional_settings_box)
        additional_settings_frame.set_margin_left(50)
        additional_settings_frame.set_margin_right(50)

        box.pack_start(control_box, False, False, 4)
        box.pack_start(time_widget, False, False, 4)
        box.pack_start(additional_settings_frame, False, False, 4)

        self.add(box)

        self.inital_name = name

        self.name_entry = name_entry
        self.weekday_buttons = weekday_buttons
        self.favorite = favorites_combo_box
        self.time_widget = time_widget
        self.info_label = info_label
        self.enable_switch = enable_switch

    def _load_css(self):
        self.screen = Gdk.Screen.get_default()
        self.provider = Gtk.CssProvider()
        self.style_context = Gtk.StyleContext()

        self.style_context.add_provider_for_screen(
            self.screen, self.provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        css = b"""
        #time_seperator {
            font-size: 300%;
        }
        #hours,#minutes {
            font-size: 300%;
        }
        """
        self.provider.load_from_data(css)

    def _exit(self, button, back_callback, *args):
        back_callback(*args)

    def remove_css(self):
        self.style_context.remove_provider_for_screen(self.screen, self.provider)

    def get_hours(self):
        return self.time_widget.get_hours()

    def get_minutes(self):
        return self.time_widget.get_minutes()

    def get_weekdays(self):
        active_weekdays = []
        for x, button in enumerate(self.weekday_buttons):
            if button.get_active():
                active_weekdays.append(x)
        return active_weekdays

    def get_name(self):
        return self.name_entry.get_text()

    def get_favorite(self):
        active_index = self.favorite.get_active_id()
        if active_index == None:
            return None

        return self.favorite_map.get(int(active_index), None)

    def get_inital_name(self):
        return self.inital_name

    def set_info(self, text):
        self.info_label.set_text(text)
        self.info_label.show()

    def get_enabled(self):
        return self.enable_switch.get_active()

    def add_favorites_combobox(
        self, combobox: Gtk.ComboBoxText, selected_favorite: str | None
    ) -> bool:
        favorite_module_domains = self.core.ModuleHandler.get_modules_by_tags(
            ["USES_FAVORITES"]
        )
        self.favorite_map = {}

        index = 0  # A bit hacky but works ¯\_(ツ)_/¯
        selected_index = "-1"  # Default to -1 if not found

        for module_domain in favorite_module_domains:
            module = self.core.ModuleHandler.get_module_by_domain(module_domain)
            module_favorites = module.on_get_favorites()

            for x, module_favorite in enumerate(module_favorites):
                combobox.append(str(index), module_favorite)
                if module_favorite == selected_favorite:
                    selected_index = str(index)
                self.favorite_map[index] = (
                    module_domain,
                    module_favorite,
                    module_favorites[module_favorite],
                )
                index += 1
        combobox.set_active_id(selected_index)
