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
# Vocabulary structure, i.e. definition of fields and the structure that comes with it.



# Imports #####################################################################
import random
import string
import copy

from alicia.integer_field import *
from alicia.utils import *



# SizeField ###################################################################
class SizeField(IntegerField):
    """
        A field that contains the size of a list of fields.
        Its value is updated after the targeted fields' value.
    """

    # Constructor =========================================
    def __init__(self, fields, size, selfSize=False, endianness="be", minValue=0, maxValue=0, name=None, fuzzing=None, overflowing=None, randoming=None, fuzzingNumber=None, overflowNumber=None, randomRate=None, randomNumber=None):
        IntegerField.__init__(self, 0, size, endianness, False, minValue, maxValue, [], name, fuzzing, overflowing, randoming, fuzzingNumber, overflowNumber, randomRate, randomNumber)
        
        if name is None:
            self.name = "SizeField {0}".format(self.elementId)
        self.type = "SizeField"
        
        # Covered fields.
        self.fields = fields
        for field in self.fields:
            field.boundElements.append(self)

        # Other parameters
        self.selfSize = selfSize
        self.default = i2sbs(self.computeSize(), self.minSize, self.endianness)
        self.value = self.default

        # Computation parameters
        self.remainingSize = 0


    # Actioners ===========================================
    # Built-ins ===========================================
    def __str__(self):
        """
            Return a string representing the element.
            @return (string)representation
        """
        string = "[{0}]: ({1}:{2}) [".format(self.name, str(self.minSize), str(self.selfSize))
        nameList = []
        for field in self.fields:
            nameList.append(field.name)
        string += ", ".join(nameList) + "]"
        return string
        

    # Notification ========================================
    def notify(self):
        """
            Update its value with the recomputed size.
        """
        if self.notifiable:
            self.update(i2sbs(self.computeSize(), self.minSize, self.endianness))


    def computeSize(self):
        """
            Adds the sizes of all the covered fields.
        """
        size = 0
        for field in self.fields:
            size += field.getLength()
        # selfSize, does not manage maxSize yet
        if self.selfSize:
            size += self.minSize
        return size


    # Fuzzing =============================================
    def nope(self, steps):
        """
            Return a standard value.
            @param (int)steps: the standard value reference
        """
        debug(">[{0}] {1} (F): Noping.".format(steps, self.name), conf.verbose)
        self.update(i2sbs(self.computeSize(), self.minSize, self.endianness))


    def basic(self, steps, singleChar=False):
        """
            Modifies the size value, while maintaining her in its bounds, without modifying the real size. It targets the bad managed size.
            @param (int)steps
        """
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
    def parse(self, value, backward=False, root=False):
        self.parsed = True
        finalValue = ""
        assert(self.minSize == self.maxSize)
        eatingSize = self.minSize

        for boundElement in self.boundElements:
            boundElement.remainingSize -= eatingSize

        assert(len(value) >= eatingSize)
        if backward:
            # Eat at the end
            finalValue = value[:-eatingSize]
            self.value = value[-eatingSize:]
        else:
            # Eat at the beginning
            finalValue = value[eatingSize:]
            self.value = value[:eatingSize]

        self.remainingSize += bs2ui(self.value)
        if self.selfSize: # Remove its own size.
            self.remainingSize -= self.minSize

        # Keep some space for the known fixed field.
        for field in self.fields:
            if field.minSize == field.maxSize:
                self.remainingSize -= field.minSize

        assert(self.remainingSize >= 0)

        if root:
            assert(len(finalValue) == 0)
        return finalValue


    def parseClean(self):
        self.parsed = False
        self.remainingSize = 0        

