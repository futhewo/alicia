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
from content import *
from alicia.configuration import *
from alicia.utils import *



# CarefulContent ##############################################################
class CarefulContent(Content):
    """
        Defines constraints on the content of a field.
        Will use values to look like the default value.
    """

    # Constructor =========================================
    def __init__(self, value):
        Content.__init__(self, value)
        self.type = "CarefulContent"


    # Actioners ===========================================
    # Fuzzing =============================================
    def newCharacter(self, rand):
        """
            Return a new character concording with this type.
        """
        return rand.choice(list(self.default))


    def fuzz(self, minSize, maxSize, rand, steps):
        """
            Fuzz the given value that needs to stay in the size range.
            @param (int)minSize
            @param (int)maxSize
            @param (random.Random)rand
            @param (int)steps
        """
        debug("  Fuzzing as {0}".format(self.type), configuration.verbose)
        value = ""
        for i in range(rand.randint(minSize, maxSize)):
            value += self.newCharacter(rand)
        self.update(value)

