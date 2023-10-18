import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import Gst, GObject, GLib, GstBase, GstVideo

import numpy as np
import cv2


FORMATS = "{RGBx,BGRx,xRGB,xBGR,RGBA,BGRA,ARGB,ABGR,RGB,BGR}"


class GstHelloWorld(GstBase.BaseTransform):

    GST_PLUGIN_NAME = 'gst_helloworld'

    __gstmetadata__ = (
        "GstHelloWorld",
        "Filter",
        "Hello World Filter Demo",
        "DaiGuard <dai_guard@gmail.com>"
    )

    __gsttemplates__ = (
        Gst.PadTemplate.new(
            "src",
            Gst.PadDirection.SRC,
            Gst.PadPresence.ALWAYS,
            Gst.Caps.from_string(
                f'video/x-raw,format={FORMATS},width=[1,2147483647],height=[1,2147483647]'
            )
        ),
        Gst.PadTemplate.new(
            "sink",
            Gst.PadDirection.SINK,
            Gst.PadPresence.ALWAYS,
            Gst.Caps.from_string(
                f'video/x-raw,format={FORMATS},width=[1,2147483647],height=[1,2147483647]'
            )
        )
    )

    def __init__(self):
        super(GstHelloWorld, self).__init__()

        self.width = -1
        self.height = -1
        self.format = 'unknown'

    def do_set_caps(self, incaps: Gst.Caps, outcaps: Gst.Caps) -> bool:
        in_struct = incaps.get_structure(0)
        self.width = in_struct.get_int('width').value
        self.height = in_struct.get_int('height').value
        self.format = in_struct.get_string('format')
        return True
    
    def do_get_property(self,
                        property_id: int,
                        value: GObject.Value,
                        pspec: GObject.ParamSpec):
        pass

    def do_set_property(self,
                        property_id: int,
                        value: GObject.Value,
                        pspec: GObject.ParamSpec):
        pass

    def do_transform(self, 
                     inbuf: Gst.Buffer,
                     outbuf: Gst.Buffer) -> Gst.FlowReturn:
        
        with inbuf.map(Gst.MapFlags.READ | Gst.MapFlags.WRITE) as info:

            if self.format in ['RGB', 'BGR']:

                image = np.ndarray(shape=(self.height, self.width, 3), 
                                dtype=np.uint8, buffer=info.data)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                data = image.tostring()
                # outbuf = Gst.Buffer.new_allocate(None, len(data), None)
                outbuf.fill(0, data)
        return Gst.FlowReturn.OK
    
    # def do_generate_output(self) -> (Gst.FlowReturn, Gst.Buffer):        
    #     inbuf = self.queued_buf
    #     return (Gst.FlowReturn.OK, )


GObject.type_register(GstHelloWorld)
__gstelementfactory__ = (GstHelloWorld.GST_PLUGIN_NAME,
                        Gst.Rank.NONE, GstHelloWorld)