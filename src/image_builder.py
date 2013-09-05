import logging
import settings
from PIL import Image
import math
from PIL.ImageQt import rgb


logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
LOG = logging.getLogger(__name__)
LOG.setLevel(settings.LOG_LEVEL)

def extract_color(img, x0, y0, x1, y1):
    """
        Extract average from block of pixels
        The first parameter is image of PIL library the next parameters is points of the square
        
        return tuple of RGB
    """

    color = None
        
    for x in range(x0, x1):
        for y in range(y0, y1):
            LOG.debug("X: %d Y: %d" % (x, y))
            cpix = img.getpixel((x, y))
            
            if not color:
                color = [cpix[0], cpix[1], cpix[2]]
            else:       
                color[0] = (color[0] + cpix[0]) / 2
                color[1] = (color[1] + cpix[1]) / 2
                color[2] = (color[2] + cpix[2]) / 2
                        
            LOG.debug("PColor R:%d G:%d B:%d" % (cpix[0], cpix[1], cpix[2]))
            LOG.debug("Media R:%d G:%d B:%d" % (color[0], color[1], color[2]))
            
    return (color[0], color[1], color[2]) 


class FakePixelImage(object):
    
    def __init__(self, fpath):
        self.img = Image.open(fpath)
        self.color = extract_color(self.img, 0, 0, self.img.size[0], self.img.size[1])
        LOG.debug(":::::> Block Color R:%d G:%d B:%d" % (self.color[0], self.color[1], self.color[2]))

        
class MosaicImage(object):
    
    def __init__(self, rfile):
        self.img = Image.open(rfile)
        self.mosaic = Image.new("RGB", self.img.size, "white")
        
    def process(self, fpixel_list):
        """
            Process mosaic
        """
        avg = 200
        color = None
        pix_size = 4
        xs = self.img.size[0] / pix_size
        ys = self.img.size[1] / pix_size
        
        for i in range(0, xs):
            for j in range(0,ys):
                x0 = (i * pix_size)
                y0 = (j * pix_size)
                
                if x0 >= self.img.size[0] - pix_size:
                    x0 = self.img.size[0] - pix_size
                
                if y0 >= self.img.size[1] - pix_size:
                    y0 = self.img.size[1] - pix_size
                            
                color = extract_color(self.img, x0, y0, x0 + pix_size, y0 + pix_size)
                
                some_pixel= False
                for f in fpixel_list[0:1]:
                    
                    sum_diff = 0
                    for RGB in range(0,3):
                        sum_diff += math.fabs(color[RGB]-f.color[RGB])
                        
                    if sum_diff < avg:
                        some_pixel = True
                        print "Coloca imagem X: %d Y: %d"%(x0,y0)
                    else:
                        fk_pixel = Image.new("RGB", (pix_size,pix_size), rgb(color[0],color[1],color[2]))
                        self.mosaic.paste(fk_pixel,(x0,y0))        
              
    def finish(self):
        self.mosaic.save("test" + ".mosaic", "JPEG")
