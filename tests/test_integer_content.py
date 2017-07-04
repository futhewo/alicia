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

from alicia.integer_content import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass



# IntegerContent ##############################################################
def test_IntegerContent___init__():
    content0 = IntegerContent("\x00\x00\x00\x01")
    assert_equals(content0.type             , "IntegerContent")
    assert_equals(content0.default          , "\x00\x00\x00\x01")
    assert_equals(content0.current          , "\x00\x00\x00\x01")
    assert_equals(content0.future           , "\x00\x00\x00\x01")
    assert_equals(content0.integerCurrent   , 1)
    assert_equals(content0.size             , 4)
    assert_equals(content0.signed           , False)
    assert_equals(content0.littleEndian     , False)
    assert_equals(content0.magicValues      , [4294967295, 0, 4294967296, 1, 4294967294])
    
    content1 = IntegerContent(32, size=2, signed=True, littleEndian=True)
    assert_equals(content1.type             , "IntegerContent")
    assert_equals(content1.default          , "\x20\x00")
    assert_equals(content1.current          , "\x20\x00")
    assert_equals(content1.future           , "\x20\x00")
    assert_equals(content1.integerCurrent   , 32)
    assert_equals(content1.size             , 2)
    assert_equals(content1.signed           , True)
    assert_equals(content1.littleEndian     , True)
    assert_equals(content1.magicValues      , [32767, -32768, 32768, -32767, 32766, -32769, -1, 0, 1])

    content2 = IntegerContent(-32, size=2, signed=True, littleEndian=True)
    assert_equals(content2.current          , "\xe0\xff")

    content3 = IntegerContent("\xfe\xff", size=2, signed=True, littleEndian=True)
    assert_equals(content3.integerCurrent   , -2)


def test_IntegerContent_update():
    content0 = IntegerContent("\x00\x00\x00\x01")
    content0.update("\x12\x00")
    assert_equals(content0.current          , "\x00\x00\x12\x00")
    assert_equals(content0.integerCurrent   , 4608)

    content1 = IntegerContent(32, size=2, signed=True, littleEndian=True)
    content1.update("\xfe\xff")
    assert_equals(content1.current          , "\xfe\xff")
    assert_equals(content1.integerCurrent   , -2)


def test_IntegerContent_integerUpdate():
    content0 = IntegerContent("\x00\x00\x00\x01")
    content0.integerUpdate(2)
    assert_equals(content0.current          , "\x00\x00\x00\x02")
    assert_equals(content0.integerCurrent   , 2)

    content1 = IntegerContent(32, size=2, signed=True, littleEndian=True)
    content1.integerUpdate(-32)
    assert_equals(content1.current          , "\xe0\xff")
    assert_equals(content1.integerCurrent   , -32)


def test_IntegerContent_commit():
    content0 = IntegerContent(32)
    content0.future = "\x00\x00\x40\x00"
    content0.commit()
    assert_equals(content0.current          , "\x00\x00\x40\x00")
    assert_equals(content0.integerCurrent   , 16384)


def test_IntegerContent_clean():
    content0 = IntegerContent(32)
    content0.update("\x00\x00\x40\x00")
    content0.clean()
    assert_equals(content0.current          , "\x00\x00\x00\x20")
    assert_equals(content0.integerCurrent   , 32)


def test_IntegerContent_newCharacter():
    content0 = IntegerContent(32)
    rand = random.Random(0)
    assert_equals(content0.newCharacter(rand), "\xff")

    rand = random.Random(1)
    assert_equals(content0.newCharacter(rand), "\x00")


def test_IntegerContent_fuzz():
    content0 = IntegerContent(32)
    rand = random.Random(1)
    content0.fuzz(4, 4, rand, 1)
    assert_equals(content0.current           , "\x00\x00\x00\x00")

    rand = random.Random(100)
    content0.fuzz(4, 4, rand, 100)
    assert_equals(content0.current           , "\x00\x00\x00 ")

