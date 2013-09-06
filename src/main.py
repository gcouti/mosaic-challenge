"""
    
"""
import sys
import logging
import PIL
import settings
from image_builder import FakePixelImage
from image_builder import MosaicImage

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
LOG = logging.getLogger(__name__)
LOG.setLevel(settings.LOG_LEVEL)

def main(rfile,pfiles):
    
    pimages = []
    for f in pfiles:
        pimages.append(FakePixelImage(f))
        
    m = MosaicImage(rfile)
    m.process(pimages)
    m.finish()
    
if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print "Error"
    
    print sys.argv[2:len(sys.argv)]
    main(sys.argv[1],sys.argv[2:len(sys.argv)])
    
