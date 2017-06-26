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
from alicia.configuration import *
from alicia.utils import *



# Element #####################################################################
class Element(object):
    """
        The fuzzer displays all elements on a tree form, all elements of this tree being of this class.
        Be warned that this class represents artificial elements without subElements or value. It is more of an abstract class, even if it can be used.
    """

    # Constructor =========================================
    def __init__(self, name=None, static=False, weight=1.0):
        """
            @param (string)name: name of the element.
            @param (bool)static: can be modified.
            @param (float)weight: ponderation for the number of fuzz-cases.
        """

        # Identification
        global elementId
        self.elementId = elementId
        elementId += 1
        self.type = "Element"
        self.setName(name)

        # Attribute setting
        assert(type(static) is bool)
        assert(type(weight) is float)
        self.static = static
        self.weight = weight

        # Bound fields
        self.boundElements = []   # Fields that depend on this field.
        self.notifiable = True

        # Parsing
        self.parsed = False

        self.preForecast()


    # Actioners ===========================================
    def setName(self, name):
        self.name = name
        if name is None:
            self.name = "{0} {1}".format(self.type, self.elementId)
        

    # Built-ins ===========================================
    def __str__(self):
        """
            Return a string representing the element.
            @return (string)representation
        """
        string = "[{0}]\n".format(self.name)
        return string


    # Notification ========================================    
    def update(self, value):
        """
            Update the value and notify the fields that depends on this field to update their value too.
            @param (string)value: the value to be updated to.
        """
        self.value = value
        for field in self.boundElements:
            field.notify()


    def notify(self):
        """
            Called when the base field is modified in order to update the size.
            Default: do nothing.
        """
        pass


    # Fuzzing =============================================
    def preForecast(self):
        """
            Prepare the forecasts. 
        """
        self.fuzzNumber = 0
        self.overflowNumber = 0


    def forecast(self):
        """
            Return the number of fuzz-case it can produce for this element.
        """
        return self.fuzzNumber


    def forecastOverflow(self):
        """
            Return the number of overflow-case it can produce for this element.
        """
        return self.overflowNumber
        

    def fuzz(self, steps):
        """
            Basic fuzzing.
            @param (int)steps: the fuzz-case reference
        """
        pass


    def overflow(self, steps):
        """
            Fuzzing aiming to overflow buffers.
            @param (int)steps
        """
        pass


    def compose(self):
        """
            Make a nested list of subElement's value.
            @return (string or [string] or [[string]])
        """
        return []


    def commit(self):
        """
            Set the working value as current value.
            Recursive.
        """

    def clean(self):
        """
            Set the default value as current value.
            Recursive.
        """
        pass


    # Parsing =============================================
    def parse(self, value):
        """
            Try to parse a value into the element according to its structure.
        """
        pass

