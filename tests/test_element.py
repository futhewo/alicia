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
# Unit-tests of Alicia



# Imports #####################################################################
from nose.tools import *

from alicia.configuration import *
from alicia.element import *
from alicia.utils import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass



# Element #####################################################################
def test_Element___init__():
    global elementId
    elementId = 0
    element0 = Element()
    assert_equals(element0.elementId        , 0)
    assert_equals(element0.type             , "Element")
    assert_equals(element0.name             , "Element 0")
    assert_equals(element0.static           , False)
    assert_equals(element0.weight           , 1.0)
    assert_equals(element0.boundElements    , [])
    assert_equals(element0.notifiable       , True)
    assert_equals(element0.parsed           , False)

    element1 = Element(name="My Element", static=True, weight=2.0)
    assert_equals(element1.elementId        , 1)
    assert_equals(element1.type             , "Element")
    assert_equals(element1.name             , "My Element")
    assert_equals(element1.static           , True)
    assert_equals(element1.weight           , 2.0)
    assert_equals(element1.boundElements    , [])
    assert_equals(element1.notifiable       , True)
    assert_equals(element1.parsed           , False)

# setName already tested.

def test_element___str__():
    element0 = Element("My Element")
    assert_equals(str(element0)             , "[My Element]\n") 


# update will be tested with more complete models. 

def test_element_forecast():
    element0 = Element()
    assert_equals(element0.fuzzNumber       , 0)
    assert_equals(element0.overflowNumber   , 0)
    assert_equals(element0.forecast()       , 0)
    assert_equals(element0.forecastOverflow(), 0)
    # To be retested for each subElements.


def test_element_mutation():
    element0 = Element()
    rand = random.Random(0)
    workingList = ["a", "b", "c", "d", "e"]
    assert_equals(element0.mutation(workingList, 1, rand, 2), ["a", "b", None, "d", "e"])


def test_element_swap():
    element0 = Element()
    rand = random.Random(0)
    workingList = ["a", "b", "c", "d", "e"]
    assert_equals(''.join(element0.swap(workingList, 1, rand, 1)), "aecdb")



