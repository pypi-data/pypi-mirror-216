import pysimpledab

from time import sleep

import threading

from datetime import datetime

from .const import *

from gi.repository import GLib, GdkPixbuf

from ringbuf import RingBuffer

import ctypes
import pyaudio
import html

ring_buf = RingBuffer(format="<h", capacity=38400 * 2)

timeout = 10
sync_timeout = 7


# dab-cmdline callbacks
class dab_callbacks:
    def __init__(self, parent, dab_help):
        self.parent = parent
        self.dab_helper = dab_help
        self.synced = False

    def programname_callback(self, name, length, data):
        if self.dab_helper.scanning:
            GLib.idle_add(self.dab_helper.scan_thread.add_program, name)
        elif self.dab_helper.wait_for_start == name.decode("utf-8"):
            GLib.idle_add(
                self.dab_helper._start_playing, name
            )  # Let it run in the main thread
        return None

    def audioOut_callback(self, buffer, size, samplerate, stereo, data):
        py_buf = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_short * size)).contents
        ring_buf.push(py_buf)
        return None

    def dataOut_callback(self, label, ctx):
        escaped_text = html.escape(label.decode("utf-8"))
        GLib.idle_add(self.parent._set_dab_title, escaped_text)
        return None

    def bytesOut_callback(self, data, amount, k, ctx):
        return None

    def motdata_callback(self, data, size, name, d, ctx):
        pixbuf_loader = GdkPixbuf.PixbufLoader()
        py_buf = ctypes.cast(data, ctypes.POINTER(ctypes.c_ubyte * size)).contents
        pixbuf_loader.write(py_buf)
        GLib.idle_add(self.parent._set_dab_image, pixbuf_loader.get_pixbuf())
        pixbuf_loader.close()
        return None

    def syncsignal_callback(self, flag, data):
        if flag:
            self.synced = True
        return None

    def pyaudio_callback(self, in_data, frame_count, time_info, status):
        if ring_buf.read_available < frame_count * 2:
            data = (
                b"x\00" * frame_count * 2
            )  # Fill buffer with nothing if ring buffer empty
        else:
            data = bytes(ring_buf.pop(frame_count * 2))
        return (data, pyaudio.paContinue)


# Thread for scanning dab channels
class scan_thread(threading.Thread):
    def __init__(self, dab_help):
        self.dab_helper = dab_help
        self.program_names = []
        self.finished = False
        self.exit = False
        super().__init__()

    def wait_for_sync(self):
        self.dab_helper.dab_callbacks.synced = False
        start_time = datetime.now()
        while not self.dab_helper.dab_callbacks.synced:
            if (datetime.now() - start_time).seconds >= sync_timeout:
                break
        return self.dab_helper.dab_callbacks.synced

    def add_program(self, name):
        self.program_names.append(name)
        return False

    def check_channel(self, band, channel):
        self.dab_helper.simple_dab.switch_frequency(band, channel)
        if not self.wait_for_sync():
            return True

        # TODO: find a way to check if all programs were found
        start_time = datetime.now()
        while not self.exit:
            sleep(0.1)
            if self.exit:
                return False
            if (
                datetime.now() - start_time
            ).seconds >= timeout:  # Seven seconds to check for programs
                break
            for name in self.program_names:
                if self.dab_helper.simple_dab.is_audio(name):
                    GLib.idle_add(
                        self.dab_helper.parent._add_program,
                        pysimpledab.BAND_III,
                        channel,
                        name.decode("utf-8"),
                    )
                self.program_names.pop()

        return True

    def run(self):
        for channel in pysimpledab.BAND_III_CHANNELS:
            self.dab_helper.parent._update_scan_status(channel)
            if self.exit:
                return False
            if not self.check_channel(pysimpledab.BAND_III, channel):
                self.dab_helper.scanning = False
                return True

        for channel in pysimpledab.L_BAND_CHANNELS:
            self.dab_helper.parent._update_scan_status(channel)
            if self.exit:
                return False
            if not self.check_channel(pysimpledab.L_BAND, channel):
                self.dab_helper.scanning = False
                return True

        self.dab_helper.parent._update_scan_status(None, done=True)

        self.finished = True
        self.dab_helper.scanning = False

    def stop(self):
        self.exit = True


# Helper for pysimpledab
class dab_helper:
    def __init__(self, parent):
        self.core = parent.core
        self.parent = parent
        self.dab_callbacks = dab_callbacks(parent, self)
        self.simple_dab = None
        self.wait_for_start = None
        self.scanning = False
        self.pyaudio = pyaudio.PyAudio()
        self.stream = None
        self.simple_dab = None
        try:
            self.simple_dab = pysimpledab.SimpleDAB()
        except pysimpledab.LibNotFound:
            parent.ENABLED = False
            return

        self._create_api_struct()

    def _create_api_struct(self):
        api_struct = pysimpledab.Callbacks()

        api_struct.dabMode = 1
        api_struct.syncsignal_Handler = pysimpledab.syncsignal_t(
            self.dab_callbacks.syncsignal_callback
        )
        api_struct.systemdata_Handler = self.simple_dab.dummy_system_callback
        api_struct.ensemblename_Handler = self.simple_dab.dummy_ensemble_callback
        api_struct.programname_Handler = pysimpledab.programname_t(
            self.dab_callbacks.programname_callback
        )
        api_struct.fib_quality_Handler = self.simple_dab.dummy_fib_callback
        api_struct.audioOut_Handler = pysimpledab.audioOut_t(
            self.dab_callbacks.audioOut_callback
        )
        api_struct.dataOut_Handler = pysimpledab.dataOut_t(
            self.dab_callbacks.dataOut_callback
        )
        api_struct.bytesOut_Handler = self.simple_dab.dummy_bytes_callback
        api_struct.programdata_Handler = self.simple_dab.dummy_program_data_callback
        api_struct.program_quality_Handler = self.simple_dab.dummy_program_qual_callback
        api_struct.motdata_Handler = pysimpledab.motdata_t(
            self.dab_callbacks.motdata_callback
        )
        api_struct.tii_data_Handler = self.simple_dab.dummy_tii_callback
        api_struct.timeHandler = self.simple_dab.dummy_time_callback

        self.api_struct = api_struct

    def _start_playing(self, station_name):
        try:
            self.simple_dab.switch_station(station_name)
            GLib.idle_add(self.parent._show_info, playing)
            self.stream = self.pyaudio.open(
                format=pyaudio.paInt16,
                channels=2,
                rate=48000,
                output=True,
                stream_callback=self.dab_callbacks.pyaudio_callback,
            )
        except pysimpledab.StationUnusable as ex:
            self.parent._on_error()
        self.wait_for_start = False
        return False

    def start(self, device_type, band, channel):
        self.simple_dab.begin(device_type, self.api_struct)
        self.simple_dab.set_gain(100)
        self.simple_dab.start(band, channel)
        return False

    def stop(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.wait_for_start:
            self.wait_for_start = None
        if self.scanning:
            self.scan_thread.stop()
            self.scan_thread.join()
            self.scanning = False

    def scan(self):
        self.stop()
        self.scanning = True
        self.scan_thread = scan_thread(self)
        self.scan_thread.start()

    def play_station(self, band, channel, station_name):
        self.stop()
        self.simple_dab.switch_frequency(band, channel)

        self.parent._show_info(waiting)

        self.wait_for_start = station_name

    def exit(self):
        self.stop()
        if self.simple_dab:
            self.simple_dab.exit()
