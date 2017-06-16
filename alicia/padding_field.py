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

from alicia.field import *
from alicia.utils import *



# PaddingField ############################################
class PaddingField(Field):
    """
        A field to make padding to a specific paddingBlockSize with specific occurences of paddingElement.
    """

    # Constructor =========================================
    def __init__(self, paddingElement, paddingBlockSize, fields, name=None, fuzzing=None, overflowing=None, randoming=None, fuzzingNumber=None, overflowNumber=None, randomRate=None, randomNumber=None):
        Field.__init__(self, "", 0, 0, [], name, fuzzing, overflowing, randoming, fuzzingNumber, overflowNumber, randomRate, randomNumber)
        
        if name is None:
            self.name = "PaddingField {0}".format(self.elementId)
        self.type = "PaddingField"

        self.paddingElement = paddingElement     # Usual value
        self.paddingBlockSize = paddingBlockSize # Targeted size for the padding
        
        # Covered fields
        self.fields = fields
        for field in self.fields:
            field.boundElements.append(self)
        
        # Generate a clever default value
        self.default = self.paddingElement * self.computeSize()
        self.value  = self.default
        self.values = [self.value]
        self.notify()

        self.remainingSize = 0


    # Actioners ===========================================
    # Built-ins ===========================================
    def __str__(self):
        """
            Return a string representing the element.
            @return (string)representation
        """
        string = "[{0}]: ({1}:{2}) [".format(self.name, self.paddingElement, self.paddingBlockSize)
        nameList = []
        for field in self.fields:
            nameList.append(field.name)
        string += ", ".join(nameList) + "]"
        return string


    # Notification ========================================
    def notify(self):
        """
            Called when the base field is modified in order to update the size.
            Its value is stuffed with paddingElement in order that its value concatenated to the value of the base field have a size multiple of paddingBlockSize.
        """
        if self.notifiable:
            self.update(self.paddingElement * self.computeSize())


    def computeSize(self):
        """
            Add the sizes of all the covered fields and deduce the needed size.
        """
        size = 0
        for field in self.fields:
            size += field.getLength()
        return self.paddingBlockSize - (size % self.paddingBlockSize)


    # Fuzzing =============================================
    def nope(self, steps):
        """
            Return a standard value.
            @param (int)steps: the standard value reference
        """
        debug(">[{0}] {1} (F): Noping.".format(steps, self.name), conf.verbose)
        self.update(self.paddingElement * self.computeSize())


    def basic(self, steps, singleChar=False):
        """
            @param (int)steps
        """
        self.notifiable = False
        Field.basic(self, steps, singleChar=True)


    def overflow(self, steps):
        """
            Add a lot of padding elements while respecting the padding block size.
            @param (int)steps
        """
        self.notifiable = False
        r = random.Random(steps)
        numberOfTimes = r.randint(conf.overflowMin * (steps + 1), conf.overflowMax * (steps + 1)) ** conf.agressivity
        numberOfTimes += self.paddingBlockSize - numberOfTimes % self.paddingBlockSize
        debug(">[{0}] {1} (F): Overflow by {2} {3}".format(steps, self.name, numberOfTimes, repr(self.paddingElement)), conf.verbose)
        self.update(self.paddingElement * numberOfTimes)


    def random(self, steps):
        """
            Stuff the padding size with one repeated random char.
            @param (int)steps
        """
        self.notifiable = False

        r = random.Random(steps)
        string = chr(r.randint(0, 255)) * len(self.value)
        debug(">[{0}] {1} (F): Random".format(steps, self.name), conf.verbose)
        self.update(string)



    # Parsing =============================================
    def parse(self, value, backward=False, root=False):
        retValue = value
        eatenValue = ""
        if backward:
            retList = list(retValue)
            retList.reverse()
            retValue = ''.join(retList)
            while retValue.find(self.paddingElement) == 0:
                retValue = retValue[len(self.paddingElement):]
                eatenValue += self.paddingElement
            retList = list(retValue)
            retList.reverse()
            retValue = ''.join(retList)

        else:
            while retValue.find(self.paddingElement) == 0:
                retValue = retValue[len(self.paddingElement):]
                eatenValue += self.paddingElement

        self.value = eatenValue
        #TODO: check that the size is respected.
        self.parsed = True

        if root:
            assert(len(retValue) == 0)
        return retValue

