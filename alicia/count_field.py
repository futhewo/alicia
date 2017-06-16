#!/usr/bin/python
# -*-  encoding: iso-8859-1 -*-



###############################################################################
# Copyright 2017 @fuzztheworld
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



###############################################################################
# A field that counts the number of elements of a node.



# Imports #####################################################################
import random
import string
import copy

from alicia.integer_field import *
from alicia.utils import *



# CountField ##################################################################
class CountField(IntegerField):
    """
        A field that counts the number of elements of a node.
    """

    # Constructor =========================================
    def __init__(self, node, size, endianness="be", minValue=0, maxValue=0, name=None, fuzzing=None, overflowing=None, randoming=None, fuzzingNumber=None, overflowNumber=None, randomRate=None, randomNumber=None):
        IntegerField.__init__(self, 0, size, endianness, False, minValue, maxValue, [], name, fuzzing, overflowing, randoming, fuzzingNumber, overflowNumber, randomRate, randomNumber)
        
        if name is None:
            self.name = "CountField {0}".format(self.elementId)
        self.type = "CountField"
        
        # Covered elements.
        self.node = node
        node.boundElements.append(self)

        # Other parameters
        self.default = i2sbs(self.computeCount(), self.minSize, self.endianness)
        self.value = self.default


    # Actioners ===========================================
    # Built-ins ===========================================
    def __str__(self):
        """
            Return a string representing the element.
            @return (string)representation
        """
        string = "[{0}]: ({1}) [{2}]".format(self.name, str(self.minSize), self.node.name)
        nameList = []
        return string
        

    # Notification ========================================
    def notify(self):
        """
            Update its value with the recomputed size.
        """
        if self.notifiable:
            self.update(i2sbs(self.computeCount(), self.minSize, self.endianness))


    def computeCount(self):
        """
            Count the number of elements of the covered node.
        """
        return len(self.node.subElements)


    # Fuzzing =============================================
    def nope(self, steps):
        """
            Return a standard value.
            @param (int)steps: the standard value reference
        """
        debug(">[{0}] {1} (F): Noping.".format(steps, self.name), conf.verbose)
        self.update(i2sbs(self.computeCount(), self.minSize, self.endianness))


    def basic(self, steps, singleChar=False):
        """
            Modifies the size value, while maintaining her in its bounds, without modifying the real size. It targets the bad managed size.
            @param (int)steps
        """
        self.notify() # TODO:Why?
        self.notifiable = False
        IntegerField.basic(self, steps)


    def overflow(self, steps):
        """
            Try the biggest sizes.
            @param (int)steps
        """
        self.notifiable = False
        IntegerField.overflow(self, steps)

    def random(self, step):
        """
            Stuff the size with random chars.
            @param (int)steps
        """
        self.notifiable = False
        IntegerField.random(self, steps)


    # Parsing =============================================
    # Inherited from node

