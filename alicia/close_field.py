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

from alicia.static_field import *
from alicia.content import *
from alicia.utils import *



# Field ########################################################################
class CloseField(StaticField):
    """
        A leaf element. Has a value.
        Manipulating him means modifying its value.
    """

    # Constructor =========================================
    def __init__(self, content, name=None, weight=1.0):
        Element.__init__(self, name, False, weight)
        
        self.type = "CloseField"
        self.setName(name)
        self.content = content       
        self.size = len(self.content.default)


    # Actioners ===========================================
    def update(self, value):
        self.content.update(value)


    # Built-ins ===========================================
    # Fuzzing =============================================
    def fuzz(self, steps):
        """
            Fuzz, through mutation, the predefined value.
        """
        rand = random.Random(steps)
        fuzzType = rand.randint(0, 1)

        if fuzzType == 0:
            self.content.fuzz(self.size, self.size, rand, steps)
        else:
            self.fieldFuzz(rand)


    def newFuzzedSubElement(self, rand):
        return self.content.newCharacter(rand)


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
            oracle = rand.choice([MUTATION, SWAP])

            # Mutation
            if oracle == MUTATION:
                workingValue = self.mutation(workingValue, rand, index)

            elif oracle == SWAP:
                workingValue = self.swap(workingValue, rand, index)
                    
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

