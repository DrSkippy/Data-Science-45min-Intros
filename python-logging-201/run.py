#!/usr/bin/env python2.7

import logging
from logging.config import fileConfig

import pet,cat,dog,snake

fileConfig("logging.cfg")

global_logger = logging.getLogger("pet_world")
global_logger.warning("Here we go...!")

d = dog.Dog()
mad_cat = cat.Cat(word="Hiss")
s = snake.Snake()
