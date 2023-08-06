import gettext
import os
import logging
from .const import (
    CORE_LOCALS,
    MODULES_LOCALS,
    FALLBACK_LANGUAGE,
    CORE_NAME,
    LOG_LEVEL,
    LOG_HANDLER,
)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOG_LEVEL)
LOGGER.addHandler(LOG_HANDLER)


# A simple wrapper around gettext for ease of translation
class CoreLocalizer:
    def __init__(self):
        translator = gettext.translation(
            CORE_NAME, localedir=CORE_LOCALS, fallback=FALLBACK_LANGUAGE
        )
        self.translator = translator

    def get_translator(self):
        return self.translator


class ModuleLocalizer:
    def __init__(self, DOMAIN: str, MODULE_FALLBACK=None):
        if MODULE_FALLBACK == None:
            MODULE_FALLBACK = FALLBACK_LANGUAGE
        translator = gettext.translation(
            DOMAIN,
            localedir=os.path.join(MODULES_LOCALS, DOMAIN),
            fallback=MODULE_FALLBACK,
        )
        self.translator = translator

    def get_translator(self):
        return self.translator
