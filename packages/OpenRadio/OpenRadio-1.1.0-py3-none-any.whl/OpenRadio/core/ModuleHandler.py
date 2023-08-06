from .const import *
import logging
import os
from importlib import import_module
from gi.repository import Gtk

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOG_LEVEL)
LOGGER.addHandler(LOG_HANDLER)


# Loads, parses and sorts modules
class ModuleHandler:
    modules = {}

    def __init__(self, core):
        for module_dir in os.listdir(MODULE_PATH_PREFIX):
            self.core = core

            current_module = import_module("OpenRadio.modules." + module_dir)

            if "MODULE_CLASS_NAME" not in current_module.__dict__:
                LOGGER.error("Module doesn't have MODULE_CLASS_NAME.")
                Gtk.main_quit()
                exit(1)

            if (
                current_module.__dict__["MODULE_CLASS_NAME"]
                not in current_module.__dict__
            ):
                LOGGER.error("Module doesn't have class specified in MODULE_CLASS_NAME")
                Gtk.main_quit()
                exit(1)

            module_class = current_module.__dict__[current_module.MODULE_CLASS_NAME]
            module_class.core = core
            module = module_class()

            if not self._validate_module(module):
                Gtk.main_quit()
                exit(1)

            self.modules[module.DOMAIN] = module

    # Check for required tags and variables
    def _validate_module(self, module):
        if module.NAME == None:
            LOGGER.error(
                f"Module {module.__module__} doesn't have the NAME variable set. Exiting."
            )
            return False

        if module.DOMAIN == None:
            LOGGER.error(
                f"Module {module.__module__} doesn't have the DOMAIN variable set. Exiting."
            )
            return False

        if not module.USES_GUI and not module.USES_CONFIG:
            return True

        if module.ICON == None:
            LOGGER.error(
                f"Module {module.__module__} doesn't have the ICON variable set or the icon is nonexistent. Exiting."
            )
            return False

        return True

    # Sorts modules by module_order
    def _sort(self, module_domains: list):
        module_order = self.core.Settings.get_config("core").get("module_order", [])
        sorted_list = []
        for module_domain in module_order:
            if module_domain in module_domains:
                module_domains.remove(module_domain)
                sorted_list.append(module_domain)
        sorted_list.extend(module_domains)
        return sorted_list

    # Returns all modules
    def get_all_modules(self) -> dict:
        return self.modules

    # Get module by domain
    def get_module_by_domain(self, domain: str):
        if domain not in self.modules:
            return None
        return self.modules[domain]

    # Get modules by tags provided as list
    def get_modules_by_tags(self, tags: list, sort: bool = False) -> dict:
        previous_modules = self.get_all_modules().keys()
        matched = []
        for tag in tags:
            matched = []
            for module_domain in previous_modules:
                module = self.get_module_by_domain(module_domain)

                if getattr(module, tag, None):
                    matched.append(module_domain)
            previous_modules = matched

        if sort:
            sorted = self._sort(matched)
            return sorted
        return matched
