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



# Node ########################################################################
class Node(Element):
    """
        A node element. It has subelements.
        Manipulating means playing with its subelements.
        Ultimately it concats its subelements.
    """

    # Constructor =========================================
    def __init__(self, subElements, name=None, static=False, weight=1.0):
        self.defaultSubElements = subElements
        self.currentSubElements = copy.copy(self.defaultSubElements)
        self.futureSubElements = copy.copy(self.defaultSubElements)

        Element.__init__(self, name, static, weight)

        self.type = "Node"
        self.setName(name)


    # Actioners ===========================================
    def getSize(self):
        """
            Concatenate the size of all subElements.
        """
        size = 0
        for subElement in self.currentSubElements:
            size += subElement.getSize()
        return size


    # Built-ins ===========================================
    def __str__(self):
        string = "[{0}]\n".format(self.name)
        if len(self.currentSubElements) > 0:
            string += self.recursive_str()
        return string


    def recursive_str(self):
        """
            Return a string representing the elements. I want something like that :
            [Element 1]
                [SubElement a]
                    [SubSubElement i]
                    [SubSubElement ii]
                [SubElement b]
            Recursive
            @return (string)representation
        """
        string = ""
        # Recursive call over the subElements
        for subElement in self.currentSubElements:
            substr = str(subElement)
            for line in substr.split("\n"):
                if len(line) > 0: # For null lines.
                    string += "\t" + line + "\n"
        return string 


    # Fuzzing =============================================
    def preForecast(self):
        self.ownFuzzNumber = int(self.weight * configuration.fuzzingNumber)
        self.ownOverflowNumber = int(self.weight * configuration.overflowNumber)

        self.fuzzNumber = self.ownFuzzNumber
        self.overflowNumber = self.ownOverflowNumber


        if len(self.currentSubElements) > 0:
            # Make a table with the steps for each subElement.
            self.subElementsFuzzSteps = []
            self.subElementsOverflowSteps = []
            for subElement in self.currentSubElements:
                self.subElementsFuzzSteps.append(subElement.fuzzNumber)
                self.fuzzNumber += subElement.fuzzNumber

                self.subElementsOverflowSteps.append(subElement.overflowNumber)
                self.overflowNumber += subElement.overflowNumber


    def getSubElementAfterFuzzSteps(self, steps):
        """
            Return the subElement in which the steps lead, and the steps remaining.
            @param (int)steps
            @return ((int)subElement index, (int)remaining steps)
        """
        remainingSteps = steps - self.ownFuzzNumber
        assert(remainingSteps >= 0)
        assert(len(self.currentSubElements) > 0)

        subElementIndex = 0
        while remainingSteps >= self.subElementsFuzzSteps[subElementIndex]:
            remainingSteps -= self.subElementsFuzzSteps[subElementIndex]
            subElementIndex += 1
        return (subElementIndex, remainingSteps)


    def getSubElementAfterOverflowSteps(self, steps):
        """
            Return the subElement in which the steps lead, and the steps remaining.
            @param (int)steps
            @return ((int)subElement index, (int)remaining steps)
        """
        remainingSteps = steps - self.ownOverflowNumber
        assert(remainingSteps >= 0)
        assert(len(self.currentSubElements) > 0)

        subElementIndex = 0
        while remainingSteps >= self.subElementsOverflowSteps[subElementIndex]:
            remainingSteps -= self.subElementsOverflowSteps[subElementIndex]
            subElementIndex += 1
        return (subElementIndex, remainingSteps)


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

        
    def compose(self):
        """
            Compose a protocol and returns the list of all its elements' subvalues.
            Will be overwritten for final elements.
            Recursive.
            @return (string or [string] or [[string]])
        """
        strings = []
        for subElement in self.currentSubElements:
            strings.append(subElement.compose())
        return strings


    def newFuzzedSubElement(self, rand):
        """
            Generate and return a new subElement according to the given random parameters.
            @param (random.Random)rand
        """
        index = rand.randint(0, len(self.defaultSubElements) - 1)
        return copy.copy(self.defaultSubElements[index])


    def nodeFuzz(self, steps):
        """
            Fuzz the node by moving the subelements.
            @param (int)steps: the fuzz-case reference
        """
        Element.fuzz(self, steps)
        rand = random.Random(steps)

        indexes = generateIndexes(len(self.currentSubElements), rand, configuration.randomness)
        for index in indexes:
            if index < 0:
                # removed index
                continue
            if len(self.currentSubElements) == 0:
                # If no elements, we can do nothing
                return
            # Select the mutation kind
            oracle = rand.choice([ADD, MUTATION, SWAP, REMOVE])

            # Mutation
            if oracle == ADD:
                self.currentSubElements = self.add(self.currentSubElements, rand, index, indexes)

            elif oracle == MUTATION:
                self.currentSubElements = self.mutation(self.currentSubElements, rand, index)

            elif oracle == SWAP:
                self.currentSubElements = self.swap(self.currentSubElements, rand, index)

            elif oracle == REMOVE:
                self.currentSubElements = self.remove(self.currentSubElements, rand, index, indexes)


    def nodeOverflow(self, steps):
        """
            Repeat a specific subElement a high number of times. The aim is to overflow buffers.
            @param (int)steps
        """
        pass


    def clean(self):
        """
            Set all subElements to their default value.
            Recursive.
        """
        self.currentSubElements = copy.copy(self.defaultSubElements)
        # Recursive call over the subElements
        for subElement in self.currentSubElements:
            subElement.clean()


    def commit(self):
        """
            Set all subElements to their future value.
            Recursive.
        """
        self.currentSubElements = copy.copy(self.futureSubElements)
        # Recursive call over the subElements
        for subElement in self.currentSubElements:
            subElement.commit()


    # Parsing =============================================
    def parse(self, value, backward=False, root=False):
        pass
