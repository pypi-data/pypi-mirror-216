from gi.repository import Gtk
from datetime import datetime

from OpenRadio.core.Localizer import ModuleLocalizer

localizer = ModuleLocalizer("builtin.alarm")
translator = localizer.get_translator()
_ = translator.gettext


# Simple Widget for adjusting the time
class TimeWidget(Gtk.AspectFrame):
    def __init__(self, hours, minutes, metric_time):
        Gtk.AspectFrame.__init__(
            self, label=_("Time"), xalign=0.5, yalign=0.5, obey_child=True
        )

        self.metric_time = metric_time

        time_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        if metric_time:
            hours_button = Gtk.SpinButton.new_with_range(0, 23, 1)
        else:
            hours_button = Gtk.SpinButton.new_with_range(1, 12, 1)

        hours_button.set_orientation(Gtk.Orientation.VERTICAL)
        hours_button.set_name("hours")
        hours_button.set_value(hours)
        hours_button.set_size_request(125, 225)
        hours_button.set_wrap(True)

        hours_button.set_margin_left(10)
        hours_button.set_margin_right(10)
        hours_button.set_margin_bottom(10)
        hours_button.connect("output", self.show_zeros)

        minutes_button = Gtk.SpinButton.new_with_range(0, 59, 1)
        minutes_button.set_orientation(Gtk.Orientation.VERTICAL)
        minutes_button.set_name("minutes")
        minutes_button.set_value(minutes)
        minutes_button.set_size_request(125, 225)
        minutes_button.set_wrap(True)

        minutes_button.set_margin_left(10)
        minutes_button.set_margin_right(10)
        minutes_button.set_margin_bottom(10)
        minutes_button.connect("output", self.show_zeros)

        time_seperator = Gtk.Label(label=":")
        time_seperator.set_name("time_seperator")

        if not metric_time:
            hour_select = Gtk.ComboBoxText()
            hour_select.append_text("AM")
            hour_select.append_text("PM")
            hour, pm = self.convert_to_12_hour(hours)

            if pm:
                hour_select.set_active(1)
            else:
                hour_select.set_active(0)

            hours_button.set_value(hour)

            hour_select.set_margin_bottom(100)
            hour_select.set_margin_top(100)
            self.hour_select = hour_select

        time_box.pack_start(hours_button, False, False, 2)
        time_box.pack_start(time_seperator, False, False, 2)
        time_box.pack_start(minutes_button, False, False, 2)

        if not metric_time:
            time_box.pack_start(hour_select, False, False, 2)

        self.add(time_box)

        self.hours_button = hours_button
        self.minutes_button = minutes_button

    def show_zeros(self, spinbutton):
        adjustment = spinbutton.get_adjustment()
        spinbutton.set_text("{:02d}".format(int(adjustment.get_value())))
        return True

    def convert_to_24_hour(self, hour, is_pm):
        if is_pm == 1 and hour != 12:
            hour += 12
        elif is_pm == 1 and hour == 12:
            hour = 0
        return hour

    def convert_to_12_hour(self, hour):
        is_pm = False
        if hour >= 12:
            is_pm = True
            if hour > 12:
                hour -= 12
        elif hour == 0:
            hour = 12
            is_pm = True
        return hour, is_pm

    def get_minutes(self):
        return int(self.minutes_button.get_value())

    def get_hours(self):
        selected_time = int(self.hours_button.get_value())
        actual_time = selected_time

        if not self.metric_time:
            actual_time = self.convert_to_24_hour(
                selected_time, self.hour_select.get_active()
            )
        return actual_time
