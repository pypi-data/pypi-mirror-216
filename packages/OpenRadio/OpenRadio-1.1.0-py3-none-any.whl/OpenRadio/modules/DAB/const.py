from OpenRadio.core.Localizer import ModuleLocalizer

DOMAIN = "builtin.dab"

localizer = ModuleLocalizer(DOMAIN)
translator = localizer.get_translator()
_ = translator.gettext

# Formats for various messages
size_fmt = """<span size="larger" weight="bold">{}</span>"""
status_done = size_fmt.format(_("Finished scanning DAB Channels"))
status_fmt = size_fmt.format(_("Scanning channel: {}"))
station_unusable = size_fmt.format(_("Station is unusable"))
waiting = size_fmt.format(_("Waiting for signal please be patient"))
playing = size_fmt.format(_("Playing:"))
error_fmt = size_fmt.format(_("An error occurred inside pysimpledab: {}: {}"))

favorite_fmt = "{} (DAB)"

title_fmt = size_fmt.format("{}")
