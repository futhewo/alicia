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
# Represent an integer.



# Imports #####################################################################
import random
import math

from alicia.field import *
from alicia.utils import *



# IntegerField #############################################
class IntegerField(Field):
    """
        A field that contains an integer.
    """

    def __init__(self, default, size, endianness="be", signed=False, minValue=0, maxValue=0, values=None, name=None, fuzzing=None, overflowing=None, randoming=None, fuzzingNumber=None, overflowNumber=None, randomRate=None, randomNumber=None):

        # This to allow users to provide integers as inpuyt.
        _default = default
        if type(default) == int:
            _default = i2sbs(default, size, endianness)

        _values = None
        if values is not None:
            _values = []
            for _value in values:
                if type(_value) == int:
                    _values.append(i2sbs(_value, size, endianness))
                else:
                    _values.append(_value)

        Field.__init__(self, _default, size, size, _values, name, fuzzing, overflowing, randoming, fuzzingNumber, overflowNumber, randomRate, randomNumber)

        if name is None:
            self.name = "IntegerField {0}".format(self.elementId)
        self.type = "IntegerField"

        self.endianness = endianness
        self.signed = signed
        self.minValue = minValue
        self.maxValue = maxValue

        self.theoricMinValue = 0
        self.theoricMaxValue = 0
        if self.signed:
            self.theoricMaxValue = 2 ** (self.maxSize * 8 - 1) - 1
            self.theoricMinValue = -self.theoricMaxValue - 1
        else:
            self.theoricMaxValue = 2 ** (self.maxSize * 8) - 1

        self.integerValue = sbs2i(self.value, self.signed, self.endianness)
        self.defaultIntegerValue = self.integerValue

        # The most classical attack vectors.
        self.basicValues = [self.theoricMaxValue, self.theoricMinValue, self.theoricMaxValue + 1, self.theoricMinValue + 1, self.theoricMaxValue - 1, self.theoricMinValue - 1, 1]
        if self.minValue != 0:
            self.basicValues += [self.minValue, self.minValue + 1, self.minValue - 1]

        if self.maxValue != 0:
            self.basicValues += [self.maxValue, self.maxValue + 1, self.maxValue - 1]

        if self.signed:
            self.basicValues += [0, -1]


    def integerUpdate(self, integerValue):
        """
            Transform an integer into a fixed-size string with the given endianness.
        """
        self.integerValue = integerValue
        self.update(i2sbs(integerValue, self.maxSize, self.endianness))


    def clean(self):
        Field.clean(self)
        self.integerValue = self.defaultIntegerValue


    # Fuzzing =============================================
    def basic(self, steps, singleChar=False):
        integerValue = 0
        # Starting with the most classical attack vectors for integer.
        if steps < len(self.basicValues):
            integerValue = self.basicValues[steps]  

        else:
            r = random.Random(steps)
            if self.signed:
                sign = -1 ** r.randint(0, 1)
                # Border case already checked
                integerValue = sign * 2 ** r.randint(1, self.maxSize * 8 - 2)
            else:
                integerValue = 2 ** r.randint(1, self.maxSize * 8 - 1)

            integerValue += r.randint(-1, 1)
        debug(">[{0}] {1} (F): Basic".format(steps, self.name), conf.verbose)
        self.integerUpdate(integerValue)


    def overflow(self, steps):
        integerValue = 0
        if self.signed:
            integerValue = 2 ** (self.maxSize * 8 + (steps / 2)) - 1
            sign = (-1) ** (steps % 2)
            integerValue = sign * integerValue - (steps % 2)
        else:
            integerValue = 2 ** (self.maxSize * 8 + steps + 1) - 1

        debug(">[{0}] {1} (F): Overflow".format(steps, self.name), conf.verbose)
        self.integerUpdate(integerValue)


    # Parsing =============================================
    def parse(self, value, backward=False, root=False):
        r = Field.parse(self, value, backward=False, root=False)
        self.integerValue = sbs2i(r, self.signed, self.endianness)
        return r

