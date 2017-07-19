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

from alicia.open_field import *
from alicia.utils import *



# PaddingField ################################################################
class PaddingField(OpenField):
    """
        A field to make padding to a specific paddingBlockSize with specific occurences of paddingElement.
    """

    # Constructor =========================================
    def __init__(self, content, paddingSize, elements, name=None, weight=1.0):
        assert(len(content.default) == 1)
        OpenField.__init__(self, content, paddingSize, 0, name, weight)
        
        self.type = "PaddingField"
        self.setName(name)

        # Covered fields
        self.elements = elements
        for element in self.elements:
            element.bound(self)

        self.padder = content.default[0]
        self.notify()
        self.content.default = self.content.current # Save the default size.


    # Actioners ===========================================
    # Built-ins ===========================================
    def __str__(self):
        """
            Return a string representing the element.
            @return (string)representation
        """
        string = "[{0}]: ({1}:{2}) [".format(self.name, self.padder, self.maxSize)
        nameList = []
        for element in self.elements:
            nameList.append(element.name)
        string += ", ".join(nameList) + "]\n"
        return string


    # Notification ========================================
    def notify(self):
        """
            Called when the base field is modified in order to update the size.
            Its value is stuffed with padder in order that its value concatenated to the value of the base field have a size multiple of the padding size.
        """
        self.update(self.padder * self.computeSize())


    def computeSize(self):
        """
            Add the sizes of all the covered fields and deduce the needed size.
        """
        size = 0
        for element in self.elements:
            size += element.getSize()
        size = self.maxSize - (size % self.maxSize)
        return size % self.maxSize


    # Fuzzing =============================================
    # Parsing =============================================
    def parse(self, value, backward=False, root=False):
        pass

