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
import random

from alicia.string_content import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass



# StringContent ##############################################################
def test_StringContent___init__():
    content0 = StringContent("Bonjour")
    assert_equals(content0.type             , "StringContent")
    assert_equals(content0.default          , "Bonjour")
    assert_equals(content0.current          , "Bonjour")
    assert_equals(content0.future           , "Bonjour")


def test_StringContent_newCharacter():
    content0 = StringContent("Bonjour")
    rand = random.Random(0)
    assert_equals(content0.newCharacter(rand), "\\")

    rand = random.Random(3)
    assert_equals(content0.newCharacter(rand), "S")


def test_StringContent_fuzz():
    content0 = StringContent("Bonjour")
    rand = random.Random(0)
    content0.fuzz(10, 10, rand, 0)
    assert_equals(content0.current           , "||ping -b ")
    content0.clean()

    rand = random.Random(1)
    content0.fuzz(20, 40, rand, 1)
    assert_equals(content0.current           , "Bonjour&#x3d;")

