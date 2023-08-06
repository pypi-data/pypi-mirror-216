# Implementing the base class
class ModuleClass:
    ICON = None
    DOMAIN = None
    NAME = None

    USES_GUI = False
    USES_CONFIG = False
    USES_HTTP = False
    USES_FAVORITES = False

    ENABLED = True

    def on_show(self):
        # Window to show when 'opened'
        pass

    def on_get_favorites(self):
        # Should return a dict in format : {"Favorite name": (arg1,arg2,...)}
        pass

    def on_play_favorite(self, on_done, on_error, *args):
        # Starts playing a favorite on_done/on_error should be called when the favorite finished/produced and error.
        # Returning False will automatically assume error
        pass

    def on_stop_favorite(self, *args):
        # Stop a favorite from playing
        pass

    def on_http(self, path, data, handler):
        # Do something with the http request
        # Return a dict in format : {"response": <data to send to client>, "response_code": <Http status code>, "content_type": "Content Type of response"}
        pass

    def on_config(self, setting):
        # Window to show for configuration
        pass

    def on_clear(self):
        # Clear window no mather what
        pass

    def on_quit(self):
        # Called when app gets closed
        pass
