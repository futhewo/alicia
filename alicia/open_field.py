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

from alicia.close_field import *
from alicia.integer_content import *
from alicia.content import *
from alicia.utils import *



# OpenField ####################################################################
class OpenField(CloseField):
    """
        A leaf element. Has a value.
        Manipulating him means modifying its value.
        Its size can vary between a provided min and a max size.
    """

    # Constructor =========================================
    def __init__(self, content, maxSize, minSize=0, name=None, weight=1.0):
        assert(type(content) is not IntegerContent) # IntegerContent are fixed-size.
        CloseField.__init__(self, content, name, weight)
        
        self.type = "OpenField"
        self.setName(name)
        
        self.maxSize = maxSize
        self.minSize = minSize


    # Actioners ===========================================
    # Built-ins ===========================================
    # Fuzzing =============================================
    def fuzz(self, steps):
        """
            Fuzz, through mutation the predefined value.
        """
        Element.fuzz(self, steps)
        rand = random.Random(steps)
        fuzzType = rand.randint(0, 1)

        if fuzzType == 0:
            self.content.fuzz(self.minSize, self.maxSize, rand, steps)
        else:
            self.fieldFuzz(rand)


    def fieldFuzz(self, rand):
        workingValue = list(self.compose())
       
        indexes = generateIndexes(len(workingValue), rand, configuration.randomness)
        for index in indexes:
            if index < 0:
                # removed index
                continue
            if len(workingValue) == 0:
                # If no elements, we can do nothing
                return
            # Select the mutation kind
            oracle = rand.choice([ADD, MUTATION, SWAP, REMOVE])

            # Mutation
            if oracle == ADD:
                workingValue = self.add(workingValue, rand, index, indexes)

            elif oracle == MUTATION:
                workingValue = self.mutation(workingValue, rand, index)

            elif oracle == SWAP:
                workingValue = self.swap(workingValue, rand, index)
            
            elif oracle == REMOVE:
                workingValue = self.remove(workingValue, rand, index, indexes)

        self.update(''.join(workingValue))


    def overflow(self, steps):
        """
            Repeat a specific char a high number of times. The aim is to overflow buffers.
            @param (int)steps
        """
        pass


    # Parsing =============================================
    def parse(self, value, backward=False, root=False):
        pass

