import logging

class Pet(object):
    def __init__(self, **kwargs):
        # attach all keyword arguments
        [setattr(self,k,v) for k,v in kwargs.items()]
        
        # get the class name
        self.animal = self.__class__.__name__
        assert self.animal != "Pet"     

    def talk(self):
        self.logger.info("{}\n".format(self.word))
        
    def get_bio(self):
        self.logger.info("This pet is a {0} named {1}. It has {2} legs.\n".format(self.animal,self.name,self.legs))

