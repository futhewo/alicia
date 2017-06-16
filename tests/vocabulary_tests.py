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
from alicia.node import *
from alicia.repeat_node import *
from alicia.field import *
from alicia.string_field import *
from alicia.integer_field import *
from alicia.size_field import *
from alicia.count_field import *
from alicia.padding_field import *
from alicia.random_field import *
from alicia.static_field import *
from alicia.tlv_field import *
from alicia.utils import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass



# Element #####################################################################
def test_element__init__():
    empty = Element()
    assert_equals(empty.elementId       , 0)
    assert_equals(empty.name            , "Element 0")
    assert_equals(empty.fuzzing         , True)
    assert_equals(empty.overflowing     , True)
    assert_equals(empty.randoming       , False)
    assert_equals(empty.fuzzingNumber   , 100)
    assert_equals(empty.overflowNumber  , 10)
    assert_equals(empty.randomRate      , 20)
    assert_equals(empty.randomNumber    , 100)
    assert_equals(empty.parsed          , False)

    full = Element("My Element", False, False, True, 2000, 200, 50, 200)
    assert_equals(full.elementId        , 1)
    assert_equals(full.name             , "My Element")
    assert_equals(full.fuzzing          , False)
    assert_equals(full.overflowing      , False)
    assert_equals(full.randoming        , True)
    assert_equals(full.fuzzingNumber    , 2000)
    assert_equals(full.overflowNumber   , 200)
    assert_equals(full.randomRate       , 50)
    assert_equals(full.randomNumber     , 200)
    assert_equals(full.parsed           , False)


def test_element__str__():
    empty = Element()
    assert_equals(str(empty)            , "[Element 2]") 


def test_element_makeSteps():
    empty = Element()
    empty.makeSteps()
    assert_equals(empty.stepsNumber     , 1)
    assert_equals(empty.totalStepsNumber, 1)
    assert_equals(empty.steps           , [1, 0, 0, 0])


def test_element_forecast():
    empty = Element()
    empty.makeSteps()
    assert_equals(empty.forecast()      , 1)


def test_element_getFuzzTypeAfterSteps():
    empty = Element()
    empty.makeSteps()
    (fuzzType, remainingSteps) = empty.getFuzzTypeAfterSteps(0)
    assert_equals(fuzzType              , 0)
    assert_equals(remainingSteps        , 0)



# Node ########################################################################
def test_node__init__():
    empty = Node()
    assert_equals(empty.defaultSubElements, [])
    assert_equals(empty.subElements     , [])
    assert_equals(empty.fuzzing         , True)
    assert_equals(empty.overflowing     , True)
    assert_equals(empty.randoming       , False)
    assert_equals(empty.fuzzingNumber   , 100)
    assert_equals(empty.overflowNumber  , 10)
    assert_equals(empty.randomRate      , 20)
    assert_equals(empty.randomNumber    , 100)

    full = Node([empty], "My Element", False, False, True, 2000, 200, 50, 200)
    assert_equals(full.name             , "My Element")
    assert_equals(full.defaultSubElements, [empty])
    assert_equals(full.subElements      , [empty])
    assert_equals(full.defaultSubElements[0].name, empty.name)
    assert_equals(full.subElements[0].name, empty.name)
    assert_equals(full.fuzzing          , False)
    assert_equals(full.overflowing      , False)
    assert_equals(full.randoming        , True)
    assert_equals(full.fuzzingNumber    , 2000)
    assert_equals(full.overflowNumber   , 200)
    assert_equals(full.randomRate       , 50)
    assert_equals(full.randomNumber     , 200)

    # Modify the object
    full.subElements = []
    assert_equals(full.defaultSubElements, [empty])
    assert_equals(full.subElements      , [])
   
     
def test_node__str__():
    node0 = Node([], "Node 0")
    node1 = Node([node0], "Node 1")
    node2 = Node([], "Node 2")
    node3 = Node([node1, node2], "Node 3")
    
    assert_equals(str(node0)            , "[Node 0]\n")
    assert_equals(str(node1)            , "[Node 1]\n\t[Node 0]\n")
    assert_equals(str(node3)            , "[Node 3]\n\t[Node 1]\n\t\t[Node 0]\n\t[Node 2]\n")


def test_node_makeSteps():
    node0 = Node([], "Node 0")
    node1 = Node([node0], "Node 1")
    node2 = Node([], "Node 2")
    node3 = Node([node1, node2], "Node 3")
    
    assert_equals(node0.steps           , [1, 100, 10, 0])
    assert_equals(node0.stepsNumber     , 111)
    assert_equals(node1.stepsNumber     , 111)
    assert_equals(node2.stepsNumber     , 111)
    assert_equals(node3.stepsNumber     , 111)
    
    assert_equals(node0.totalStepsNumber, 111)
    assert_equals(node1.totalStepsNumber, 222)
    assert_equals(node2.totalStepsNumber, 111)
    assert_equals(node3.totalStepsNumber, 444)
    
    node4 = Node([], "Node 4", True, True, True, 2000, 200, 50, 200)
    assert_equals(node4.steps           , [1, 2000, 200, 200])
    assert_equals(node4.stepsNumber     , 2401)
    assert_equals(node4.totalStepsNumber, 2401)

    null = Node([], "Node 4", False, False, False, 2000, 200, 50, 200)
    assert_equals(null.steps            , [1, 0, 0, 0])
    assert_equals(null.stepsNumber      , 1)
    assert_equals(null.totalStepsNumber , 1)


def test_node_forecast():
    node0 = Node([], "Node 0")
    node1 = Node([node0], "Node 1")
    node2 = Node([], "Node 2")
    node3 = Node([node1, node2], "Node 3")
    assert_equals(node0.forecast()      , 111)
    assert_equals(node1.forecast()      , 222)
    assert_equals(node2.forecast()      , 111)
    assert_equals(node3.forecast()      , 444)
    
    node4 = Node([], "Node 4", True, True, True, 2000, 200, 50, 200)
    assert_equals(node4.forecast()      , 2401)
    
    field1 = Field("Value")
    node5 = Node([field1], "Node 5")
    node6 = Node([node4, node5, node3], "Node 6")
    assert_equals(node6.forecast()      , 3178) # 2401 (node4) + 444 (node3) + 111 (node5) + 111 (node6) + 111 (field1)


def test_node_getSubElementAfterSteps():
    node0 = Node([], "Node 0")
    node1 = Node([node0], "Node 1")
    node2 = Node([], "Node 2")
    node3 = Node([node1, node2], "Node 3")

    (subElementIndex, remainingSteps) = node3.getSubElementAfterSteps(111)
    assert_equals(subElementIndex       , 0)
    assert_equals(remainingSteps        , 0)
    
    (subElementIndex, remainingSteps) = node3.getSubElementAfterSteps(330)
    assert_equals(subElementIndex       , 0)
    assert_equals(remainingSteps        , 330 - 111)
    
    (subElementIndex, remainingSteps) = node3.getSubElementAfterSteps(443)
    assert_equals(subElementIndex       , 1)
    assert_equals(remainingSteps        , 110)
    

def test_node_getFuzzTypeAfterSteps(): 
    node4 = Node([], "Node 4", True, True, True, 2000, 200, 50, 200)
   
    (fuzzType, remainingSteps) = node4.getFuzzTypeAfterSteps(0)
    assert_equals(fuzzType              , 0)
    assert_equals(remainingSteps        , 0)
     
    (fuzzType, remainingSteps) = node4.getFuzzTypeAfterSteps(2000)
    assert_equals(fuzzType              , 1)
    assert_equals(remainingSteps        , 1999)
    
    (fuzzType, remainingSteps) = node4.getFuzzTypeAfterSteps(2100)
    assert_equals(fuzzType              , 2)
    assert_equals(remainingSteps        , 99)
    
    (fuzzType, remainingSteps) = node4.getFuzzTypeAfterSteps(2400)
    assert_equals(fuzzType              , 3)
    assert_equals(remainingSteps        , 199)


def test_node_compose():
    field0 = Field("value 0") 
    field1 = Field("value 1") 
    field2 = Field("value 2") 
    node = Node([field0, field1, field2])
    
    assert_equals(node.compose()        , ["value 0", "value 1", "value 2"]) 


def test_node_nope():
    node0 = Node([], "Node 0")
    node1 = Node([], "Node 1")
    node2 = Node([], "Node 2")
    node3 = Node([node0, node1, node2]  , "Node 3")
    node3.makeSteps()
    node3.nope(0)

    assert_equals(node3.subElements     , [node0, node1, node2])
    

def test_node_basic():
    field0 = Field("A") 
    field1 = Field("B") 
    field2 = Field("C") 
    node = Node([field0, field1, field2])
  
    # Tested through a subset. 

    # Adding
    node.fuzz(1) 
    assert_equals(''.join(node.compose()), "BABC")
    node.clean()

    # Mutation
    node.fuzz(11) 
    assert_equals(''.join(node.compose()), "CBC")
    node.clean()

    # Repeat
    node.fuzz(21) 
    assert_equals(''.join(node.compose()), "ABCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
    node.clean()

    # Removing
    node.fuzz(31) 
    assert_equals(''.join(node.compose()), "AB")
    node.clean()

    # Moving
    node.fuzz(45) 
    assert_equals(''.join(node.compose()), "BAC")
    node.clean()


def test_node_overflow():
    field0 = Field("A") 
    field1 = Field("B") 
    field2 = Field("C") 
    node = Node([field0, field1, field2], fuzzing=False)
  
    # Tested through a subset. 
    node.overflow(0) 
    assert_equals(''.join(node.compose()), "ABCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
    node.clean()
    node.overflow(1) 
    assert_equals(''.join(node.compose()), "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABC")
    node.clean()
    node.overflow(2) 
    assert_equals(''.join(node.compose()), "ABCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
    node.clean()
    node.overflow(5) 
    assert_equals(''.join(node.compose()), "ABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBC")
    node.clean()


def test_node_clean():
    field0 = Field("A") 
    field1 = Field("B") 
    field2 = Field("C") 
    node = Node([field0, field1, field2], fuzzing=False)
  
    # Tested through a subset. 
    node.fuzz(1) 
    assert_equals(''.join(node.compose()), "ABCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
    node.clean()
    assert_equals(''.join(node.compose()), "ABC")


def test_node_fuzz():
    field0 = Field("value 0 ") 
    field1 = Field("value 1 ") 
    field2 = Field("value 2 ") 
    node = Node([field0, field1, field2])
     
    node.nope(0)
    expected = node.compose()
    node.clean()
    node.fuzz(0)
    assert_equals(node.compose()        , expected)
    node.clean()

    node.basic(50)
    expected = node.compose()
    node.clean()
    node.fuzz(51)
    assert_equals(node.compose()        , expected)
    node.clean()

    node.overflow(9)
    expected = node.compose()
    node.clean()
    node.fuzz(110)
    assert_equals(node.compose()        , expected)
    node.clean()


def test_node_splitOnStaticFields():
    sfield = StaticField("#")
    field0 = Field("value0") 
    field1 = Field("value1") 
    field2 = Field("value2")
    subNode = Node([field1]) 
    node = Node([field0, sfield, subNode, sfield, field2])
    elementsBlocks = node.splitOnStaticFields("value0#value1#value2")
    assert_equals(len(elementsBlocks)               , 5)

    assert_equals(elementsBlocks[0].value           , "value0")
    assert_equals(len(elementsBlocks[0].elements)   , 1)
    assert_equals(elementsBlocks[0].elements[0]     , field0)

    assert_equals(elementsBlocks[1].value           , "#")
    assert_equals(len(elementsBlocks[1].elements)   , 1)
    assert_equals(elementsBlocks[1].elements[0]     , sfield)

    assert_equals(elementsBlocks[2].value           , "value1")
    assert_equals(len(elementsBlocks[2].elements)   , 1)
    assert_equals(elementsBlocks[2].elements[0]     , subNode)

    assert_equals(elementsBlocks[3].value           , "#")
    assert_equals(len(elementsBlocks[3].elements)   , 1)
    assert_equals(elementsBlocks[3].elements[0]     , sfield)

    assert_equals(elementsBlocks[4].value           , "value2")
    assert_equals(len(elementsBlocks[4].elements)   , 1)
    assert_equals(elementsBlocks[4].elements[0]     , field2)


    # Comes from a bug
    fixedField0 = Field("value", name="fixed", minSize=5, maxSize=5)
    dynamicField0 = Field("", minSize=0, maxSize=100, name="dynamic")
    paddingField0 = PaddingField('#', 10, [fixedField0, dynamicField0], name="padding")
    sizeField0 = SizeField([fixedField0, dynamicField0], 2, name="size")
    staticField0 = StaticField(" ", name="static")
    node2 = Node([fixedField0, staticField0, dynamicField0, staticField0, paddingField0, staticField0, sizeField0])
    elementsBlocks = node2.splitOnStaticFields("vavav ABCDEFGHIJKLMNOP1234 ##### \x00\x19")
    assert_equals(elementsBlocks[0].value           , "vavav")
    assert_equals(elementsBlocks[1].value           , " ")
    assert_equals(elementsBlocks[2].value           , "ABCDEFGHIJKLMNOP1234")
    assert_equals(elementsBlocks[3].value           , " ")
    assert_equals(elementsBlocks[4].value           , "#####")
    assert_equals(elementsBlocks[5].value           , " ")
    assert_equals(elementsBlocks[6].value           , "\x00\x19")

    node3 = Node([dynamicField0, staticField0, node, staticField0, node2])
    elementsBlocks = node3.splitOnStaticFields("vavavABCDEFGHIJKLMNOP1234#####\x00\x19 totor123456789#####\x00\x0e BBBBB AaaaaaaaaaaaaaaaaaaA ##### \x00\x19")
    assert_equals(elementsBlocks[0].value           , "vavavABCDEFGHIJKLMNOP1234#####\x00\x19")
    assert_equals(elementsBlocks[1].value           , " ")
    assert_equals(elementsBlocks[2].value           , "totor123456789#####\x00\x0e")
    assert_equals(elementsBlocks[2].elements[0]     , node)
    assert_equals(elementsBlocks[3].value           , " ")
    assert_equals(elementsBlocks[4].value           , "BBBBB AaaaaaaaaaaaaaaaaaaA ##### \x00\x19")
    assert_equals(elementsBlocks[4].elements[0]     , node2)


def test_node_parse():
    # Simple scenario with no StaticField and subnodes.
    fixedField0 = Field("value", name="fixed", minSize=5, maxSize=5)
    dynamicField0 = Field("", minSize=0, maxSize=100, name="dynamic")
    paddingField0 = PaddingField('#', 10, [fixedField0, dynamicField0], name="padding")
    sizeField0 = SizeField([fixedField0, dynamicField0], 2, name="size")
    node0 = Node([fixedField0, dynamicField0, paddingField0, sizeField0])
    assert_equals(node0.parse("vavavABCDEFGHIJKLMNOP1234#####\x00\x19"), "")
    assert_equals(fixedField0.value, "vavav")
    assert_equals(dynamicField0.value, "ABCDEFGHIJKLMNOP1234")
    assert_equals(paddingField0.value, "#####")
    assert_equals(sizeField0.value, "\x00\x19")
    node0.clean()
    node0.parseClean()

    # Double scenario
    fixedField1 = Field("value", name="fixed1", minSize=5, maxSize=5)
    dynamicField1 = Field("", minSize=0, maxSize=100, name="dynamic1")
    paddingField1 = PaddingField('#', 10, [fixedField1, dynamicField1], name="padding1")
    sizeField1 = SizeField([fixedField1, dynamicField1], 2, name="size1")
    fixedField2 = Field("value", name="fixed2", minSize=5, maxSize=5)
    dynamicField2 = Field("", minSize=0, maxSize=100, name="dynamic2")
    paddingField2 = PaddingField("#", 10, [fixedField2, dynamicField2], name="padding2")
    sizeField2 = SizeField([fixedField2, dynamicField2], 2, name="size2")
    node1 = Node([fixedField1, dynamicField1, paddingField1, sizeField1, fixedField2, dynamicField2, paddingField2, sizeField2])
    assert_equals(node1.parse("vavavABCDEFGHIJKLMNOP1234#####\x00\x19lulul12345#####\x00\x0a"), "")
    assert_equals(fixedField1.value, "vavav")
    assert_equals(dynamicField1.value, "ABCDEFGHIJKLMNOP1234")
    assert_equals(paddingField1.value, "#####")
    assert_equals(sizeField1.value, "\x00\x19")
    assert_equals(fixedField2.value, "lulul")
    assert_equals(dynamicField2.value, "12345")
    assert_equals(paddingField2.value, "#####")
    assert_equals(sizeField2.value, "\x00\x0a")
    node1.clean()
    node1.parseClean()

    # Simple scenario with StaticFields.
    staticField0 = StaticField(" ", name="static")
    node2 = Node([fixedField0, staticField0, dynamicField0, staticField0, paddingField0, staticField0, sizeField0])
    assert_equals(node2.parse("vavav ABCDEFGHIJKLMNOP1234 ##### \x00\x19"), "")
    assert_equals(fixedField0.value, "vavav")
    assert_equals(dynamicField0.value, "ABCDEFGHIJKLMNOP1234")
    assert_equals(paddingField0.value, "#####")
    assert_equals(sizeField0.value, "\x00\x19")
    node2.clean()
    node2.parseClean()

    # Double scenario with StaticField
    node3 = Node([fixedField1, dynamicField1, paddingField1, sizeField1, staticField0, sizeField2, paddingField2, dynamicField2, fixedField2])
    assert_equals(node3.parse("vavavABCDEFGHIJKLMNOP1234#####\x00\x19 \x00\x0a#####12345lulul"), "")
    assert_equals(fixedField1.value, "vavav")
    assert_equals(dynamicField1.value, "ABCDEFGHIJKLMNOP1234")
    assert_equals(paddingField1.value, "#####")
    assert_equals(sizeField1.value, "\x00\x19")
    assert_equals(fixedField2.value, "lulul")
    assert_equals(dynamicField2.value, "12345")
    assert_equals(paddingField2.value, "#####")
    assert_equals(sizeField2.value, "\x00\x0a")
    node3.clean()
    node3.parseClean()

    # Meta scenario with subnodes
    node = Node([fixedField1, dynamicField1, paddingField1, sizeField1, staticField0, node2])
    assert_equals(node.parse("vavavABCDEFGHIJKLMNOP1234#####\x00\x19 BBBBB AaaaaaaaaaaaaaaaaaaA ##### \x00\x19"), "")
    assert_equals(fixedField1.value, "vavav")
    assert_equals(dynamicField1.value, "ABCDEFGHIJKLMNOP1234")
    assert_equals(paddingField1.value, "#####")
    assert_equals(sizeField1.value, "\x00\x19")
    assert_equals(fixedField0.value, "BBBBB")
    assert_equals(dynamicField0.value, "AaaaaaaaaaaaaaaaaaaA")
    assert_equals(paddingField0.value, "#####")
    assert_equals(sizeField0.value, "\x00\x19")


def test_node_parseclean():
    field = Field("value")
    paddingField = PaddingField('#', 10, [field])
    sizeField = SizeField([field, paddingField], 2)
    node = Node([field, paddingField, sizeField])

    node.parse("value#####\x00\x0A")
    node.parseClean()
    assert_equals(node.parsed, False)
    assert_equals(sizeField.parsed, False)
    assert_equals(paddingField.parsed, False)
    assert_equals(field.parsed, False)


# RepeatNode ########################################################################
def test_repeat_node__init__():
    son = Field("a")
    empty = RepeatNode(son, 1)
    assert_equals(empty.defaultSubElements, [son])
    assert_equals(empty.subElements     , [son])
    assert_equals(empty.size            , 1)
    assert_equals(empty.defaultSize     , 1)
    assert_equals(empty.maxSize         , 1)
    assert_equals(empty.minSize         , 0)
    assert_equals(empty.fuzzing         , True)
    assert_equals(empty.overflowing     , True)
    assert_equals(empty.randoming       , False)
    assert_equals(empty.fuzzingNumber   , 100)
    assert_equals(empty.overflowNumber  , 10)
    assert_equals(empty.randomRate      , 20)
    assert_equals(empty.randomNumber    , 100)

    full = RepeatNode(empty, 5, 2, 10, "My Element", False, False, True, 2000, 200, 50, 200)
    assert_equals(full.name             , "My Element")
    assert_equals(len(full.defaultSubElements), 5)
    assert_equals(len(full.subElements) , 5)
    assert_equals(full.defaultSubElements[0].name, empty.name)
    assert_equals(full.subElements[0].name, empty.name)
    assert_equals(full.size             , 5)
    assert_equals(full.defaultSize      , 5)
    assert_equals(full.maxSize          , 10)
    assert_equals(full.minSize          , 2)
    assert_equals(full.fuzzing          , False)
    assert_equals(full.overflowing      , False)
    assert_equals(full.randoming        , True)
    assert_equals(full.fuzzingNumber    , 2000)
    assert_equals(full.overflowNumber   , 200)
    assert_equals(full.randomRate       , 50)
    assert_equals(full.randomNumber     , 200)

    # Modify the object
    full.subElements = []
    assert_equals(len(full.defaultSubElements), 5)
    assert_equals(len(full.subElements)  , 0)
   
     
def test_repeat_node__str__():
    field = Field("a", name="Field 1")
    repeatNode0 = RepeatNode(field, 3, 3, 10, name="RepeatNode 0")
    node0 = Node([field], "Node 0")
    node1 = Node([repeatNode0, node0], "Node 1")
    repeatNode1 = RepeatNode(node1, 2, 0, 4, name="RepeatNode 1")
 
    assert_equals(str(repeatNode0)      , "[RepeatNode 0 [3:3:10]]\n\t[Field 1]: (0:1) [a]\n\t[Field 1]: (0:1) [a]\n\t[Field 1]: (0:1) [a]\n")
    assert_equals(str(repeatNode1)      , "[RepeatNode 1 [0:2:4]]\n\t[Node 1]\n\t\t[RepeatNode 0 [3:3:10]]\n\t\t\t[Field 1]: (0:1) [a]\n\t\t\t[Field 1]: (0:1) [a]\n\t\t\t[Field 1]: (0:1) [a]\n\t\t[Node 0]\n\t\t\t[Field 1]: (0:1) [a]\n\t[Node 1]\n\t\t[RepeatNode 0 [3:3:10]]\n\t\t\t[Field 1]: (0:1) [a]\n\t\t\t[Field 1]: (0:1) [a]\n\t\t\t[Field 1]: (0:1) [a]\n\t\t[Node 0]\n\t\t\t[Field 1]: (0:1) [a]\n")


def test_repeat_node_basic():
    field0 = Field("A") 
    field1 = Field("B") 
    field2 = Field("C") 
    node = Node([field0, field1, field2])
    repeatNode = RepeatNode(node, 3, 0, 5) 
 
    # Tested through a subset. 

    # Adding
    repeatNode.fuzz(1) 
    assert_equals(flatten(repeatNode.compose()), "ABCABCABCABCABC")
    repeatNode.clean()

    # Removing
    repeatNode.fuzz(2) 
    assert_equals(flatten(repeatNode.compose()), "")
    repeatNode.clean()

    repeatNode.fuzz(4) 
    assert_equals(flatten(repeatNode.compose()), "ABC")
    repeatNode.clean()

def test_repeat_node_overflow():
    field0 = Field("A") 
    field1 = Field("B") 
    field2 = Field("C") 
    node = Node([field0, field1, field2])
    repeatNode = RepeatNode(node, 3, 0, 5) 
  
    # Tested through a subset. 
    repeatNode.overflow(0) 
    assert_equals(flatten(repeatNode.compose()), "ABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABC")
    repeatNode.clean()
    repeatNode.overflow(1) 
    assert_equals(flatten(repeatNode.compose()), "ABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABCABC")
    repeatNode.clean()


def test_repeat_node_clean():
    field0 = Field("A") 
    field1 = Field("B") 
    field2 = Field("C") 
    node = Node([field0, field1, field2])
    repeatNode = RepeatNode(node, 3, 0, 5) 
  
    # Tested through a subset. 
    repeatNode.fuzz(1) 
    assert_equals(flatten(repeatNode.compose()), "ABCABCABCABCABC")
    repeatNode.clean()
    assert_equals(flatten(repeatNode.compose()), "ABCABCABC")


def test_repeat_node_parse():
    #TODO
    # Trivial example
    dynamicField = Field("", maxSize=3, name="dynamic")
    repeatNode = RepeatNode(dynamicField, 3, 2, 5)
    assert_equals(repeatNode.parse("AAABBBCCC"), "")
    assert_equals(repeatNode.size, 3)
    assert_equals(repeatNode.subElements[0].value, "AAA")
    assert_equals(repeatNode.subElements[1].value, "BBB")
    assert_equals(repeatNode.subElements[2].value, "CCC")
    assert_equals(repeatNode.parse("AAABBBCCCDDDEEEFFFGGG"), "FFFGGG")
    assert_equals(repeatNode.size, 5)
    assert_equals(repeatNode.subElements[0].value, "AAA")
    assert_equals(repeatNode.subElements[1].value, "BBB")
    assert_equals(repeatNode.subElements[2].value, "CCC")
    assert_equals(repeatNode.subElements[3].value, "DDD")
    assert_equals(repeatNode.subElements[4].value, "EEE")


#    # Simple scenario with no StaticField and subnodes.
#    fixedField0 = Field("value", name="fixed", minSize=5, maxSize=5)
#    dynamicField0 = Field("", minSize=0, maxSize=100, name="dynamic")
#    paddingField0 = PaddingField('#', 10, [fixedField0, dynamicField0], name="padding")
#    sizeField0 = SizeField([fixedField0, dynamicField0], 2, name="size")
#    node0 = Node([fixedField0, dynamicField0, paddingField0, sizeField0])
#    repeatNode = RepeatNode()
#    assert_equals(node0.parse("vavavABCDEFGHIJKLMNOP1234#####\x00\x19"), "")
#    assert_equals(fixedField0.value, "vavav")
#    assert_equals(dynamicField0.value, "ABCDEFGHIJKLMNOP1234")
#    assert_equals(paddingField0.value, "#####")
#    assert_equals(sizeField0.value, "\x00\x19")
#    node0.clean()
#    node0.parseClean()
#
#    # Double scenario
#    fixedField1 = Field("value", name="fixed1", minSize=5, maxSize=5)
#    dynamicField1 = Field("", minSize=0, maxSize=100, name="dynamic1")
#    paddingField1 = PaddingField('#', 10, [fixedField1, dynamicField1], name="padding1")
#    sizeField1 = SizeField([fixedField1, dynamicField1], 2, name="size1")
#    fixedField2 = Field("value", name="fixed2", minSize=5, maxSize=5)
#    dynamicField2 = Field("", minSize=0, maxSize=100, name="dynamic2")
#    paddingField2 = PaddingField("#", 10, [fixedField2, dynamicField2], name="padding2")
#    sizeField2 = SizeField([fixedField2, dynamicField2], 2, name="size2")
#    node1 = Node([fixedField1, dynamicField1, paddingField1, sizeField1, fixedField2, dynamicField2, paddingField2, sizeField2])
#    assert_equals(node1.parse("vavavABCDEFGHIJKLMNOP1234#####\x00\x19lulul12345#####\x00\x0a"), "")
#    assert_equals(fixedField1.value, "vavav")
#    assert_equals(dynamicField1.value, "ABCDEFGHIJKLMNOP1234")
#    assert_equals(paddingField1.value, "#####")
#    assert_equals(sizeField1.value, "\x00\x19")
#    assert_equals(fixedField2.value, "lulul")
#    assert_equals(dynamicField2.value, "12345")
#    assert_equals(paddingField2.value, "#####")
#    assert_equals(sizeField2.value, "\x00\x0a")
#    node1.clean()
#    node1.parseClean()
#
#    # Simple scenario with StaticFields.
#    staticField0 = StaticField(" ", name="static")
#    node2 = Node([fixedField0, staticField0, dynamicField0, staticField0, paddingField0, staticField0, sizeField0])
#    assert_equals(node2.parse("vavav ABCDEFGHIJKLMNOP1234 ##### \x00\x19"), "")
#    assert_equals(fixedField0.value, "vavav")
#    assert_equals(dynamicField0.value, "ABCDEFGHIJKLMNOP1234")
#    assert_equals(paddingField0.value, "#####")
#    assert_equals(sizeField0.value, "\x00\x19")
#    node2.clean()
#    node2.parseClean()
#
#    # Double scenario with StaticField
#    node3 = Node([fixedField1, dynamicField1, paddingField1, sizeField1, staticField0, sizeField2, paddingField2, dynamicField2, fixedField2])
#    assert_equals(node3.parse("vavavABCDEFGHIJKLMNOP1234#####\x00\x19 \x00\x0a#####12345lulul"), "")
#    assert_equals(fixedField1.value, "vavav")
#    assert_equals(dynamicField1.value, "ABCDEFGHIJKLMNOP1234")
#    assert_equals(paddingField1.value, "#####")
#    assert_equals(sizeField1.value, "\x00\x19")
#    assert_equals(fixedField2.value, "lulul")
#    assert_equals(dynamicField2.value, "12345")
#    assert_equals(paddingField2.value, "#####")
#    assert_equals(sizeField2.value, "\x00\x0a")
#    node3.clean()
#    node3.parseClean()
#
#    # Meta scenario with subnodes
#    node = Node([fixedField1, dynamicField1, paddingField1, sizeField1, staticField0, node2])
#    assert_equals(node.parse("vavavABCDEFGHIJKLMNOP1234#####\x00\x19 BBBBB AaaaaaaaaaaaaaaaaaaA ##### \x00\x19"), "")
#    assert_equals(fixedField1.value, "vavav")
#    assert_equals(dynamicField1.value, "ABCDEFGHIJKLMNOP1234")
#    assert_equals(paddingField1.value, "#####")
#    assert_equals(sizeField1.value, "\x00\x19")
#    assert_equals(fixedField0.value, "BBBBB")
#    assert_equals(dynamicField0.value, "AaaaaaaaaaaaaaaaaaaA")
#    assert_equals(paddingField0.value, "#####")
#    assert_equals(sizeField0.value, "\x00\x19")


#def test_node_parseclean():
#    field = Field("value")
#    paddingField = PaddingField('#', 10, [field])
#    sizeField = SizeField([field, paddingField], 2)
#    node = Node([field, paddingField, sizeField])
#
#    node.parse("value#####\x00\x0A")
#    node.parseClean()
#    assert_equals(node.parsed, False)
#    assert_equals(sizeField.parsed, False)
#    assert_equals(paddingField.parsed, False)
#    assert_equals(field.parsed, False)
    

# ElementsBlock ###############################################################
def test_elements_block__init__():
    field0 = Field("0")
    field1 = Field("1")
    elementsBlock = ElementsBlock("value", [field0, field1])
    assert_equals(elementsBlock.value, "value")
    assert_equals(len(elementsBlock.elements), 2)
    assert_equals(elementsBlock.elements, [field0, field1])



# Field #######################################################################
def test_field__init__():
    empty = Field("Value")
    assert_equals(empty.default         , "Value")
    assert_equals(empty.values          , ["Value"])
    assert_equals(empty.value           , "Value")
    assert_equals(empty.minSize         , 0)
    assert_equals(empty.maxSize         , 5)
    assert_equals(empty.fuzzing         , True)
    assert_equals(empty.overflowing     , True)
    assert_equals(empty.randoming       , False)
    assert_equals(empty.fuzzingNumber   , 100)
    assert_equals(empty.overflowNumber  , 10)
    assert_equals(empty.randomRate      , 20)
    assert_equals(empty.randomNumber    , 100)

    full = Field("Value", 2, 52, ["valeur", "test"], "My Element", False, False, True, 2000, 200, 50, 200)
    assert_equals(full.name             , "My Element")
    assert_equals(full.values           , ["Value", "valeur", "test"])
    assert_equals(full.default          , "Value")
    assert_equals(full.value            , "Value")
    assert_equals(full.minSize          , 2)
    assert_equals(full.maxSize          , 52)
    assert_equals(full.fuzzing          , False)
    assert_equals(full.overflowing      , False)
    assert_equals(full.randoming        , True)
    assert_equals(full.fuzzingNumber    , 2000)
    assert_equals(full.overflowNumber   , 200)
    assert_equals(full.randomRate       , 50)
    assert_equals(full.randomNumber     , 200)

    # Modify the object
    full.value = "New value"
    assert_equals(full.default          , "Value")
    assert_equals(full.value            , "New value")

   
def test_field_getLength():
    full = Field("Value", 2, 52, ["valeur", "test"], "My Element", False, False, True, 2000, 200, 50, 200)
    assert_equals(full.getLength()      , 5)

  
def test_field__str__():
    full = Field("Value", 2, 52, ["valeur", "test"], "My Element")
    assert_equals(str(full)             , "[My Element]: (2:52) [Value, valeur, test]\n")


def test_field_update():
    empty = Field("test")
    assert_equals(empty.value           , "test")
    
    empty.update("Value")
    assert_equals(empty.value           , "Value")


def test_field_makeSteps():
    field = Field("Value")
    assert_equals(field.values           , ["Value"])
    
    assert_equals(field.steps           , [1, 100, 10, 0])
    assert_equals(field.stepsNumber     , 111)
    
    assert_equals(field.totalStepsNumber, 111)
    
    field2 = Field("Value", 2, 52, ["valeur", "test"], "My Element", True, True, True, 2000, 200, 50, 200)
   
    assert_equals(field2.steps          , [3, 2000, 200, 200])
    assert_equals(field2.stepsNumber    , 2403)
    assert_equals(field2.totalStepsNumber, 2403)

    null = Field("Value", 2, 52, ["valeur", "test"], "My Element", False, False, False, 2000, 200, 50, 200)
   
    assert_equals(null.steps            , [3, 0, 0, 0])
    assert_equals(null.stepsNumber      , 3)
    assert_equals(null.totalStepsNumber  , 3)


def test_field_forecast():
    field = Field("Value")
    assert_equals(field.values          , ["Value"])
    assert_equals(field.forecast()      , 111)
    
    field2 = Field("Value", 2, 52, ["valeur", "test"], "My Element", True, True, True, 2000, 200, 50, 200)
    assert_equals(field2.forecast()     , 2403)


def test_field_getFuzzTypeAfterSteps(): 
    field = Field("Value", 2, 52, ["valeur", "test"], "My Element", True, True, True, 2000, 200, 50, 200)
   
    (fuzzType, remainingSteps) = field.getFuzzTypeAfterSteps(0)
    assert_equals(fuzzType              , 0)
    assert_equals(remainingSteps        , 0)
     
    (fuzzType, remainingSteps) = field.getFuzzTypeAfterSteps(2000)
    assert_equals(fuzzType              , 1)
    assert_equals(remainingSteps        , 1997)
    
    (fuzzType, remainingSteps) = field.getFuzzTypeAfterSteps(2100)
    assert_equals(fuzzType              , 2)
    assert_equals(remainingSteps        , 97)
    
    (fuzzType, remainingSteps) = field.getFuzzTypeAfterSteps(2400)
    assert_equals(fuzzType              , 3)
    assert_equals(remainingSteps        , 197)


def test_field_compose():
    field = Field("Value", 2, 52, ["valeur", "test"], "My Element", True, True, True, 2000, 200, 50, 200)
    
    assert_equals(field.compose()       , "Value") 


def test_field_nope():
    field = Field("Value", 2, 52, ["valeur", "test"], "My Element", True, True, True, 2000, 200, 50, 200)
    field.nope(0)
    assert_equals(field.value           , "Value")
    field.clean()
    field.nope(1)
    assert_equals(field.value           , "valeur")
    field.clean()
    field.nope(2)
    assert_equals(field.value           , "test")
    field.clean()


def test_field_basic():
    field = Field("Value", 2, 52, ["valeur", "test"], "My Element")
  
    # Tested through a subset. 
    
    # Repeat
    field.basic(0) 
    assert_equals(field.value           , "teeeeeeeeeeest")
    field.clean()
    
    # Repeat and modify
    field.basic(8) 
    assert_equals(field.value           , "V5luuuuuuuuuuuuuuuue")
    field.clean()
    
    # Adding
    field.basic(18) 
    assert_equals(field.value           , "Vaulue")
    field.clean()

    # Adding, removing, modifying
    field.basic(28) 
    assert_equals(field.value           , "6Va!e")
    field.clean()

    # Moving
    field.basic(38) 
    assert_equals(field.value           , "vaelur")
    field.clean()

    # Moving, moving, modifying
    field.basic(48) 
    assert_equals(field.value           , "ale\x1brv")
    field.clean()


def test_field_overflow():
    field = Field("Value", 2, 52, ["valeur", "test"])
  
    # Tested through a subset. 
    field.overflow(0) 
    assert_equals(field.value           , "testttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
    field.clean()
    field.overflow(1) 
    assert_equals(field.value           , "Valueeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    field.clean()
    field.overflow(9) 
    assert_equals(field.value           , "valllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllleur")
    field.clean()
    field.overflow(4) 
    assert_equals(field.value           , "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVValue")
    field.clean()


def test_field_clean():
    field = Field("Value", 2, 52, ["valeur", "test"], fuzzing=False)
    
    field.fuzz(3) 
    assert_equals(field.value           , "testttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
    field.clean()
    assert_equals(field.value           , "Value")


def test_field_fuzz():
    field = Field("Value", 2, 52, ["valeur", "test"])
    
    field.nope(0)
    expected = field.value
    field.clean()
    field.fuzz(0)
    assert_equals(field.value           , expected)
    field.clean()

    field.basic(50)
    expected = field.value
    field.clean()
    field.fuzz(53)
    assert_equals(field.value           , expected)
    field.clean()

    field.overflow(9)
    expected = field.value
    field.clean()
    field.fuzz(112)
    assert_equals(field.value           , expected)
    field.clean()


def test_field_parse():
    field = Field("value", minSize=5, maxSize=5)
    assert_equals(field.parse("abcdef"), "f")
    assert_equals(field.value, "abcde")
 
    # Backward
    field.parseClean()   
    assert_equals(field.parse("abcdef", backward=True), "a")
    assert_equals(field.value, "bcdef")

    # With a SizeField
    field = Field("value", minSize=0, maxSize=5)
    sizeField = SizeField([field], 1)
    sizeField.remainingSize = 3
    sizeField.parsed = True
    assert_equals(field.parse("abcdef"), "def")
    assert_equals(field.value, "abc")
    assert_equals(sizeField.remainingSize, 0)


def test_field_parseclean():
    field = Field("0")
    field.parsed = True
    field.parseClean()
    assert_equals(field.parsed, False)



# IntegerField ################################################################
def test_integerfield_init__():
    empty = IntegerField(32, 1)
    assert_equals(empty.default         , "\x20")
    assert_equals(empty.value           , "\x20")
    assert_equals(empty.values          , ["\x20"])
    assert_equals(empty.endianness      , "be")
    assert_equals(empty.signed          , False)
    assert_equals(empty.minValue        , 0)
    assert_equals(empty.maxValue        , 0)
    assert_equals(empty.minSize         , 1)
    assert_equals(empty.maxSize         , 1)
    assert_equals(empty.fuzzing         , True)
    assert_equals(empty.overflowing     , True)
    assert_equals(empty.randoming       , False)
    assert_equals(empty.fuzzingNumber   , 100)
    assert_equals(empty.overflowNumber  , 10)
    assert_equals(empty.randomRate      , 20)
    assert_equals(empty.randomNumber    , 100)
    assert_equals(empty.theoricMinValue , 0)
    assert_equals(empty.theoricMaxValue , 255)
    assert_equals(empty.integerValue    , 32)

    full = IntegerField(-153, 4, "le", True, -300, 300, [-1], "My Element", False, False, True, 2000, 200, 50, 200)
    assert_equals(full.default          , "\x67\xff\xff\xff")
    assert_equals(full.value            , "\x67\xff\xff\xff")
    assert_equals(full.values           , ["\x67\xff\xff\xff", "\xFF\xFF\xFF\xFF"])
    assert_equals(full.endianness       , "le")
    assert_equals(full.signed           , True)
    assert_equals(full.minValue         , -300)
    assert_equals(full.maxValue         , 300)
    assert_equals(full.minSize          , 4)
    assert_equals(full.maxSize          , 4)
    assert_equals(full.fuzzing          , False)
    assert_equals(full.overflowing      , False)
    assert_equals(full.randoming        , True)
    assert_equals(full.fuzzingNumber    , 2000)
    assert_equals(full.overflowNumber   , 200)
    assert_equals(full.randomRate       , 50)
    assert_equals(full.randomNumber     , 200)
    assert_equals(full.theoricMinValue  , -2147483648)
    assert_equals(full.theoricMaxValue  , 2147483647)
    assert_equals(full.integerValue     , -153)


def test_integerfield_integerUpdate():
    empty = IntegerField(23, 4)
    assert_equals(empty.default         , "\x00\x00\x00\x17")
    assert_equals(empty.value           , "\x00\x00\x00\x17")
    assert_equals(empty.integerValue    , 23)

    empty.integerUpdate(1000)
    assert_equals(empty.default         , "\x00\x00\x00\x17")
    assert_equals(empty.value           , "\x00\x00\x03\xe8")
    assert_equals(empty.integerValue    , 1000)


def test_integerfield_clean():
    field = IntegerField(100, 4)
    assert_equals(field.integerValue    , 100)
    field.integerValue = 200

    assert_equals(field.integerValue    , 200)
    field.clean()
    assert_equals(field.integerValue    , 100)


def test_integerfield_basic():
    field = IntegerField(100, 4)
    field.basic(0)
    assert_equals(field.integerValue           , 4294967295)
    field.clean()

    field = IntegerField(-153, 4, "be", True, -300, 300)
    
    field.basic(0)
    assert_equals(field.integerValue           , 2147483647)
    field.clean()
    
    field.basic(11)
    assert_equals(field.integerValue           , 301)
    field.clean()

    field.basic(1)
    assert_equals(field.integerValue           , -2147483648)
    field.clean()

    field.basic(13) 
    assert_equals(field.integerValue           , 0)
    field.clean()

    field.basic(20) 
    assert_equals(field.integerValue           , -2097151)
    field.clean()


def test_integerfield_overflow():
    field = IntegerField(100, 1)
    
    field.overflow(0) 
    assert_equals(field.integerValue           , 511)
    field.clean()

    field.overflow(1) 
    assert_equals(field.integerValue           , 1023)
    field.clean()

    field = IntegerField(100, 1, "be", True, -300, 300)
    
    field.overflow(0) 
    assert_equals(field.integerValue           , 255)
    field.clean()

    field.overflow(1) 
    assert_equals(field.integerValue           , -256)
    field.clean()
    
    field.overflow(2)
    assert_equals(field.integerValue           , 511)
    field.clean()

    field.overflow(3) 
    assert_equals(field.integerValue           , -512)
    field.clean()



# CountField ##################################################################
def test_count_field__init__():
    node1 = Node()
    empty = CountField(node1, 1)
    assert_equals(empty.node.name       , node1.name)
    assert_equals(empty.endianness      , "be")
    assert_equals(empty.minValue        , 0)
    assert_equals(empty.maxValue        , 0)
    assert_equals(empty.default         , "\x00")
    assert_equals(empty.value           , "\x00")
    assert_equals(empty.fuzzing         , True)
    assert_equals(empty.overflowing     , True)
    assert_equals(empty.randoming       , False)
    assert_equals(empty.fuzzingNumber   , 100)
    assert_equals(empty.overflowNumber  , 10)
    assert_equals(empty.randomRate      , 20)
    assert_equals(empty.randomNumber    , 100)


    field1 = Field("")
    field2 = Field("")
    field3 = Field("")
    node2  = Node([field1, field2, field3])
    full = CountField(node2, 3, "le", 0, 200, "My Count Field", False, False, True, 2000, 200, 50, 200)
    assert_equals(full.node.name        , node2.name)
    assert_equals(full.endianness       , "le")
    assert_equals(full.minValue         , 0)
    assert_equals(full.maxValue         , 200)
    assert_equals(node2.boundElements   , [full])
    assert_equals(full.default          , "\x03\x00\x00")
    assert_equals(full.value            , "\x03\x00\x00")
    assert_equals(full.name             , "My Count Field")
    assert_equals(full.fuzzing          , False)
    assert_equals(full.overflowing      , False)
    assert_equals(full.randoming        , True)
    assert_equals(full.fuzzingNumber    , 2000)
    assert_equals(full.overflowNumber   , 200)
    assert_equals(full.randomRate       , 50)
    assert_equals(full.randomNumber     , 200)
    

def test_count_field__str__():
    field1 = Field("")
    field2 = Field("")
    field3 = Field("")
    node2  = Node([field1, field2, field3], name="node1")
    full = CountField(node2, 3, "le", 0, 200, "My Count Field", False, False, True, 2000, 200, 50, 200)
    assert_equals(str(full)             , "[My Count Field]: (3) [node1]")


def test_count_field_computeCount():
    field = Field("A", name="field 1")
    repeatNode = RepeatNode(field, 3, 0, 10)
    countField = CountField(repeatNode, 3)

    assert_equals(countField.computeCount(), 3)
    repeatNode.fuzz(1)
    assert_equals(flatten(repeatNode.compose()), "AAAAAAA")
    assert_equals(countField.computeCount(), 7)


def test_count_field_notify():
    field = Field("A", name="field 1")
    repeatNode = RepeatNode(field, 3, 0, 10)
    countField = CountField(repeatNode, 3)

    assert_equals(countField.value, "\x00\x00\x03") 
    for i in range(4):
        repeatNode.subElements.append(field)    
    countField.notify()   
 
    assert_equals(countField.value, "\x00\x00\x07") 

    field = Field("A", name="field 1")
    repeatNode = RepeatNode(field, 3, 0, 10)
    countField = CountField(repeatNode, 3, "le")

    assert_equals(countField.value, "\x03\x00\x00") 
    for i in range(4):
        repeatNode.subElements.append(field)    
    countField.notify()   
    
    assert_equals(countField.value, "\x07\x00\x00") 


# TODO
#def test_sizefield_parse():
#    field = SizeField([], 2)
#    assert_equals(field.parse("abcdef"), "cdef")
#    assert_equals(field.value, "ab")
# 
#    # Backward
#    field.parseClean()
#    assert_equals(field.parse("abcdef", backward=True), "abcd")
#    assert_equals(field.value, "ef")
#
#
#def test_sizefield_parseclean():
#    field = SizeField([], 2)
#    field.parsed = True
#    field.remainingSize = 321
#    field.parseClean()
#    assert_equals(field.parsed, False)
#    assert_equals(field.remainingSize, 0)
# TODO


# SizeField ###################################################################
def test_sizefield__init__():
    empty = SizeField([], 1)
    assert_equals(empty.fields          , [])
    assert_equals(empty.selfSize        , False)
    assert_equals(empty.default         , "\x00")
    assert_equals(empty.value           , "\x00")
    assert_equals(empty.fuzzing         , True)
    assert_equals(empty.overflowing     , True)
    assert_equals(empty.randoming       , False)
    assert_equals(empty.fuzzingNumber   , 100)
    assert_equals(empty.overflowNumber  , 10)
    assert_equals(empty.randomRate      , 20)
    assert_equals(empty.randomNumber    , 100)


    field1 = Field("")
    field2 = Field("")
    field3 = Field("")
    full = SizeField([field1, field2, field3], 3, True, "le", 0, 200, "My Size Field", False, False, True, 2000, 200, 50, 200)
    assert_equals(full.fields           , [field1, field2, field3])
    assert_equals(full.selfSize         , True)
    assert_equals(field1.boundElements    , [full])
    assert_equals(field2.boundElements    , [full])
    assert_equals(field3.boundElements    , [full])
    assert_equals(full.default          , "\x03\x00\x00")
    assert_equals(full.value            , "\x03\x00\x00")
    assert_equals(full.name             , "My Size Field")
    assert_equals(full.fuzzing          , False)
    assert_equals(full.overflowing      , False)
    assert_equals(full.randoming        , True)
    assert_equals(full.fuzzingNumber    , 2000)
    assert_equals(full.overflowNumber   , 200)
    assert_equals(full.randomRate       , 50)
    assert_equals(full.randomNumber     , 200)
   
     
def test_sizefield__str__():
    field1 = Field("", name="field 1")
    field2 = Field("", name="field 2")
    field3 = Field("", name="field 3")
    full = SizeField([field1, field2, field3], 3, True, "le", 0, 200, "My Size Field", False, False, True, 2000, 200, 50, 200)
    assert_equals(str(full)             , "[My Size Field]: (3:True) [field 1, field 2, field 3]")


def test_sizefield_update():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = SizeField([field1, field2, field3], 3, True, "be", 0, 200, "My Size Field", False, False, True, 2000, 200, 50, 200)

    assert_equals(field.value           , "\x00\x00\x09")

    field.selfSize = False
    field.update(i2sbs(field.computeSize(), field.minSize))
    assert_equals(field.value           , "\x00\x00\x06")
     
    field1.update("A" * 100)
    assert_equals(field.value           , "\x00\x00\x69")


def test_sizefield_makeSteps():
    empty = SizeField([], 1)
    assert_equals(empty.values          , ["\x00"])
    
    assert_equals(empty.steps           , [1, 100, 10, 0])
    assert_equals(empty.stepsNumber     , 111)
    assert_equals(empty.totalStepsNumber, 111)
    
    field1 = Field("", name="field 1")
    field2 = Field("", name="field 2")
    field3 = Field("", name="field 3")
    full = SizeField([field1, field2, field3], 3, True, "le", 0, 200, "My Size Field", True, True, True, 2000, 200, 50, 200)
   
    assert_equals(full.steps            , [1, 2000, 200, 200])
    assert_equals(full.stepsNumber      , 2401)
    assert_equals(full.totalStepsNumber , 2401)
    
    null = SizeField([field1, field2, field3], 3, True, "le", 0, 200, "My Size Field", False, False, False, 2000, 200, 50, 200)
   
    assert_equals(null.steps            , [1, 0, 0, 0])
    assert_equals(null.stepsNumber      , 1)
    assert_equals(null.totalStepsNumber , 1)


def test_sizefield_forecast():
    field1 = Field("", name="field 1")
    field2 = Field("", name="field 2")
    field3 = Field("", name="field 3")

    empty = SizeField([], 1)
    assert_equals(empty.forecast()      , 111)
    
    full = SizeField([field1, field2, field3], 3, True, "le", 0, 200, "My Size Field", True, True, True, 2000, 200, 50, 200)
    assert_equals(full.forecast()       , 2401)


def test_sizefield_getFuzzTypeAfterSteps(): 
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = SizeField([field1, field2, field3], 3, True, "le", 0, 200, "My Size Field", True, True, True, 2000, 200, 50, 200)
   
    (fuzzType, remainingSteps) = field.getFuzzTypeAfterSteps(0)
    assert_equals(fuzzType              , 0)
    assert_equals(remainingSteps        , 0)
     
    (fuzzType, remainingSteps) = field.getFuzzTypeAfterSteps(2000)
    assert_equals(fuzzType              , 1)
    assert_equals(remainingSteps        , 1999)
    
    (fuzzType, remainingSteps) = field.getFuzzTypeAfterSteps(2100)
    assert_equals(fuzzType              , 2)
    assert_equals(remainingSteps        , 99)
    
    (fuzzType, remainingSteps) = field.getFuzzTypeAfterSteps(2400)
    assert_equals(fuzzType              , 3)
    assert_equals(remainingSteps        , 199)


def test_sizefield_computeSize():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = SizeField([field1, field2, field3], 3, False, "le", 0, 200, "My Size Field", True, True, True, 2000, 200, 50, 200)
    assert_equals(field.computeSize()   , 6) 
    
    field.selfSize = True
    assert_equals(field.computeSize()   , 9) 


def test_sizefield_notify():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = SizeField([field1, field2, field3], 3, False, "be")
    
    assert_equals(field.value   , "\x00\x00\x06") 
    field1.value = "A" * 100
    field.notify()
    assert_equals(field.value   , "\x00\x00\x69") 

    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = SizeField([field1, field2, field3], 3, False, "le")
    
    assert_equals(field.value   , "\x06\x00\x00") 
    field1.value = "A" * 100
    field.notify()
    assert_equals(field.value   , "\x69\x00\x00") 


def test_sizefield_compose():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = SizeField([field1, field2, field3], 3, True, "be", 0, 200, "My Size Field", True, True, True, 2000, 200, 50, 200)

    assert_equals(field.compose()       , "\x00\x00\t") 


def test_sizefield_nope():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = SizeField([field1, field2, field3], 3, True)
    
    field.nope(0)
    assert_equals(field.value           , "\x00\x00\t")


def test_sizefield_basic():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = SizeField([field1, field2, field3], 3, True, "le", 0, 200, "My Size Field", True, True, True, 2000, 200, 50, 200)
  
    # Tested through a subset. 
    field.basic(2) 
    assert_equals(field.value           , "\x00\x00\x01")
    field.clean()
    field.basic(10) 
    assert_equals(field.value           , "\x00@\x00")
    field.clean()
    field.basic(20) 
    assert_equals(field.value           , "\x01\x00 ")
    field.clean()
    field.basic(30) 
    assert_equals(field.value           , "\xff\x1f\x00")
    field.clean()
    field.basic(40) 
    assert_equals(field.value           , "\x01\x08\x00")
    field.clean()
    field.basic(50) 
    assert_equals(field.value           , "\xff\x0f\x00")
    field.clean()
    field.basic(60) 
    assert_equals(field.value           , "\x00\x01\x00")
    field.clean()
    field.basic(7) 
    assert_equals(field.value           , "\xc8\x00\x00")
    field.clean()


def test_sizefield_overflow():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = SizeField([field1, field2, field3], 3, True, "le", 0, 200, "My Size Field", True, True, True, 2000, 200, 50, 200)
  
    # Tested through a subset. 
    field.overflow(0) 
    assert_equals(field.value           , "\xff\xff\x01")
    field.clean()
    field.overflow(1) 
    assert_equals(field.value           , "\xff\xff\x03")
    field.clean()
    field.overflow(2) 
    assert_equals(field.value           , "\xff\xff\x07")
    field.clean()
    field.overflow(3) 
    assert_equals(field.value           , "\xff\xff\x0f")
    field.clean()


def test_sizefield_clean():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = SizeField([field1, field2, field3], 3, True, "be", 0, 200, "My Size Field", True, True, True, 2000, 200, 50, 200)
    
    field.overflow(0) 
    assert_equals(field.value           , "\x01\xff\xff")
    field.clean()
    assert_equals(field.value           , "\x00\x00\t")


def test_sizefield_fuzz():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = SizeField([field1, field2, field3], 3, True, "le", 0, 200, "My Size Field", True, True, True)
    
    field.nope(0)
    expected = field.value
    field.clean()
    field.fuzz(0)
    assert_equals(field.value           , expected)
    field.clean()

    field.basic(50)
    expected = field.value
    field.clean()
    field.fuzz(51)
    assert_equals(field.value           , expected)
    field.clean()

    field.overflow(9)
    expected = field.value
    field.clean()
    field.fuzz(110)
    assert_equals(field.value           , expected)
    field.clean()


def test_sizefield_parse():
    field = SizeField([], 2)
    assert_equals(field.parse("abcdef"), "cdef")
    assert_equals(field.value, "ab")
 
    # Backward
    field.parseClean()
    assert_equals(field.parse("abcdef", backward=True), "abcd")
    assert_equals(field.value, "ef")


def test_sizefield_parseclean():
    field = SizeField([], 2)
    field.parsed = True
    field.remainingSize = 321
    field.parseClean()
    assert_equals(field.parsed, False)
    assert_equals(field.remainingSize, 0)



# PaddingField ################################################################
def test_paddingfield__init__():
    empty = PaddingField("\x00", 1, [])
    assert_equals(empty.paddingElement  , "\x00")
    assert_equals(empty.paddingBlockSize, 1)
    assert_equals(empty.fields          , [])
    assert_equals(empty.default         , "\x00")
    assert_equals(empty.value           , "\x00")
    assert_equals(empty.fuzzing         , True)
    assert_equals(empty.overflowing     , True)
    assert_equals(empty.randoming       , False)
    assert_equals(empty.fuzzingNumber   , 100)
    assert_equals(empty.overflowNumber  , 10)
    assert_equals(empty.randomRate      , 20)
    assert_equals(empty.randomNumber    , 100)


    field1 = Field("A")
    field2 = Field("BB")
    field3 = Field("CCC")
    full = PaddingField("#", 4, [field1, field2, field3], "My Padding Field", False, False, True, 2000, 200, 50, 200)
    assert_equals(full.paddingElement   , "#")
    assert_equals(full.paddingBlockSize , 4)
    assert_equals(full.fields           , [field1, field2, field3])
    assert_equals(field1.boundElements    , [full])
    assert_equals(field2.boundElements    , [full])
    assert_equals(field3.boundElements    , [full])
    assert_equals(full.default          , "##")
    assert_equals(full.value            , "##")
    assert_equals(full.name             , "My Padding Field")
    assert_equals(full.fuzzing          , False)
    assert_equals(full.overflowing      , False)
    assert_equals(full.randoming        , True)
    assert_equals(full.fuzzingNumber    , 2000)
    assert_equals(full.overflowNumber   , 200)
    assert_equals(full.randomRate       , 50)
    assert_equals(full.randomNumber     , 200)
   
     
def test_paddingfield__str__():
    field1 = Field("", name="field 1")
    field2 = Field("", name="field 2")
    field3 = Field("", name="field 3")
    full = PaddingField("#", 4, [field1, field2, field3], "My Padding Field", False, False, True, 2000, 200, 50, 200)
    assert_equals(str(full)             , "[My Padding Field]: (#:4) [field 1, field 2, field 3]")


def test_paddingfield_update():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = PaddingField("#", 4, [field1, field2, field3], "My Padding Field", False, False, True, 2000, 200, 50, 200)

    assert_equals(field.value           , "##")

    field1.update("A" * 100)
    assert_equals(field.value           , "###")


def test_paddingfield_makeSteps():
    empty = PaddingField("\x00", 1, [])
    
    assert_equals(empty.steps           , [1, 100, 10, 0])
    assert_equals(empty.stepsNumber     , 111)
    assert_equals(empty.totalStepsNumber, 111)
    
    field1 = Field("", name="field 1")
    field2 = Field("", name="field 2")
    field3 = Field("", name="field 3")
    full = PaddingField("#", 4, [field1, field2, field3], "My Padding Field", True, True, True, 2000, 200, 50, 200)
   
    assert_equals(full.steps            , [1, 2000, 200, 200])
    assert_equals(full.stepsNumber      , 2401)
    assert_equals(full.totalStepsNumber , 2401)

    null = PaddingField("#", 4, [field1, field2, field3], "My Padding Field", False, False, False, 2000, 200, 50, 200)
    assert_equals(null.steps            , [1, 0, 0, 0])
    assert_equals(null.stepsNumber      , 1)
    assert_equals(null.totalStepsNumber , 1)

def test_paddingfield_forecast():
    field1 = Field("", name="field 1")
    field2 = Field("", name="field 2")
    field3 = Field("", name="field 3")

    empty = PaddingField("\x00", 1, [])
    assert_equals(empty.forecast()      , 111)
    
    full = PaddingField("#", 4, [field1, field2, field3], "My Padding Field", True, True, True, 2000, 200, 50, 200)
    assert_equals(full.forecast()       , 2401)


def test_paddingfield_getFuzzTypeAfterSteps(): 
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = PaddingField("#", 4, [field1, field2, field3], "My Padding Field", True, True, True, 2000, 200, 50, 200)
   
    (fuzzType, remainingSteps) = field.getFuzzTypeAfterSteps(0)
    assert_equals(fuzzType              , 0)
    assert_equals(remainingSteps        , 0)
     
    (fuzzType, remainingSteps) = field.getFuzzTypeAfterSteps(2000)
    assert_equals(fuzzType              , 1)
    assert_equals(remainingSteps        , 1999)
    
    (fuzzType, remainingSteps) = field.getFuzzTypeAfterSteps(2100)
    assert_equals(fuzzType              , 2)
    assert_equals(remainingSteps        , 99)
    
    (fuzzType, remainingSteps) = field.getFuzzTypeAfterSteps(2400)
    assert_equals(fuzzType              , 3)
    assert_equals(remainingSteps        , 199)


def test_paddingfield_computeSize():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = PaddingField("#", 4, [field1, field2, field3], "My Padding Field", False, False, True, 2000, 200, 50, 200)
    assert_equals(field.computeSize()   , 2) 


def test_paddingfield_notify():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = PaddingField("#", 4, [field1, field2, field3], "My Padding Field", False, False, True, 2000, 200, 50, 200)
    
    assert_equals(field.computeSize()   , 2) 
    field1.value = "A" * 100
    field.notify()
    assert_equals(field.computeSize()   , 3) 


def test_paddingfield_compose():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = PaddingField("#", 4, [field1, field2, field3], "My Padding Field", False, False, True, 2000, 200, 50, 200)

    assert_equals(field.compose()       , "##") 


def test_paddingfield_nope():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = PaddingField("#", 4, [field1, field2, field3], "My Padding Field", False, False, True, 2000, 200, 50, 200)
    
    field.nope(0)
    assert_equals(field.value           , "##")


def test_paddingfield_basic():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = PaddingField("#", 4, [field1, field2, field3])
  
    # Tested through a subset. 
    
    # Repeat
    field.basic(0) 
    assert_equals(field.value           , "###############")
    field.clean()

    # Adding
    field.basic(20) 
    assert_equals(field.value           , "#\xa2#")
    field.clean()

    # Mutation
    field.basic(34) 
    assert_equals(field.value           , "#]")
    field.clean()
    field.basic(42) 
    assert_equals(field.value           , "#")
    field.clean()


def test_paddingfield_overflow():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = PaddingField("#", 4, [field1, field2, field3])
  
    # Tested through a subset. 
    field.overflow(0) 
    assert_equals(field.value           , "############################################################################################################################################################################################")
    field.clean()
    field.overflow(1) 
    assert_equals(field.value           , "####################################################################################################################################################################################################################################")
    field.clean()
    field.overflow(2) 
    assert_equals(field.value           , "############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################")
    field.clean()
    field.overflow(3) 
    assert_equals(field.value           , "################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################")
    field.clean()


def test_paddingfield_clean():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = PaddingField("#", 4, [field1, field2, field3], "My Padding Field", False, False, True, 2000, 200, 50, 200)
    
    field.overflow(0) 
    assert_equals(field.value           , "############################################################################################################################################################################################")
    field.clean()
    assert_equals(field.value           , "##")


def test_paddingfield_fuzz():
    field1 = Field("A", name="field 1")
    field2 = Field("BB", name="field 2")
    field3 = Field("CCC", name="field 3")
    field = PaddingField("#", 4, [field1, field2, field3], "My Padding Field")
    
    field.nope(0)
    expected = field.value
    field.clean()
    field.fuzz(0)
    assert_equals(field.value           , expected)
    field.clean()

    field.basic(50)
    expected = field.value
    field.clean()
    field.fuzz(51)
    assert_equals(field.value           , expected)
    field.clean()

    field.overflow(9)
    expected = field.value
    field.clean()
    field.fuzz(110)
    assert_equals(field.value           , expected)
    field.clean()

def test_paddingfield_parse():
    field = PaddingField("#", 16, [])
    assert_equals(field.parse("################toto"), "toto")
    assert_equals(field.value, "################")
 
    # Backward
    field.parseClean()
    assert_equals(field.parse("################toto", backward=True), "################toto")
    assert_equals(field.value, "")



# StringField ###################################################################
def test_StringField__init__():
    empty = StringField("Value")
    assert_equals(empty.default         , "Value")
    assert_equals(empty.values          , ["Value"])
    assert_equals(empty.value           , "Value")
    assert_equals(empty.minSize         , 0)
    assert_equals(empty.maxSize         , 5)
    assert_equals(empty.fuzzing         , True)
    assert_equals(empty.overflowing     , True)
    assert_equals(empty.randoming       , False)
    assert_equals(empty.fuzzingNumber   , 100)
    assert_equals(empty.overflowNumber  , 10)
    assert_equals(empty.randomRate      , 20)
    assert_equals(empty.randomNumber    , 100)
    assert_equals(empty.usualChars      , string.printable)
    assert_equals(empty.specialChars    , " \r\t\n!%#$^&*()`-+=:;'\"\\/?<>.,")
    assert_equals(len(empty.attackVectors), 86)

    full = StringField("Value", 2, 52, ["valeur", "test"], "My Element", False, False, True, 2000, 200, 50, 200)
    full.usualChars = "1234567890"
    full.specialChars = "/*-+"
    full.attackVectors = ["1/0"]

    assert_equals(full.name             , "My Element")
    assert_equals(full.values           , ["Value", "valeur", "test"])
    assert_equals(full.default          , "Value")
    assert_equals(full.value            , "Value")
    assert_equals(full.minSize          , 2)
    assert_equals(full.maxSize          , 52)
    assert_equals(full.fuzzing          , False)
    assert_equals(full.overflowing      , False)
    assert_equals(full.randoming        , True)
    assert_equals(full.fuzzingNumber    , 2000)
    assert_equals(full.overflowNumber   , 200)
    assert_equals(full.randomRate       , 50)
    assert_equals(full.randomNumber     , 200)
    assert_equals(full.usualChars       , "1234567890")
    assert_equals(full.specialChars     , "/*-+")
    assert_equals(full.attackVectors    , ["1/0"])
    

def test_StringField_basic():
    field = StringField("Value", 2, 52, ["valeur", "test"], "My Element")

    # Snipe-add
    field.basic(0) 
    assert_equals(field.value           , "t%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%n%nest")
    field.clean()

    # Snipe-mute
    field.basic(20) 
    assert_equals(field.value           , "te{ping,-b,255.255.255.255}st")
    field.clean()

    # Longer field
    longField = StringField("Loooooooooooooooooonger value", 2, 120, [], "My Element")

    # Snipe-add & snipe-mute
    longField.basic(2) 
    assert_equals(longField.value       , "LPo`touch /tmp/ALICIA`ooooooooooooooo|ping -b 255.255.255.255;{ping,-b,255.255.255.255}onger va`(){ :;};{touch,/tmp/ALICIA}`lue")
    longField.clean()

    shortField = StringField("short", 2, 5, [], "My Element")
    
    # Snipe-add a short one
    shortField.basic(1) 
    assert_equals(shortField.value      , "sho<rt")
    shortField.clean()

    # Snipe-mute
    shortField.basic(4) 
    assert_equals(shortField.value      , "|ping")
    shortField.clean()

    # Snipe-add a long one
    shortField.basic(12) 
    assert_equals(shortField.value      , "sh(){ :;};touch /tmp/ALICIArt")
    shortField.clean()


# Field creators ################################################################
def test_TLVFields():
    [t, l, v] = TLVFields("\x01", 1, "My value", ["\x02", "\x03"], ["value", "Biiiiiiiiiiiig valuuuuuuuuuuuue"], "be", 0, 0, "My TLV", False, True, False, 2000, 200, 50, 200)
    assert_equals(t.value               , "\x01")
    assert_equals(t.values              , ["\x01", "\x02", "\x03"])
    assert_equals(t.name                , "tMy TLV")
    assert_equals(t.fuzzing             , False)
    assert_equals(t.overflowing         , True)
    assert_equals(t.randoming           , False)
    assert_equals(t.fuzzingNumber       , 2000)
    assert_equals(t.overflowNumber      , 200)
    assert_equals(t.randomRate          , 50)
    assert_equals(t.randomNumber        , 200)

    assert_equals(l.value               , "\x08")
    assert_equals(l.minSize             , 1)
    assert_equals(l.selfSize            , False)
    assert_equals(l.name                , "lMy TLV")
    assert_equals(l.fuzzing             , False)
    assert_equals(l.overflowing         , True)
    assert_equals(l.randoming           , False)
    assert_equals(l.fuzzingNumber       , 2000)
    assert_equals(l.overflowNumber      , 200)
    assert_equals(l.randomRate          , 50)
    assert_equals(l.randomNumber        , 200)

    assert_equals(v.value               , "My value")
    assert_equals(v.values              , ["My value", "value", "Biiiiiiiiiiiig valuuuuuuuuuuuue"])
    assert_equals(v.name                , "vMy TLV")
    assert_equals(v.fuzzing             , False)
    assert_equals(v.overflowing         , True)
    assert_equals(v.randoming           , False)
    assert_equals(v.fuzzingNumber       , 2000)
    assert_equals(v.overflowNumber      , 200)
    assert_equals(v.randomRate          , 50)
    assert_equals(v.randomNumber        , 200)


def test_StaticField():
    t = StaticField("Value", "My Static Field") 
    assert_equals(t.value               , "Value")
    assert_equals(t.values              , ["Value"])
    assert_equals(t.name                , "My Static Field")
    assert_equals(t.fuzzing             , False)
    assert_equals(t.overflowing         , False)
    assert_equals(t.randoming           , False)

