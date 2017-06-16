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

from alicia.element import *
from alicia.static_field import *
from alicia.utils import *



# Node ########################################################################
class Node(Element):
    """
        A node element. It has subelements.
        Manipulating means playing with its subelements.
    """

    # Constructor =========================================
    def __init__(self, subElements=[], name=None, fuzzing=None, overflowing=None, randoming=None, fuzzingNumber=None, overflowNumber=None, randomRate=None, randomNumber=None):
        Element.__init__(self, name, fuzzing, overflowing, randoming, fuzzingNumber, overflowNumber, randomRate, randomNumber)
       
        if name is None:
            self.name = "Node {0}".format(self.elementId)
        self.node = "Node"    
    
        self.defaultSubElements = subElements
        self.subElements = copy.copy(self.defaultSubElements)
        self.makeSteps()
        # TODO check according to previous version


    # Actioners ===========================================
    # Built-ins ===========================================
    def __str__(self):
        string = "[{0}]\n".format(self.name)
        if len(self.subElements) > 0:
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
        for subElement in self.subElements:
            substr = str(subElement)
            for line in substr.split("\n"):
                if len(line) > 0: # For null lines.
                    string += "\t" + line + "\n"
        return string 

    # Fuzzing =============================================
    def forecast(self):
        """
            Steps are a way to identify each fuzz case. 
            For understanding, the configuration will give a number of fuzz-cases, which are dubbed 'steps'.
            Compute the number of fuzz-cases (steps) this element can produce according to the configuration.
        """
        self.makeSteps()
        return self.totalStepsNumber


    def makeSteps(self):
        """
            Make the computation for steps 
        """
        self.stepsNumber = 1        # Default step
        self.totalStepsNumber = 1   # Including the subElementSteps

        # Make a table with the steps for each type of fuzzing.
        self.steps = [1, 0, 0, 0]
        if self.fuzzing:
            self.stepsNumber += self.fuzzingNumber
            self.steps[FUZZING]   = self.fuzzingNumber
        if self.overflowing:
            self.stepsNumber += self.overflowNumber
            self.steps[OVERFLOWING]= self.overflowNumber
        if self.randoming:
            self.stepsNumber += self.randomNumber
            self.steps[RANDOMING] = self.randomNumber
        
        self.totalStepsNumber = self.stepsNumber
        if len(self.subElements) > 0:
            # Make a table with the steps for each subElement.
            self.subElementsSteps = []
            for subElement in self.subElements:
                self.subElementsSteps.append(subElement.totalStepsNumber)
                self.totalStepsNumber += subElement.totalStepsNumber 


    def getSubElementAfterSteps(self, steps):
        """
            Return the subElement in which the steps lead, and the steps remaining.
            @param (int)steps
            @return ((int)subElement index, (int)remaining steps)
        """
        remainingSteps = steps - self.stepsNumber # Remove the element steps.
        assert(remainingSteps >= 0)
        assert(len(self.subElements) > 0)

        subElementIndex = 0
        while remainingSteps >= self.subElementsSteps[subElementIndex]:
            remainingSteps -= self.subElementsSteps[subElementIndex]
            subElementIndex += 1
        return (subElementIndex, remainingSteps)


    def fuzz(self, steps):
        """
            Fuzz the element. The element is then modified.
            @param (int)steps
        """
        assert type(steps) == int
        assert(steps >= 0)

        # Element fuzzing
        if steps < self.stepsNumber:
            (fuzzType, remainingSteps) = self.getFuzzTypeAfterSteps(steps)
            if fuzzType == NOPE:
                self.nope(remainingSteps)
            elif fuzzType == FUZZING:
                self.basic(remainingSteps)
            elif fuzzType == OVERFLOWING:
                self.overflow(remainingSteps)
            elif fuzzType == RANDOMING:
                self.random(remainingSteps)
        
        # SubElements fuzzing
        else:
            assert(len(self.subElements) > 0)
            # Get the subElement to fuzz
            (subElementIndex, remainingStep) = self.getSubElementAfterSteps(steps)
            # Fuzz it
            self.subElements[subElementIndex].fuzz(remainingStep)


        
    def compose(self):
        """
            Compose a protocol and returns the list of all its elements' subvalues.
            Will be overwritten for final elements.
            Recursive.
            @return (string or [string] or [[string]])
        """
        strings = []
        for subElement in self.subElements:
            strings.append(subElement.compose())
        return strings


    def nope(self, steps):
        """
            Return a standard value.
            @param (int)steps: the standard value reference
        """
        # Do nothing
        debug(">[{0}] {1} (N): Noping.".format(steps, self.name), conf.verbose)


    def basic(self, steps, singleChar=False):
        """
            Move the subelements.
            @param (int)steps: the fuzz-case reference
        """
        r = random.Random(steps)
        
        # Determine a list of indexes that will be fuzzed. 
        indexes = []
        for index in range(len(self.subElements)):
            if r.randint(0, 99) < self.randomRate:
                indexes.append(index)
        
        # In order to have at least one fuzzed element. 
        if len(indexes) == 0:
            indexes.append(r.randint(0, len(self.subElements) - 1))

        for index in indexes: 
            # Generate a random classic subElement.
            newSubElementIndex = r.randint(0, len(self.subElements) - 1) # Choosing a random subElement
            newSubElement = copy.copy(self.subElements[newSubElementIndex])

            # Select the mutation kind
            mutation = 0
            if len(self.subElements) == 0:
                # If no elements, we can only add one.
                mutation = ADDING
            elif len(self.subElements) == 1:
                # It is pointless to move an element if he is alone.
                mutation = r.randint(1, 4)
            else:
                mutation = r.randint(0, 4)
           
            
            if mutation == MUTATION:
                assert(len(self.subElements) > index >= 0)
                self.subElements[index] = copy.copy(newSubElement)
                debug(">[{0}] {1} (N): Modifying {2}".format(steps, self.name, index), conf.verbose)
            
            elif mutation == REMOVING:
                assert(len(self.subElements) > index >= 0)
                self.subElements.pop(index)

                # Rectify all other indexes to take into account the removal of this one.
                for i in range(len(indexes)):
                    if indexes[i] > index:
                        indexes[i] -= 1
                debug(">[{0}] {1} (N): Removing {2}".format(steps, self.name, index), conf.verbose)
            
            elif mutation == ADDING:
                #TODO: for now it is only copying another element. It would be better if it was able to create a new one from what he knows of all the elements' structure.
                assert(len(self.subElements) > index >= 0)
                self.subElements.insert(index, newSubElement)
                
                # Rectify all other indexes to take into account the adding of this one.
                for i in range(len(indexes)):
                    if indexes[i] > index:
                        indexes[i] += 1
                debug(">[{0}] {1} (N): Adding in {2}".format(steps, self.name, index), conf.verbose)
                 
            elif mutation == REPEAT:
                assert(len(self.subElements) > index >= 0)
                
                numberOfTimes = r.randint(1, conf.subElemRepeat)
                repeatingSubElements = []
                baseSubElement = self.subElements[index]
                for i in range(numberOfTimes):
                    repeatingSubElements.append(copy.copy(baseSubElement))
                self.subElements = self.subElements[:index] + repeatingSubElements + self.subElements[index:]
                
                # Rectify all other indexes to take into account the repetition of this one.
                for i in range(len(indexes)):
                    if indexes[i] > index:
                        indexes[i] += numberOfTimes
                debug(">[{0}] {1} (N): Repeating {2} {3} times".format(steps, self.name, index, numberOfTimes), conf.verbose)
            
            elif mutation == MOVING:
                assert(len(self.subElements) > 1) # No point to move it if there is only one element.
                assert(index >= 0)

                newIndex = r.randint(0, len(self.subElements))

                # This poor hack definitely favored the switch of two consecutive elements, which is clearly a good thing eventually.
                if newIndex == index:
                    newIndex = (newIndex + 1) % (len(self.subElements) - 1)
                self.subElements.insert(newIndex, self.subElements.pop(index))
                
                # Rectify all other indexes to take into account the move of this one.
                for i in range(len(indexes)):
                    if indexes[i] > index and indexes[i] >= newIndex:
                        # +1 -1
                        pass
                    elif indexes[i] > index:
                        indexes[i] -= 1
                    elif indexes[i] >= newIndex:
                        indexes[i] += 1
                debug(">[{0}] {1} (N): Moving {2} to {3}".format(steps, self.name, index, newIndex), conf.verbose)


    def overflow(self, steps):
        """
            Repeat a specific subElement a high number of times. The aim is to overflow buffers.
            @param (int)steps
        """
        r = random.Random(steps)
        index = r.randint(0, len(self.subElements) - 1)
        numberOfTimes = r.randint(conf.overflowMin * (steps + 1), conf.overflowMax * (steps + 1)) ** conf.agressivity
        repeatingSubElements = []
        baseSubElement = self.subElements[index]
        for i in range(numberOfTimes):
            repeatingSubElements.append(copy.copy(baseSubElement))
        self.subElements = self.subElements[:index] + repeatingSubElements + self.subElements[index:]

        debug(">[{0}] {1} (N): Overflow {2} by {3}".format(steps, self.name, index, numberOfTimes), conf.verbose)


    def random(self, steps):
        """
            Replace the node with a random node cleverly generated.
            Not implemented yet. 
            @param (int)steps
        """
        #TODO
        pass

    def clean(self):
        """
            Set all subElements to their default value.
            Recursive.
        """
        self.subElements = copy.copy(self.defaultSubElements)
        # Recursive call over the subElements
        for subElement in self.subElements:
            subElement.clean()


    # Parsing =============================================
    def splitOnStaticFields(self, value):
        """
            Split a node and a given value on its StaticFields.
            @param (String)value
            @return (list(ElementBlock))a list of value-list of elements pair, this list is made by parallely cutting the given value on the StaticFields separator and the subElements of the node on its StaticFields.
        """
        currentValue = value
        elements = []
        elementsBlocks = []
        for subElement in self.subElements:
            # Detect StaticField
            if isinstance(subElement, StaticField):
                staticStart = currentValue.find(subElement.value)
                staticEnd = staticStart + len(subElement.value)
                assert(staticStart >= 0) # Found it

                beforeBlock = ElementsBlock(currentValue[:staticStart], elements)
                staticBlock = ElementsBlock(currentValue[staticStart:staticEnd], [subElement])
                elementsBlocks.append(beforeBlock)
                elementsBlocks.append(staticBlock)

                currentValue = currentValue[staticEnd:]
                elements = []
            else:
                elements.append(subElement)
        elementsBlocks.append(ElementsBlock(currentValue, elements))

        return elementsBlocks


    def parse(self, value, backward=False, root=False):
        """
            Parse a value inside the node. It calls the parsing function of all subElements one by one.

            @param (String)value: the value to parse into this node.
            @param (bool)backward: should the parsing be done backward or forward
            @param (boot)root: is the node a root node, if so the entire value has to be parsed, or the parsing would have failed.
        """
        elementsBlocks = self.splitOnStaticFields(value)

        # Loop on the blocks, len(self.subElements) times. After that, all fields should have been parsed
        for i in range(len(self.subElements)): # Optimisation : /2, should think about it
            # Loop through all blocks.
            for elementsBlock in elementsBlocks:
                elements = copy.copy(elementsBlock.elements) # Work copy
                _backward = backward
                # Try both ways
                for way in range(2):
                    # Loop through elements
                    #debug("[" + ",".join(map(lambda x:x.name, elements)) + "]", conf.verbose)
                    for element in elements:
                        try:
                            elementsBlock.value = element.parse(elementsBlock.value, backward=_backward)
                            if backward:
                                elementsBlock.elements.pop(-1)
                            else:
                                elementsBlock.elements.pop(0)
                            debug("[Parsing succeed] {0}: element={3}, backward={1}, value={2}".format(self.name, _backward, elementsBlock.value, element.name), conf.verbose)
                        except AssertionError, e:
                            debug("[Parsing error] {0}: element={3}, backward={1}, value={2}".format(self.name, _backward, elementsBlock.value, element.name), conf.verbose)
                            # Then try backward
                    # Go from forward parsing to backward and vice-versa.
                    _backward = not _backward
                    elements = copy.copy(elementsBlock.elements) # Work copy
                    elements.reverse()

            # Remove empty elementsBlock
            for elementsBlock in elementsBlocks:
                if len(elementsBlock.value) == 0 and len(elementsBlock.elements) == 0:
                    elementsBlocks.remove(elementsBlock)

        for i in range(len(elementsBlocks) - 1):
            elementsBlock = elementsBlocks[i]
            # Everything should have been parsed
            assert(len(elementsBlock.value) == 0)
            assert(len(elementsBlock.elements) == 0)
       
        # Last element, if he exists.
        if len(elementsBlocks) > 0: 
            elementsBlock = elementsBlocks[-1]
            assert(len(elementsBlock.elements) == 0)
            if root:
                assert(len(elementsBlock.value) == 0) # Everything should have been parsed.
            self.parsed = True
            return elementsBlock.value # Return what remains
        else:
            self.parsed = True
            return ""

    def parseClean(self):
        for subElement in self.subElements:
            subElement.parseClean()
        self.parsed = False

