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

from alicia.utils import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass



# Tools #######################################################################
def test_twos_complement():
    assert_equals(twoscomp(0, 4)        , 0)
    assert_equals(twoscomp(1, 4)        , 0xFFFFFFFF)


def test_ui2bs():
    assert_equals(ui2bs(0)              , "\x00")
    assert_equals(ui2bs(14923237)       , "\xE3\xB5\xE5")
    assert_equals(ui2bs(14923237, "le") , "\xE5\xB5\xE3")


def test_bs2ui():
    assert_equals(bs2ui("\x00")         , 0)
    assert_equals(bs2ui("\xE3\xB5\xE5") , 14923237)
    assert_equals(bs2ui("\xE5\xB5\xE3", "le"), 14923237)


def test_i2sbs():
    assert_equals(i2sbs(0, 4)           , "\x00\x00\x00\x00")
    assert_equals(i2sbs(14923237, 4)    , "\x00\xE3\xB5\xE5")
    assert_equals(i2sbs(14923237, 2)    , "\xE3\xB5")
    assert_equals(i2sbs(14923237, 4, "le"), "\xE5\xB5\xE3\x00")
    assert_equals(i2sbs(14923237, 2, "le"), "\xB5\xE3")

    assert_equals(i2sbs(-14923237, 4) , "\xFF\x1C\x4A\x1B")
    assert_equals(i2sbs(-14923237, 4, "le"), "\x1B\x4A\x1C\xFF")
    

def test_sbs2i():
    assert_equals(sbs2i("\x00\x00\x00") , 0)
    assert_equals(sbs2i("\xE3\xB5\xE5") , 14923237)
    assert_equals(sbs2i("\x00\xE3\xB5\xE5", True) , 14923237)
    assert_equals(sbs2i("\xFF\x1C\x4A\x1B", True) , -14923237)
    assert_equals(sbs2i("\x00\x00\x00", littleEndian=True), 0)
    assert_equals(sbs2i("\xE5\xB5\xE3", littleEndian=True), 14923237)
    assert_equals(sbs2i("\xE5\xB5\xE3\x00", True, "le"), 14923237)
    assert_equals(sbs2i("\x1B\x4A\x1C\xFF", True, "le"), -14923237)


def test_flatten():
    assert_equals(flatten("test")       , "test")
    assert_equals(flatten([[[[["test"]]]]]), "test")
    assert_equals(flatten(["a", "b", "c"]), "abc")
    assert_equals(flatten([["a", "b", "c"], "d", ["e", ["f", ["g"], "h"], "i"], "j"]), "abcdefghij")

def test_generateIndexes():
    rand = random.Random(0)
    randomness = 20
    assert_equals(generateIndexes(5, rand, randomness), [2])

