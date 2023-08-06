from scheduler import Scheduler
import scheduler.trigger as trigger

from datetime import datetime
from datetime import time

from gi.repository import GLib

from .RingUI import RingUI


# Schedules the alarms
class AlarmScheduler:
    schedule = Scheduler(n_threads=0)

    def __init__(self, parent):
        self.parent = parent
        self.core = parent.core
        self.scheduled_list = {}
        self.weekday_to_trigger = [
            trigger.Monday,
            trigger.Tuesday,
            trigger.Wednesday,
            trigger.Thursday,
            trigger.Friday,
            trigger.Saturday,
            trigger.Sunday,
        ]
        self.start()
        self.schedule_all()
        self.ring_ui = RingUI(parent)

    def _save_dict(self, name, alarm_dict):
        alarms = self.get_alarms()
        alarms[name] = alarm_dict
        self.save_alarms(alarms)

    # Show ring ui and start playing favorite
    def run_alarm(self, name, once):
        alarm = self.get_alarm(name)

        if once:
            self.disable_alarm(name)

        favorite_domain = alarm.get("favorite_domain", None)
        favorite_name = alarm.get("favorite_name", None)
        favorite_args = alarm.get("favorite_args", None)

        # Ignore if no favorite was set
        if not favorite_domain or not favorite_name:
            return
        module = self.core.ModuleHandler.get_module_by_domain(favorite_domain)

        if not module:
            # Do nothing if module was not found
            return
        self.core.Window.force_show(
            self.ring_ui.play_module, name, module, *favorite_args
        )

    # Check for job updates
    def check(self):
        self.schedule.exec_jobs()
        return True

    # Starts checking for alarms
    def start(self):
        self.check_id = GLib.timeout_add(
            1000, self.check
        )  # Check for updates every second

    # Converts weekday numbers to triggers
    def weekdays_to_trigger(self, weekdays, ring_time):
        result = []
        for weekday in weekdays:
            result.append(self.weekday_to_trigger[weekday](ring_time))
        return result

    # Schedules a new alarm
    def schedule_alarm(self, name, weekdays, minutes, hours, enabled):
        if not enabled:
            # Not enabled
            return

        alarm_time = time(minute=minutes, hour=hours)

        if len(weekdays) == 0:
            alarm_job = self.schedule.once(
                alarm_time,
                self.run_alarm,
                args=(
                    name,
                    True,
                ),
            )
            self.scheduled_list[name] = alarm_job
            return

        triggers = self.weekdays_to_trigger(weekdays, alarm_time)
        alarm_job = self.schedule.weekly(
            triggers,
            self.run_alarm,
            args=(
                name,
                False,
            ),
        )
        self.scheduled_list[name] = alarm_job

    # Reads config and adds alarms
    def schedule_all(self):
        all_alarms = self.get_alarms()

        for alarm_name in all_alarms:
            alarm = all_alarms[alarm_name]
            self.schedule_alarm(
                alarm_name,
                alarm.get("weekdays", None),
                alarm.get("minutes", None),
                alarm.get("hours", None),
                alarm.get("enabled", None),
            )

    # Removes an alarm from the queue
    def remove_alarm_from_queue(self, alarm_name):
        alarm_job = self.scheduled_list.get(alarm_name, None)
        if not alarm_job:
            return False
        self.schedule.delete_job(alarm_job)
        return True

    # Get specific alarm
    def get_alarm(self, name):
        all_alarms = self.get_alarms()
        requested = all_alarms.get(name, None)
        return requested

    # Save alarms to config
    def save_alarms(self, alarms):
        config = self.core.Settings.get_config(self.parent.DOMAIN)
        config["alarms"] = alarms
        self.core.Settings.save_config(self.parent.DOMAIN, config)

    # Get all alarms
    def get_alarms(self):
        config = self.core.Settings.get_config(self.parent.DOMAIN)
        return config.get("alarms", {})

    # Save single alarm to config
    def save_alarm(
        self,
        name,
        minutes,
        hours,
        weekdays,
        favorite_domain,
        favorite_name,
        favorite_args,
        enabled,
    ):
        self.schedule_alarm(name, weekdays, minutes, hours, enabled)
        alarm_dict = {
            "minutes": minutes,
            "hours": hours,
            "weekdays": weekdays,
            "favorite_domain": favorite_domain,
            "favorite_name": favorite_name,
            "favorite_args": favorite_args,
            "enabled": enabled,
        }
        self._save_dict(name, alarm_dict)

    # Disables alarm
    def disable_alarm(self, name):
        alarm = self.get_alarm(name)
        alarm["enabled"] = False
        self._save_dict(name, alarm)

    # Removes alarm
    def remove_alarm(self, name):
        alarms = self.get_alarms()
        if not alarms.get(name, False):
            return
        alarms.pop(name)

        self.save_alarms(alarms)

        self.remove_alarm_from_queue(name)
