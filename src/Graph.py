# coding=utf-8

from RoutingTable import *
from Node import *
import random
from random import choice
from Crypto.Hash import SHAKE256
from binascii import hexlify
from random import choice
from Exceptions import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Graph():

    def __init__(self):
        self.mapID = {}
        self.count = 0

    def addMap(self,map):
        self.mapID = map

    def incrementCounter(self):
        self.count += 1

    def getCounter(self):
        return self.count