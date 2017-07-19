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



# SizeField ###################################################################
class SizeField(CloseField):
    """
        A field that contains the size of a list of elements.
        Its value is updated after the targeted elements' value.
    """

    # Constructor =========================================
    def __init__(self, content, elements, selfSize=False, name=None, weight=1.0):
        assert(type(content) is IntegerContent)
        CloseField.__init__(self, content, name, weight)
        
        self.type = "SizeField"
        self.setName(name)

        self.selfSize = selfSize

        # Covered fields
        self.elements = elements
        for element in self.elements:
            element.bound(self)

        self.notify()
        self.content.default = self.content.current # Save the default size.


    # Actioners ===========================================
    # Built-ins ===========================================
    def __str__(self):
        """
            Return a string representing the element.
            @return (string)representation
        """
        string = "[{0}]: ({1}:{2}) [".format(self.name, self.selfSize, self.content.size)
        nameList = []
        for element in self.elements:
            nameList.append(element.name)
        string += ", ".join(nameList) + "]\n"
        return string


    # Notification ========================================
    def notify(self):
        """
            Update its value with the recomputed size.
        """
        self.content.integerUpdate(self.computeSize())
        self.pushNotification()


    def computeSize(self):
        """
            Add the sizes of all the covered fields and deduce the needed size.
        """
        size = 0
        for element in self.elements:
            size += element.getSize()
        if self.selfSize:
            size += self.getSize()
        return size


    # Fuzzing =============================================
    # Parsing =============================================
    def parse(self, value, backward=False, root=False):
        pass

