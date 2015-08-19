#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Analyzer
# Generated: Wed Aug 19 15:57:40 2015
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx
import posix_ipc as ipc
import mmap


class analyzer(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Analyzer")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        self.channel = ipc.SharedMemory('/chan', ipc.O_CREAT, size=2)
        self.mem = mmap.mmap(self.channel.fd, 2)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 192000
        self.mem.seek(0)
        self.channel = channel = int(self.mem.read(1))
        self.baseband = baseband = 60

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=baseband,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.5,
        	title="Waterfall Plot",
        )
        self.Add(self.wxgui_waterfallsink2_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=baseband,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=50,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.666,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        _channel_sizer = wx.BoxSizer(wx.VERTICAL)
        self._channel_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_channel_sizer,
        	value=self.channel,
        	callback=self.set_channel,
        	label='channel',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._channel_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_channel_sizer,
        	value=self.channel,
        	callback=self.set_channel,
        	minimum=0,
        	maximum=7,
        	num_steps=7,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.Add(_channel_sizer)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_short*1, "/home/jszum/github/zmqtransfer/zmqfifo", False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_short_to_float_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.wxgui_waterfallsink2_0, 0))    
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_float_to_complex_0, 0))    


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel
        self.mem.seek(0)
        self.mem.write(str(channel))
        self._channel_slider.set_value(self.channel)
        self._channel_text_box.set_value(self.channel)

    def get_baseband(self):
        return self.baseband

    def set_baseband(self, baseband):
        self.baseband = baseband
        self.wxgui_fftsink2_0.set_baseband_freq(self.baseband)
        self.wxgui_waterfallsink2_0.set_baseband_freq(self.baseband)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = analyzer()
    tb.Start(True)
    tb.Wait()
