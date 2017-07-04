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

from alicia.content import *
from alicia.configuration import *
from alicia.utils import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass



# Content #####################################################################
def test_Content___init__():
    content0 = Content("ABCDE")
    assert_equals(content0.type             , "Content")
    assert_equals(content0.default          , "ABCDE")
    assert_equals(content0.current          , "ABCDE")
    assert_equals(content0.future           , "ABCDE")


def test_Content_update():
    content0 = Content("ABCDE")
    content0.update("FGHIJ")
    assert_equals(content0.current          , "FGHIJ")
    

def test_Content_commit():
    content0 = Content("ABCDE")
    content0.future = "FGHIJ"
    content0.commit()
    assert_equals(content0.current          , "FGHIJ")


def test_Content_clean():
    content0 = Content("ABCDE")
    content0.update("FGHIJ")
    content0.clean()
    assert_equals(content0.current          , "ABCDE")


def test_Content_newCharacter():
    content0 = Content("ABCDE")
    rand = random.Random(0)
    assert_equals(content0.newCharacter(rand), "\xd8")


def test_Content_fuzz():
    content0 = Content("ABCDE")
    rand = random.Random(0)
    content0.fuzz(5, 5, rand, 0)
    assert_equals(content0.current           , "\xc2kB\x82g")

