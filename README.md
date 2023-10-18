# gst_helloworld

---

![](images/gst.drawio.png)

```bash
$ git clone https://github.com/DaiGuard/gst_helloworld.git
$ cd gst_helloworld
$ GST_DEBUG=4 GST_PLUGIN_PATH=$GST_PLUGIN_PATH:$PWD/gst \
    gst-launch-1.0 videotestsrc ! "video/x-raw,format=RGB" ! gst_helloworld ! \
    videoconvert ! autovideosink sync=false

```