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
from alicia.choice import *
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



# Choice ######################################################################
def test_Choice___init__():
    global elementId
    elementId = 0
    element0 = Element()
    node0 = Choice([element0])
    assert_equals(node0.elementId           , 1)
    assert_equals(node0.type                , "Choice")
    assert_equals(node0.name                , "Choice 1")
    assert_equals(node0.static              , False)
    assert_equals(node0.weight              , 1.0)
    assert_equals(node0.defaultSubElements  , [element0])
    assert_equals(node0.currentSubElements  , [element0])
    assert_equals(node0.futureSubElements   , [element0])
    assert_equals(node0.defaultChoice       , 0)
    assert_equals(node0.currentChoice       , 0)
    assert_equals(node0.futureChoice        , 0)


    element1 = Element()
    node1 = Choice([element0, element1], choice=1, name="My Choice", static=True, weight=2.5)
    assert_equals(node1.elementId           , 3)
    assert_equals(node1.type                , "Choice")
    assert_equals(node1.name                , "My Choice")
    assert_equals(node1.static              , True)
    assert_equals(node1.weight              , 2.5)
    assert_equals(node1.defaultSubElements  , [element0, element1])
    assert_equals(node1.currentSubElements  , [element0, element1])
    assert_equals(node1.futureSubElements   , [element0, element1])
    assert_equals(node1.defaultChoice       , 1)
    assert_equals(node1.currentChoice       , 1)
    assert_equals(node1.futureChoice        , 1)


def test_Choice_compose():
    content0 = StringContent("ABCDE")
    element0 = CloseField(content0)
    content1 = IntegerContent(32)
    element1 = CloseField(content1)
    node0 = Choice([element0, element1])
    assert_equals(node0.compose()       , "ABCDE")

    node0.currentChoice = 1
    assert_equals(node0.compose()       , "\x00\x00\x00 ")


def test_Choice_nodeFuzz():
    configuration.fuzzing = 100
    content0 = StringContent("ABCDE")
    element0 = CloseField(content0)
    content1 = IntegerContent(32)
    element1 = CloseField(content1)
    node0 = Choice([element0, element1])

    node0.nodeFuzz(0)
    assert_equals(node0.compose()       , "\x00\x00\x00 ")
    node0.clean()    

    node0.nodeFuzz(1)
    assert_equals(node0.compose()       , "ABCDE")
    node0.clean()    


def test_Choice_fuzz():
    configuration.fuzzingNumber = 10
    content0 = StringContent("ABCDE")
    element0 = CloseField(content0)
    content1 = IntegerContent(32)
    element1 = CloseField(content1)
    node0 = Choice([element0, element1])

    # NodeFuzz : Mutation
    node0.fuzz(0)
    assert_equals(node0.compose()       , "\x00\x00\x00 ")
    node0.clean()    

    # Field fuzz
    node0.fuzz(10)
    assert_equals(node0.compose()       , "ABCWE")
    node0.clean()    

    # Field fuzz
    node0.fuzz(21)
    assert_equals(node0.compose()       , "\x00\x00\x00\x00")
    node0.clean()    


def test_Choice_clean():
    content0 = StringContent("ABCDE")
    element0 = CloseField(content0)
    content1 = IntegerContent(32)
    element1 = CloseField(content1)
    node0 = Choice([element0, element1])

    element0.fuzz(0)
    element1.fuzz(0)
    node0.currentChoice = 1
    node0.clean()
    
    assert_equals(node0.compose()       , "ABCDE")
 

def test_Choice_commit():
    content0 = StringContent("ABCDE")
    element0 = CloseField(content0)
    content1 = IntegerContent(32)
    element1 = CloseField(content1)
    node0 = Choice([element0, element1])

    node0.futureChoice = 1
    content1.future = "\x00\x00\x00\xff"
    node0.commit()

    assert_equals(node0.compose()       , "\x00\x00\x00\xff")

