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
import copy

from alicia.element import *
from alicia.node import *



# Choice ######################################################################
class Choice(Node):
    """
        A node element. It has subelements.
        Manipulating means playing with its subelements.
        Ultimately it chosses one of its subelements.
    """

    # Constructor =========================================
    def __init__(self, subElements, choice=0, name=None, static=False, weight=1.0):
        Node.__init__(self, subElements, name, static, weight)

        self.type = "Choice"
        self.setName(name)

        assert(choice < len(subElements))
        self.defaultChoice = choice
        self.currentChoice = choice
        self.futureChoice = choice


    # Actioners ===========================================
    def getSize(self):
        """
            Return the size of the current choice.
        """
        return self.currentSubElements[self.currentChoice].getSize()


    # Built-ins ===========================================
    # Fuzzing =============================================
    def fuzz(self, steps):
        """
            Choose between fuzzing the node or one of its subElements.
            @param (int)steps
        """
        assert type(steps) == int
        assert(steps >= 0)

        # Element fuzzing
        if steps < self.ownFuzzNumber:
            self.nodeFuzz(steps)
        
        # SubElements fuzzing
        else:
            assert(len(self.currentSubElements) > 0)
            # Get the subElement to fuzz
            (subElementIndex, remainingStep) = self.getSubElementAfterFuzzSteps(steps)
            # Fuzz it
            self.currentSubElements[subElementIndex].fuzz(remainingStep)
            self.currentChoice = subElementIndex
        self.pushNotification()


    def overflow(self, steps):
        """
            Choose between overflowing the node or one of its subElements.
            @param (int)steps
        """
        assert type(steps) == int
        assert(steps >= 0)

        # Element fuzzing
        if steps < self.ownOverflowNumber:
            self.nodeOverflow(steps)

        # SubElements fuzzing
        else:
            assert(len(self.currentSubElements) > 0)
            # Get the subElement to fuzz
            (subElementIndex, remainingStep) = self.getSubElementAfterOverflowSteps(steps)
            # Fuzz it
            self.subElements[subElementIndex].overflow(remainingStep)
            self.currentChoice = subElementIndex
        self.pushNotification()

        
    def compose(self):
        """
            @return (string or [string] or [[string]])
        """
        return self.currentSubElements[self.currentChoice].compose()


    def nodeFuzz(self, steps):
        """
            Choose a subElement.
            @param (int)steps: the fuzz-case reference
        """
        Element.fuzz(self, steps)
        rand = random.Random(steps)

        if len(self.currentSubElements) == 0:
            # If no elements, we can do nothing
            return
            # Select the mutation kind
        self.currentChoice = rand.randint(0, len(self.currentSubElements) - 1)


    def nodeOverflow(self, steps):
        """
            Repeat a specific subElement a high number of times. The aim is to overflow buffers.
            @param (int)steps
        """
        pass


    def clean(self):
        Node.clean(self)
        self.currentChoice = self.defaultChoice
        self.pushNotification()


    def commit(self):
        Node.commit(self)
        self.currentChoice = self.futureChoice
        self.pushNotification()


    # Parsing =============================================
    def parse(self, value, backward=False, root=False):
        pass
