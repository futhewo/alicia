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

from alicia.configuration import *
from alicia.utils import *



# Element #####################################################################
class Element(object):
    """
        The fuzzer displays all elements on a tree form, all elements of this tree being of this class.
        Be warned that this class represents artificial elements without subElements or value. It is more of an abstract class, even if it can be used.
    """

    # Constructor =========================================
    def __init__(self, name=None, fuzzing=None, overflowing=None, randoming=None, fuzzingNumber=None, overflowNumber=None, randomRate=None, randomNumber=None):

        global elementId
        self.elementId = elementId
        elementId += 1
        self.type = "Element"

        self.name = name
        if name is None:
            self.name = "Element {0}".format(self.elementId)

        # Bound fields
        self.boundElements = []   # Fields that depend on this field.
        self.notifiable = True

        # Getting the default attributes in the current configuration object if they are not defined.
        if fuzzing is None:
            fuzzing = conf.fuzzing
        if overflowing is None:
            overflowing = conf.overflowing
        if randoming is None:
            randoming = conf.randoming
        if fuzzingNumber is None:
            fuzzingNumber = conf.fuzzingNumber
        if overflowNumber is None:
            overflowNumber = conf.overflowNumber
        if randomRate is None:
            randomRate = conf.randomRate
        if randomNumber is None:
            randomNumber = conf.randomNumber
      
        # Configuration attributes 
        self.fuzzing        = fuzzing
        self.overflowing    = overflowing
        self.randoming      = randoming
        self.fuzzingNumber  = fuzzingNumber 
        self.overflowNumber = overflowNumber
        self.randomRate     = randomRate
        self.randomNumber   = randomNumber

        # Control on random rate value
        if randomRate > 100:
            self.randomRate = 100

        self.parsed = False



    # Actioners ===========================================
    # Built-ins ===========================================
    def __str__(self):
        """
            Return a string representing the element.
            @return (string)representation
        """
        string = "[{0}]".format(self.name)
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
    def forecast(self):
        """
            Steps are a way to identify each fuzz case. 
            For understanding, the configuration will give a number of fuzz-cases, which are dubbed 'steps'.
            Compute the number of fuzz-cases (steps) this element can produce according to the configuration.
        """
        return self.totalStepsNumber


    def makeSteps(self):
        """
            Make the computation for steps 
        """
        self.stepsNumber = 1        # Default step
        self.totalStepsNumber = 1   # Including the subElementSteps

        # Make a table with the steps for each type of fuzzing.
        self.steps = [1, 0, 0, 0]

    
    def getFuzzTypeAfterSteps(self, steps):
        """
            Return the fuzz type in which the steps lead, and the steps remaining.
            @param (int)steps
            @return ((int)fuzz type, (int)remaining steps)
        """
        remainingSteps = steps
        assert(self.totalStepsNumber > remainingSteps >= 0)

        fuzzType = 0
        while remainingSteps >= self.steps[fuzzType]:
            remainingSteps -= self.steps[fuzzType]
            fuzzType += 1
        return (fuzzType, remainingSteps)


    def fuzz(self, steps):
        """
            Fuzz the element. The element is then modified.
            For an artificial element, it does nothing though.
            @param (int)steps
        """
        pass
        

    def compose(self):
        """
            Compose a protocol and returns the list of all its elements' subvalues.
            For an artificial element, which has neither value, nor son, it returns nothing. 
            @return (string or [string] or [[string]])
        """
        return []


    def nope(self, steps):
        """
            Return a standard value.
            @param (int)steps: the standard value reference
        """
        pass


    def basic(self, steps, singleChar=False):
        """
            Basic fuzzing.
            @param (int)steps: the fuzz-case reference
            @param (bool)singleChar: tells if there is only one character that can take the final value (for instance paddingField)
        """
        pass


    def overflow(self, steps):
        """
            Fuzzing aiming to overflow buffers.
            @param (int)steps
        """
        pass


    def random(self, steps):
        """
            Strictly random fuzzing.
        """
        pass


    def clean(self):
        """
            Set all subElements to their default value.
            Recursive.
        """
        pass


    # Parsing =============================================
    def parse(self, value):
        """
            Try to parse a value into the element according to its structure.
        """
        pass


    def parseClean(self):
        pass


# ElementsBlock ###############################################################
class ElementsBlock():
    def __init__(self, value, elements):
        self.value = value
        self.elements = elements




