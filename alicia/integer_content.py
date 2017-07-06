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
from configuration import *
from utils import *

from content import *



# IntegerContent ##############################################################
class IntegerContent(Content):
    """
        Defines constraints on the content of a field.
    """

    magicCharacters = ["\x00", "\x01", "\xfe", "\xff"]

    # Constructor =========================================
    def __init__(self, value, size=4, signed=False, littleEndian=False):
        self.type = "IntegerContent"
        _value = ""
        integerCurrent = 0
        if type(value) == int:
            _value = i2sbs(value, size, littleEndian)
            integerCurrent = value
        elif type(value) == str:
            _value = value
            fill(_value, size)
            integerCurrent = sbs2i(value, signed, littleEndian)
        self.default = _value
        self.current = _value
        self.future = _value
        self.integerCurrent = integerCurrent

        self.size = size
        self.signed = signed
        self.littleEndian = littleEndian

        # Make a list of magicValues we would like to see.
        theoricMinValue = 0
        theoricMaxValue = 0
        if self.signed:
            theoricMaxValue = 2 ** (self.size * 8 - 1) - 1
            theoricMinValue = -theoricMaxValue - 1
        else:
            theoricMaxValue = 2 ** (self.size * 8) - 1

        # The most classical attack vectors.
        self.magicValues = [theoricMaxValue, theoricMinValue, theoricMaxValue + 1, theoricMinValue + 1, theoricMaxValue - 1]
        if self.signed:
            self.magicValues += [theoricMinValue - 1, -1, 0, 1]


    # Actioners ===========================================
    def update(self, value):
        self.current = fill(value, self.size)
        self.integerCurrent = sbs2i(value, self.signed, self.littleEndian)


    def integerUpdate(self, integerValue):
        """
            Transform an integer into a fixed-size string with the given endianness.
        """
        self.integerCurrent = integerValue
        self.update(i2sbs(integerValue, self.size, self.littleEndian))


    # Fuzzing =============================================
    def newCharacter(self, rand):
        """
            Return a new character concording with this type.
        """
        return rand.choice(IntegerContent.magicCharacters)


    def fuzz(self, minSize, maxSize, rand, steps):
        """
            Fuzz the given value that needs to stay in the size range.
            @param (int)minSize
            @param (int)maxSize
            @param (random.Random)rand
            @param (int)steps
        """
        assert(self.size == maxSize == minSize)
        debug("  Fuzzing as {0}".format(self.type), configuration.verbose)
        integerValue = 0
        # Starting with the most classical attack vectors for integer.

        if steps < len(self.magicValues):
            integerValue = self.magicValues[steps]

        else:
            if self.signed:
                sign = -1 ** r.randint(0, 1)
                # Border case already checked
                integerValue = sign * 2 ** rand.randint(1, maxSize * 8 - 2)
            else:
                integerValue = 2 ** rand.randint(1, maxSize * 8 - 1)

            integerValue += rand.randint(-1, 1)
        self.integerUpdate(integerValue)

