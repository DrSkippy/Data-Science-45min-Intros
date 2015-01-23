import logging
from pet import Pet

logger = logging.getLogger("pet_world." + __name__)

class Dog(Pet):
    def __init__(self, **kwargs):
        # default values
        self.name = "Fido"
        self.word = "Arf!"
        self.legs = 4
        super(Dog,self).__init__(**kwargs)
       
        self.logger = logger
        self.logger.info("{} is ready for play!".format(self.name))
