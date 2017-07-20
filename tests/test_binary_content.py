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

from alicia.contents.binary_content import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass



# BinaryContent ###############################################################
def test_BinaryContent___init__():
    content0 = BinaryContent("\xff\x00")
    assert_equals(content0.type             , "BinaryContent")
    assert_equals(content0.default          , "\xff\x00")
    assert_equals(content0.current          , "\xff\x00")
    assert_equals(content0.future           , "\xff\x00")
    assert_equals(content0.binaryCurrent.tobytes(), "\xff\x00")
    

def test_BinaryContent_update():
    content0 = BinaryContent("\xff\x00")
    content0.update("\x00\xff")
    assert_equals(content0.current          , "\x00\xff")
    assert_equals(content0.binaryCurrent.tobytes(), "\x00\xff")


def test_BinaryContent_binaryUpdate():
    content0 = BinaryContent("\xff\x00")
    content0.binaryUpdate(bitarray.bitarray("0000000011111111"))
    assert_equals(content0.current          , "\x00\xff")
    assert_equals(content0.binaryCurrent.tobytes(), "\x00\xff")


def test_BinaryContent_commit():
    content0 = BinaryContent("\xff\x00")
    content0.future = "\x00\xff"
    content0.commit()
    assert_equals(content0.current          , "\x00\xff")
    assert_equals(content0.binaryCurrent.tobytes(), "\x00\xff")


def test_BinaryContent_clean():
    content0 = BinaryContent("\x00\xff")
    content0.update("\xff\x00")
    content0.clean()
    assert_equals(content0.current          , "\x00\xff")
    assert_equals(content0.binaryCurrent.tobytes(), "\x00\xff")


def test_BinaryContent_newCharacter():
    content0 = BinaryContent("\x00\xff")
    rand = random.Random(0)
    assert_equals(content0.newCharacter(rand), "\xd8")

    rand = random.Random(1)
    assert_equals(content0.newCharacter(rand), '"')


def test_BinaryContent_fuzz():
    content0 = BinaryContent("\x00\xff")
    rand = random.Random(1)
    content0.fuzz(2, 2, rand, 0)
    assert_equals(content0.current           , "\x80\xff")

    content0.clean()
    rand = random.Random(2)
    content0.fuzz(2, 2, rand, 15)
    assert_equals(content0.current           , "\x00\xfe")


    content0.clean()
    rand = random.Random(1)
    content0.fuzz(2, 2, rand, 16)
    assert_equals(content0.current           , "\x80;")

