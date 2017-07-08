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
from alicia.node import *
from alicia.element import *
from alicia.close_field import *
from alicia.string_content import *
from alicia.integer_content import *
from alicia.utils import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass



# Node ########################################################################
def test_Node___init__():
    global elementId
    elementId = 0
    element0 = Element()
    node0 = Node([element0])
    assert_equals(node0.elementId           , 1)
    assert_equals(node0.type                , "Node")
    assert_equals(node0.name                , "Node 1")
    assert_equals(node0.static              , False)
    assert_equals(node0.weight              , 1.0)
    assert_equals(node0.defaultSubElements  , [element0])
    assert_equals(node0.currentSubElements  , [element0])
    assert_equals(node0.futureSubElements   , [element0])


    element1 = Element()
    node1 = Node([element0, element1], name="My Node", static=True, weight=2.5)
    assert_equals(node1.elementId           , 3)
    assert_equals(node1.type                , "Node")
    assert_equals(node1.name                , "My Node")
    assert_equals(node1.static              , True)
    assert_equals(node1.weight              , 2.5)
    assert_equals(node1.defaultSubElements  , [element0, element1])
    assert_equals(node1.currentSubElements  , [element0, element1])
    assert_equals(node1.futureSubElements   , [element0, element1])


def test_Node___str__():
    element0 = Element(name="Element 0")
    element1 = Element(name="Element 1")
    node0 = Node([element0], "Node 0")
    node1 = Node([node0, element1], "Node 1")
    node2 = Node([], "Node 2")
    node3 = Node([node1, node2], "Node 3")
    
    assert_equals(str(node0)            , "[Node 0]\n\t[Element 0]\n")
    assert_equals(str(node1)            , "[Node 1]\n\t[Node 0]\n\t\t[Element 0]\n\t[Element 1]\n")
    assert_equals(str(node3)            , "[Node 3]\n\t[Node 1]\n\t\t[Node 0]\n\t\t\t[Element 0]\n\t\t[Element 1]\n\t[Node 2]\n")


def test_Node_preforecast():
    configuration.fuzzingNumber = 3
    configuration.overflowNumber = 2

    content0 = StringContent("ABCDE")
    content1 = IntegerContent(32)
    element0 = CloseField(content0)
    element1 = CloseField(content1)
    node0 = Node([element0])
    node1 = Node([node0, element1])
    node2 = Node([])
    node3 = Node([node1, node2])

    assert_equals(node0.fuzzNumber      , 6)
    assert_equals(node1.fuzzNumber      , 12)
    assert_equals(node2.fuzzNumber      , 3)
    assert_equals(node3.fuzzNumber      , 18)
    assert_equals(node3.ownFuzzNumber   , 3)
    assert_equals(node3.subElementsFuzzSteps, [12, 3])

    assert_equals(node0.overflowNumber  , 4)
    assert_equals(node1.overflowNumber  , 8)
    assert_equals(node2.overflowNumber  , 2)
    assert_equals(node3.overflowNumber  , 12)
    assert_equals(node3.ownOverflowNumber, 2)
    assert_equals(node3.subElementsOverflowSteps, [8, 2])


def test_Node_getSubElementAfterFuzzSteps():
    configuration.fuzzingNumber = 3
    content0 = StringContent("ABCDE")
    content1 = IntegerContent(32)
    element0 = CloseField(content0)
    element1 = CloseField(content1)
    node0 = Node([element0])
    node1 = Node([node0, element1])
    node2 = Node([])
    node3 = Node([node1, node2])
    
    node3.preForecast()
    subElementIndex0, remainingSteps0 = node3.getSubElementAfterFuzzSteps(3)
    assert_equals(subElementIndex0      , 0) # node1
    assert_equals(remainingSteps0       , 0)

    subElementIndex1, remainingSteps1 = node3.getSubElementAfterFuzzSteps(7)
    assert_equals(subElementIndex1      , 0) # node0
    assert_equals(remainingSteps1       , 4)

    subElementIndex2, remainingSteps2 = node3.getSubElementAfterFuzzSteps(11)
    assert_equals(subElementIndex2      , 0) # element0
    assert_equals(remainingSteps2       , 8)

    subElementIndex3, remainingSteps3 = node3.getSubElementAfterFuzzSteps(13)
    assert_equals(subElementIndex3      , 0) # element1
    assert_equals(remainingSteps3       , 10)

    subElementIndex4, remainingSteps4 = node3.getSubElementAfterFuzzSteps(15)
    assert_equals(subElementIndex4      , 1) # node2
    assert_equals(remainingSteps4       , 0)


def test_Node_getSubElementAfterOverflowSteps():
    configuration.overflowNumber = 3
    content0 = StringContent("ABCDE")
    content1 = IntegerContent(32)
    element0 = CloseField(content0)
    element1 = CloseField(content1)
    node0 = Node([element0])
    node1 = Node([node0, element1])
    node2 = Node([])
    node3 = Node([node1, node2])
    
    node3.preForecast()
    subElementIndex0, remainingSteps0 = node3.getSubElementAfterOverflowSteps(3)
    assert_equals(subElementIndex0      , 0) # Node1
    assert_equals(remainingSteps0       , 0)

    subElementIndex1, remainingSteps1 = node3.getSubElementAfterOverflowSteps(7)
    assert_equals(subElementIndex1      , 0) # Node0
    assert_equals(remainingSteps1       , 4)

    subElementIndex2, remainingSteps2 = node3.getSubElementAfterOverflowSteps(11)
    assert_equals(subElementIndex2      , 0) # Element0
    assert_equals(remainingSteps2       , 8)

    subElementIndex3, remainingSteps3 = node3.getSubElementAfterOverflowSteps(13)
    assert_equals(subElementIndex3      , 0) # Element1
    assert_equals(remainingSteps3       , 10)

    subElementIndex4, remainingSteps4 = node3.getSubElementAfterOverflowSteps(15)
    assert_equals(subElementIndex4      , 1) # Node2
    assert_equals(remainingSteps4       , 0)


def test_Node_compose():
    content0 = StringContent("ABCDE")
    element0 = CloseField(content0)
    content1 = IntegerContent(32)
    element1 = CloseField(content1)
    node0 = Node([element0, element1])
    assert_equals(node0.compose()       , ["ABCDE", "\x00\x00\x00 "])


def test_Node_nodeFuzz():
    configuration.fuzzing = 100
    content0 = StringContent("ABCDE")
    element0 = CloseField(content0)
    content1 = IntegerContent(32)
    element1 = CloseField(content1)
    node0 = Node([element0, element1])

    # Mutation
    node0.fuzz(0)
    assert_equals(node0.compose()       , ["\x00\x00\x00 ", "\x00\x00\x00 "])
    node0.clean()    

    # Remove
    node0.nodeFuzz(1)
    assert_equals(node0.compose()       , ["\x00\x00\x00 "])
    node0.clean()    

    # Add
    node0.nodeFuzz(2)
    assert_equals(node0.compose()       , ['\x00\x00\x00 ', "ABCDE", "\x00\x00\x00 "])
    node0.clean()  

    # Swap
    node0.nodeFuzz(3)
    assert_equals(node0.compose()       , ["\x00\x00\x00 ", "ABCDE"])

    # Remove 1 (previously only 0 was impacted)
    node0.nodeFuzz(5)
    assert_equals(node0.compose()       , ["\x00\x00\x00 "])


def test_Node_newFuzzedSubElement():
    content0 = StringContent("ABCDE")
    element0 = CloseField(content0)
    content1 = IntegerContent(32)
    element1 = CloseField(content1)
    node0 = Node([element0, element1])

    rand = random.Random(0)
    assert_equals(node0.newFuzzedSubElement(rand).compose(), element1.compose())

    rand = random.Random(1)
    assert_equals(node0.newFuzzedSubElement(rand).compose(), element0.compose())


def test_Node_fuzz():
    configuration.fuzzingNumber = 10
    content0 = StringContent("ABCDE")
    element0 = CloseField(content0)
    content1 = IntegerContent(32)
    element1 = CloseField(content1)
    node0 = Node([element0, element1])

    # NodeFuzz : Mutation
    node0.fuzz(0)
    assert_equals(node0.compose()       , ["\x00\x00\x00 ", "\x00\x00\x00 "])
    node0.clean()    

    # Field fuzz
    node0.fuzz(10)
    assert_equals(node0.compose()       , ["ABCWE", "\x00\x00\x00 "])
    node0.clean()    

    # Field fuzz
    node0.fuzz(20)
    assert_equals(node0.compose()       , ["ABCDE", "\x00\x00\x00 "])
    node0.clean()    


def test_Node_clean():
    content0 = StringContent("ABCDE")
    element0 = CloseField(content0)
    content1 = IntegerContent(32)
    element1 = CloseField(content1)
    node0 = Node([element0, element1])

    element0.fuzz(0)
    element1.fuzz(0)
    node0.currentElement = [element1, element0]
    node0.clean()

    assert_equals(node0.compose()       , ["ABCDE", "\x00\x00\x00 "])

