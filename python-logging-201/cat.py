import logging
from pet import Pet

logger = logging.getLogger("pet_world." + __name__)

class Cat(Pet):
    def __init__(self, **kwargs):
        # default values
        self.name = "Tom"
        self.word = "Meow"
        self.legs = 4
        super(Cat,self).__init__(**kwargs)
        
        self.logger = logger
        self.logger.info("{} is ready for play!".format(self.name))
