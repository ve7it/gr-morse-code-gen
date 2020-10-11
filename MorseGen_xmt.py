#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Morse Code Generator
# Author: Barry Duggan
# Description: USRP transmit
# GNU Radio version: 3.9.0.0-git

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio import zeromq
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import epy_block_0_0

from gnuradio import qtgui

class MorseGen_xmt(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Morse Code Generator", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Morse Code Generator")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "MorseGen_xmt")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.speed = speed = 13
        self.samp_rate = samp_rate = 50000
        self.usrp_rate = usrp_rate = 1000000
        self.symbol_rate = symbol_rate = 300
        self.rf_gain = rf_gain = 9
        self.repeat = repeat = int(1.2 * samp_rate / speed)
        self.center_freq = center_freq = 144.95e6

        ##################################################
        # Blocks
        ##################################################
        self._rf_gain_range = Range(0, 76, 1, 9, 200)
        self._rf_gain_win = RangeWidget(self._rf_gain_range, self.set_rf_gain, 'RF Gain', "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._rf_gain_win)
        self._center_freq_range = Range(144.0e6, 148.0e6, 1.0e3, 144.95e6, 200)
        self._center_freq_win = RangeWidget(self._center_freq_range, self.set_center_freq, 'Tuning', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._center_freq_win)
        self.zeromq_pull_msg_source_0 = zeromq.pull_msg_source('tcp://127.0.0.1:50251', 100, False)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_samp_rate(usrp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(200000, 0)
        self.uhd_usrp_sink_0.set_gain(rf_gain, 0)
        self.root_raised_cosine_filter_0_0 = filter.fir_filter_fff(
            1,
            firdes.root_raised_cosine(
                0.95,
                samp_rate,
                symbol_rate,
                0.35,
                200))
        self.root_raised_cosine_filter_0 = filter.fir_filter_fff(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                symbol_rate,
                0.35,
                200))
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            16384, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1.5)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.5, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.epy_block_0_0 = epy_block_0_0.mc_sync_block()
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_repeat_0_0 = blocks.repeat(gr.sizeof_gr_complex*1, (int)(usrp_rate/samp_rate))
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, repeat)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.zeromq_pull_msg_source_0, 'out'), (self.epy_block_0_0, 'msg_in'))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_repeat_0_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_repeat_0_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.epy_block_0_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.root_raised_cosine_filter_0_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.qtgui_time_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "MorseGen_xmt")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed
        self.set_repeat(int(1.2 * self.samp_rate / self.speed))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_repeat(int(1.2 * self.samp_rate / self.speed))
        self.blocks_repeat_0_0.set_interpolation((int)(self.usrp_rate/self.samp_rate))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol_rate, 0.35, 200))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(0.95, self.samp_rate, self.symbol_rate, 0.35, 200))

    def get_usrp_rate(self):
        return self.usrp_rate

    def set_usrp_rate(self, usrp_rate):
        self.usrp_rate = usrp_rate
        self.blocks_repeat_0_0.set_interpolation((int)(self.usrp_rate/self.samp_rate))
        self.uhd_usrp_sink_0.set_samp_rate(self.usrp_rate)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol_rate, 0.35, 200))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(0.95, self.samp_rate, self.symbol_rate, 0.35, 200))

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.uhd_usrp_sink_0.set_gain(self.rf_gain, 0)

    def get_repeat(self):
        return self.repeat

    def set_repeat(self, repeat):
        self.repeat = repeat
        self.blocks_repeat_0.set_interpolation(self.repeat)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)





def main(top_block_cls=MorseGen_xmt, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
