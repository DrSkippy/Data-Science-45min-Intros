import logging
from pet import Pet

logger = logging.getLogger("pet_world." + __name__)

class Snake(Pet):
    def __init__(self, **kwargs):
        # default values
        self.name = "Voltemort"
        self.word = "Sssss"
        self.legs = 0
        super(Snake,self).__init__(**kwargs)
        
        self.logger = logger
        self.logger.info("{} is ready for play!".format(self.name))
