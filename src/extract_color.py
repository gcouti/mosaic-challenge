import logging
import settings

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
LOG = logging.getLogger(__name__)
LOG.setLevel(settings.LOG_LEVEL)

class ExtractColor(object):
    
    def __init__(self):
        pass
    
    def which_color(self):
        pass
    
    
    
        