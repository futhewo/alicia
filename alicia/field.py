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
from alicia.utils import *



# Field ########################################################################
class Field(Element):
    """
        A leaf element. Has a value.
        Manipulating him means modifying its value.
    """

    # Constructor =========================================
    def __init__(self, default, minSize=0, maxSize=0, values=None, name=None, fuzzing=None, overflowing=None, randoming=None, fuzzingNumber=None, overflowNumber=None, randomRate=None, randomNumber=None):
        Element.__init__(self, name, fuzzing, overflowing, randoming, fuzzingNumber, overflowNumber, randomRate, randomNumber)
        
        if name is None:
            self.name = "Field {0}".format(self.elementId)
        self.type = "Field"      
 
        if values == None:
            values = []
        
        # Usual and default values
        self.values = values                # Usual values
        self.default = default              # Default value
        self.value = default                # Current value
        # The default value is the first of the usual values.
        #if default not in self.values:
        self.values.insert(0, default)
       
        # Managing sizes 
        self.minSize = minSize              # Size in bytes
        self.maxSize = maxSize
        
        # Some control over size.
        if self.maxSize == 0:
            self.maxSize = len(self.default)
        assert(self.maxSize >= len(self.default) >= self.minSize >= 0)

        # Define the characters allowed and specific for this type
        self.usualChars     = "" 
        self.specialChars   = ""
        self.attackVectors  = [] 
        
        # Sets the steps variable.
        self.makeSteps()


    # Actioners ===========================================
    def getLength(self):
        return len(self.value)


    # Built-ins ===========================================
    def __str__(self):
        """
            Return a string representing the element.
            @return (string)representation
        """
        string = "[{0}]: ({1}:{2}) [".format(self.name, str(self.minSize), str(self.maxSize))
        string += ", ".join(self.values) + "]\n"
        return string


    # Fuzzing =============================================
    def forecast(self):
        """
            Steps are a way to identify each fuzz case. 
            For understanding, the configuration will give a number of fuzz-cases, which are dubbed 'steps'.
            Compute the number of fuzz-cases (steps) this element can produce according to the configuration.
        """
        self.makeSteps() 
        return self.stepsNumber


    def makeSteps(self):
        """
            Make the computation for steps 
        """
        self.stepsNumber = len(self.values)    # Default step

        # Make a table with the steps for each type of fuzzing.
        self.steps = [len(self.values), 0, 0, 0]
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


    def fuzz(self, steps):
        """
            Fuzz the element. The element is then modified.
            @param (int)steps
        """
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


    def compose(self):
        """
            Return the value of a field.
        """
        return self.value


    def nope(self, steps):
        """
            Return a standard value.
        """
        debug(">[{0}] {1} (F): Noping.".format(steps, self.name), conf.verbose)
        self.update(self.values[steps % len(self.values)])


    def basic(self, steps, singleChar=False):
        """
            Fuzz, through mutation, the predefined values.
        """
        assert(len(self.values) > 0)

        r = random.Random(steps)
        
        fuzzedValue = self.values[r.randint(0, len(self.values) - 1)]
        listedValue = list(fuzzedValue)
        
        # Determine a list of indexes that will be fuzzed. 
        indexes = []
        for index in range(len(listedValue)):
            if r.randint(0, 99) < self.randomRate:
                indexes.append(index)
        
        if len(indexes) == 0:
            # In order to have at least one fuzzed element.
            if len(listedValue) == 0:
                indexes.append(0)
            else:
                indexes.append(r.randint(0, len(listedValue) - 1))

        for index in indexes:
            if index == -1:
                # removed index
                continue
             
            # Select the mutation kind
            mutation = 0
            if len(listedValue) == 0:
                # If no elements, we can only add one.
                if len(self.attackVectors) > 0:
                    choice = r.randint(0, 1)
                    if choice == 1:
                        mutation = SNIPEADD
                    else:
                        mutation = ADDING
                else:
                    mutation = ADDING
            else:
                if len(self.attackVectors) > 0:
                    # If we have attack vectors, we try to use them.
                    if len(listedValue) == 1 or singleChar:
                        # It is pointless to move an element if he is alone.
                        # It is pointless to move a char if they are all identics
                        mutation = r.randint(1, 6)
                    else:
                        mutation = r.randint(0, 6)
                else:
                    if len(listedValue) == 1 or singleChar:
                        mutation = r.randint(1, 4)
                    else:
                        mutation = r.randint(0, 4)

            # Generate a random character.
            newChar = ""
            if mutation == MUTATION or mutation == ADDING:
                if self.usualChars is not "":
                    if self.specialChars is not "":
                        useSpecialChars = r.randint(0, 1)
                        if useSpecialChars == 1:
                            newChar = r.choice(self.specialChars)
                        else:
                            newChar = r.choice(self.usualChars)
                    else:
                        newChar = r.choice(self.usualChars)
                else:
                    if self.specialChars is not "":
                        useSpecialChars = r.randint(0, 1)
                        if useSpecialChars == 1:
                            newChar = r.choice(self.specialChars)
                        else:
                            newChar = chr(r.randint(0, 255))
                    else:
                        newChar = chr(r.randint(0, 255))
          
            if mutation == SNIPEADD or mutation == SNIPEMUTE:
                newChar = r.choice(self.attackVectors)
           
            if mutation == MUTATION:
                assert(len(listedValue) > index >= 0)
                debug(">[{0}] {1} (F): Modifying {2} ({3}) to {4}".format(steps, self.name, index, repr(listedValue[index]), repr(newChar)), conf.verbose)
                
                listedValue[index] = newChar

            elif mutation == REMOVING:
                assert(len(listedValue) > index >= 0)
                debug(">[{0}] {1} (F): Removing {2} ({3})".format(steps, self.name, index, repr(listedValue[index])), conf.verbose)
                
                listedValue.pop(index)
                
                # Rectify all other indexes to take into account the removal of this one.
                for i in range(len(indexes)):
                    if indexes[i] > index:
                        indexes[i] -= 1

            elif mutation == ADDING:
                assert(len(listedValue) >= index >= 0)
                debug(">[{0}] {1} (F): Adding {3} in {2}".format(steps, self.name, index, repr(newChar)), conf.verbose)
                
                listedValue.insert(index, newChar)
                
                # Rectify all other indexes to take into account the adding of this one.
                for i in range(len(indexes)):
                    if indexes[i] > index:
                        indexes[i] += 1

            elif mutation == REPEAT:
                assert(len(listedValue) > index >= 0)
                numberOfTimes = r.randint(1, conf.charRepeat)
                repeatingChars = ""
                baseChar = listedValue[index]
                debug(">[{0}] {1} (F): Repeating {2} ({4}) {3} times".format(steps, self.name, index, numberOfTimes, repr(listedValue[index])), conf.verbose)
                
                repeatingChars = baseChar * numberOfTimes
                listedValue = listedValue[:index] + list(repeatingChars) + listedValue[index:]
                 
                # Rectify all other indexes to take into account the repetition of this one.
                for i in range(len(indexes)):
                    if indexes[i] > index:
                        indexes[i] += numberOfTimes

            elif mutation == MOVING:
                assert(len(listedValue) > 1)
                assert(index >= 0)
                newIndex = r.randint(0, len(listedValue) - 1)
                debug(">[{0}] {1} (F): Moving {2} ({4}) to {3}".format(steps, self.name, index, newIndex, repr(listedValue[index])), conf.verbose)
                
                # This poor hack definitely favored the switch of two consecutive elements, which is clearly a good thing eventually.
                if newIndex == index:
                    newIndex = (newIndex + 1) % (len(listedValue) - 1)
                listedValue.insert(newIndex, listedValue.pop(index))
                
                # Rectify all other indexes to take into account the move of this one.
                for i in range(len(indexes)):
                    if indexes[i] > index and indexes[i] >= newIndex:
                        # +1 -1
                        pass
                    elif indexes[i] > index:
                        indexes[i] -= 1
                    elif indexes[i] >= newIndex:
                        indexes[i] += 1
                    
            elif mutation == SNIPEADD:
                assert(len(listedValue) > index >= 0)
                debug(">[{0}] {1} (F): Snipe-adding {3} in {2}".format(steps, self.name, index, repr(newChar)), conf.verbose)

                # We dumbly add the attack vector.
                listedValue = listedValue[:index] + list(newChar) + listedValue[index:]
                
                # Rectify all other indexes to take into account the adding of this one.
                for i in range(len(indexes)):
                    if indexes[i] > index:
                        indexes[i] += len(newChar)
                
            elif mutation == SNIPEMUTE:
                assert(len(listedValue) > index >= 0)
                debug(">[{0}] {1} (F): Snipe-mutation {3} in {2}".format(steps, self.name, index, repr(newChar)), conf.verbose)

                # We make the attack vector fit in the field.
                if len(newChar) > self.maxSize:
                    # If the field is too small, we reduce the attack vector.
                    listedValue = list(newChar[:self.maxSize])

                    # Remove all other indexes
                    for i in range(len(indexes)):
                        indexes[i] = -1 # -1 means not used (impossible value)

                else:
                    removedElements = 1
                    while index >= len(listedValue) and (len(listedValue) + len(newChar)) > self.maxSize:
                        # We remove as many elements as it is needed to fit the attack vector in.
                        removedElements += 1
                        listedValue.pop(index)
                    if index >= len(listedValue):
                        # Start removing elements before the index.
                        while len(listedValue) + len(newChar) > self.maxSize:
                            listedValue.pop(len(listedValue) - 1)
                            removedElements += 1
                        listedValue += list(newChar)    
                    else:
                        listedValue = listedValue[:index] + list(newChar) + listedValue[index:]
                             
                    # Rectify all other indexes to take into account the adding of this one.
                    for i in range(len(indexes)):
                        if indexes[i] > len(listedValue) - 1: # -1 for the adding of newChar
                            # We won't use this index anymore.
                            indexes[i] = -1 
                        elif indexes[i] > index:
                            # Take into account every element removed.
                            indexes[i] += len(newChar) - removedElements

        self.update(''.join(listedValue))


    def overflow(self, steps):
        """
            Repeat a specific char a high number of times. The aim is to overflow buffers.
            @param (int)steps
        """
        r = random.Random(steps)
        fuzzedValue = self.values[r.randint(0, len(self.values) - 1)]
        index = r.randint(0, len(fuzzedValue) - 1)
        numberOfTimes = r.randint(conf.overflowMin * (steps + 1), conf.overflowMax * (steps + 1)) ** conf.agressivity
        newChar = fuzzedValue[index]
        debug(">[{0}] {1} (F): Overflow by {2} {3}".format(steps, self.name, numberOfTimes, newChar), conf.verbose)
        self.update(fuzzedValue[:index] + newChar * (numberOfTimes - 1) + fuzzedValue[index:])


    def random(self, step):
        """
            Stuff the size with random chars.
        """
        r = random.Random(step)
        value = ""
        size = r.randint(self.minSize, self.maxSize)
        for j in range(size):
            if self.usualChars is not "": # If characters are forced.
                value += r.choice(self.usualChars)
            else:
                value += chr(r.randint(0, 255))
        debug(">[{0}] {1} (F): Random".format(steps, self.name), conf.verbose)
        self.update(value)


    def clean(self):
        """
            Clean the field after having fuzzed it.
        """
        self.value = self.default
        self.notifiable = True


    # Parsing =============================================
    def parse(self, value, backward=False, root=False):
        self.parsed = True
        finalValue = ""
        eatingSize = 0
        if self.minSize == self.maxSize:
            eatingSize = self.minSize
        else:
            for boundElement in self.boundElements:
                if boundElement.type == "SizeField":
                    assert(boundElement.parsed)
                    eatingSize = min(self.maxSize, len(value), boundElement.remainingSize)
                    for boundElement in self.boundElements:
                        boundElement.remainingSize -= eatingSize
                    break
                    # Don't care if in several boundElements

        assert(len(value) >= eatingSize)
        if backward:
            # Eat at the end
            finalValue = value[:-eatingSize]
            self.value = value[-eatingSize:]
        else:
            # Eat at the beginning
            finalValue = value[eatingSize:]
            self.value = value[:eatingSize]

        if root:
            assert(len(finalValue) == 0)
        return finalValue


    def parseClean(self):
        self.parsed = False

