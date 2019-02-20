import pyrana
from pyrana.formats import find_stream, MediaType
import PIL

if __name__ == "__main__":
  filePath = "./samples/drop.avi"
  pyrana.setup()  

  # with open(filePath,"rb") as src:
  #   dmx = pyrana.Demuxer(src)
  with open(filePath, "rb") as src:
   dmx = pyrana.formats.Demuxer(src)
   sid = pyrana.formats.find_stream(dmx.streams,
                                    0,
                                    MediaType.AVMEDIA_TYPE_VIDEO)
   num = 0
   vdec = dmx.open_decoder(sid)
   frame = vdec.decode(dmx.stream(sid))
   image = frame.image(pyrana.video.PixelFormat.AV_PIX_FMT_RGB24)
   print("type image: ",type(image))
   
   
