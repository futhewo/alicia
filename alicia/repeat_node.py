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
# Node that repeats its subelement.



# Imports #####################################################################
import random
import string
import copy

from alicia.node import *
from alicia.utils import *



# Node ########################################################################
class RepeatNode(Node):
    """
        A node element. It has one subelement it can repeat up to a given time.
        Manipulating it means playing with its subelement.
    """

    # Constructor =========================================
    def __init__(self, subElement, size, minSize=0, maxSize=1, name=None, fuzzing=None, overflowing=None, randoming=None, fuzzingNumber=None, overflowNumber=None, randomRate=None, randomNumber=None):
        assert(minSize >= 0)
        assert(size >= minSize)
        Node.__init__(self, [], name, fuzzing, overflowing, randoming, fuzzingNumber, overflowNumber, randomRate, randomNumber)
       
        if name is None:
            self.name = "RepeatNode {0}".format(self.elementId)
        self.type = "RepeatNode"
        
        self.size = size
        self.defaultSize = self.size
        self.minSize = minSize
        self.maxSize = maxSize
        if self.maxSize < self.size:
            self.maxSize = self.size

        if self.size > 0:
            self.defaultSubElements.append(subElement)
            # Copy for the others.
            for i in range(self.size - 1):
                self.defaultSubElements.append(copy.copy(subElement))

        self.subElements = copy.copy(self.defaultSubElements)
        self.makeSteps()


    # Actioners ===========================================
    # Built-ins ===========================================
    def __str__(self):
        string = "[{0} [{1}:{2}:{3}]]\n".format(self.name, self.minSize, self.size, self.maxSize)
        if len(self.subElements) > 0:
            string += self.recursive_str()    
        return string


    # Fuzzing =============================================
    def basic(self, steps, singleChar=False):
        """
            Repeat the subelements.
            @param (int)steps: the fuzz-case reference
        """
        r = random.Random(steps)
       
        # Select the mutation kind
        mutation = 0
        if len(self.subElements) == 0:
            # If no elements, we can only add one.
            mutation = ADDING
        else:
            mutation = r.randint(1, 2)

            # Generate a random classic subElement.
            newSubElementIndex = r.randint(0, len(self.subElements) - 1) # Choosing a random subElement
           
        if mutation == REMOVING:
            count = r.randint(1, max(1, len(self.subElements) - self.minSize))
            for i in range(count):
                index = r.randint(0, len(self.subElements) - 1)
                self.subElements.pop(index)
                debug(">[{0}] {1} (N): Removing {2}".format(steps, self.name, index), conf.verbose)
        
        elif mutation == ADDING:
            count = r.randint(1, max(1, self.maxSize - len(self.subElements) + 1)) # Always do at least once
            for i in range(count):
                newSubElement = copy.copy(self.subElements[r.randint(0, len(self.subElements) - 1)])
                index = r.randint(0, len(self.subElements) - 1)
                self.subElements.insert(index, newSubElement)
                debug(">[{0}] {1} (N): Adding in {2}".format(steps, self.name, index), conf.verbose)
        self.size = len(self.subElements)


    # overflow inherited
    # random inherited

    def clean(self):
        """
            Set all subElements to their default value.
            Recursive.
        """
        Node.clean(self)
        self.size = self.defaultSize


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
        # TODO Can be constrained by a count.
        _value = value
 
        # Clean the subElements
        self.subElements = []
        self.size = 0
        # TODO: check size against the min size.

        # While there is things to eat and we are not over the max size.
        while len(_value) > 0 and _count < self.maxSize:
            next_value = _value
            _backward = backward
            # Try both ways
            for way in range(2):
                # Loop through elements
                try:
                    next_value = element.parse(_value, backward=_backward)
                    debug("[Parsing succeed] {0}: element={3}, backward={1}, value={2}".format(self.name, _backward, elementsBlock.value, element.name), conf.verbose)
                except AssertionError, e:
                    debug("[Parsing error] {0}: element={3}, backward={1}, value={2}".format(self.name, _backward, elementsBlock.value, element.name), conf.verbose)
                    # Then try backward
                # Go from forward parsing to backward and vice-versa.
                _backward = not _backward
                next_value = ''.join(list(next_value).reverse()) # Reverse the food.
            _value = next_value

        assert(len(_value) == 0) # Everything should have been parsed. Elsewhere we lacked a condition.
        self.parsed = True
        return ""


    def parseClean(self):
        self.size = self.defaultSize
        self.subElements = self.defaultSubElements
        for subElement in self.subElements:
            subElement.parseClean()
        self.parsed = False

