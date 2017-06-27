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
# Utilitary code.



# Code ########################################################################
def twoscomp(integer, size):
    """
        Compute the two's complement of a signed positive integer.
    """
    ti = 0
    if integer != 0:
        ti = ((2 ** (size * 8) - 1) ^ integer) + 1
    return ti


def ui2bs(integer, endianness="be"):
    """
        Unsigned integer to byte string.
    """
    assert(integer >= 0)
    bs = ""
    ui = integer
    if ui == 0:
        bs = "\x00"
    while ui > 0:
        bs = chr(ui & 0xFF) + bs
        ui = ui >> 8
    if endianness == "le":
        lr = list(bs)
        lr.reverse()
        bs = "".join(lr)
    return bs


def bs2ui(bytestring, endianness="be"):
    """
        Byte String to unsigned integer.
    """
    ui = 0
    bs = bytestring
    if endianness == "le":
        lr = list(bs)
        lr.reverse()
        bs = ''.join(lr)
    for b in bs:
        ui = ui << 8
        ui += ord(b)
    return ui


def i2sbs(integer, size, endianness="be"):
    """
        Integer to sized byte string.
        Fill with 0x00 an integer on a byte string representation.
    """
    i = integer
    if i < 0:
        i = twoscomp(-i, size)

    bs = ui2bs(i, endianness)
    if size > len(bs):
        if endianness == "le":
            bs += "\x00" * (size - len(bs))
        else:
            bs = "\x00" * (size - len(bs)) + bs
    elif size < len(bs):
        if endianness == "le":
            bs = bs[-size:]
        else:
            bs = bs[:size]
    return bs


def sbs2i(bytestring, signed=False, endianness="be"):
    """
        Signed byte string to integer.
    """
    bs = bytestring
    i = 0
    if signed:
        negative = False
        if endianness == "le":
            negative = (0x80 & ord(bs[len(bs) - 1])) != 0
        else:
            negative = (0x80 & ord(bs[0])) != 0

        i = bs2ui(bytestring, endianness)
        if negative:
            i = -twoscomp(i, len(bytestring))

    else:
        i = bs2ui(bytestring, endianness)
    return i


def fill(bytestring, size):
    """
        Fill a bytestring with 0x00.
    """
    bs = bytestring
    if size > len(bs):
        bs = "\x00" * (size - len(bs)) + bs
    elif size < len(bs):
        bs = bs[-size:]
    return bs


def hexPrint(stri):
    """
        Display a string in a pretty hexedit like format.
        Very convenient to compare to real case.
    """
    chunks = []
    for i in range(0, len(stri), 16):
        chunks.append(stri[0 + i:16 + i])
    for chunk in chunks:
        preline = ""
        postline = ""
        i = 0
        for char in chunk:
            preline += char.encode("hex") + ' '
            i += 1
            if i == 8:
                preline += ' '
            if char in string.printable and char not in "\x0c\v\n\r\t":
                postline += char
            else:
                postline += '.'
        if len(chunk) < 8:
            print preline + (16 - len(chunk)) * "   " + '  ' + postline
        elif len(chunk) < 16:
            print preline + (16 - len(chunk)) * "   " + ' ' + postline
        else:
            print preline + ' ' + postline

        
def prettyPrint(listt):
    """
        Display a list of string in hexedit formats properly separated.
    """
    if listt is None:
        return
    i = 0
    for stri in listt:
        print "\n========== Case {0} ==========".format(i)
        hexPrint(stri)
        i += 1


def debug(string, verbose):
    """
        If the verbose flag is set, print the information.
    """
    if verbose:
        print string


def log(string):
    """
        Log information.
    """
    print string


def error(string):
    """
        Warns for an error
    """
    print "[ERROR] " + string


def flatten(stringList):
    """
        Flatten a string list in one big string.
        @param stringList: can be a string, a list(string), a list(list(string), string, list(list(string)), a list(list(...(string)...), etc.
    """
    if type(stringList) == list:
        if len(stringList) == 0:
            return "" 
        elif len(stringList) == 1:
            return flatten(stringList[0])
        else:
            rslt = []
            onlyString = True
            # Loop through elements
            for element in stringList:
                if type(element) == list:
                    rslt += element
                    onlyString = False
                else:
                    rslt.append(element)
            if onlyString:
                # Cat everything
                return flatten(reduce(lambda x,y: x + y, rslt))
            else:
                # Wait one more turn
                return flatten(rslt)
    else:
        # End of it
        return stringList


def generateIndexes(size, rand, randomness):
    """
        Generate a list of indexes from a list of the provided size, pointing to elements that will be modified.
        @param (int)size: the size of the list
        @param (random.Random)rand: the random object that will decide
        @param (int)randomess: the randomness rate
    """
    indexes = []
    for index in range(size):
        if rand.randint(0, 99) < randomness:
            indexes.append(index)

    if len(indexes) == 0:
        if size == 0:
            indexes.append(0)
        else:
            indexes.append(rand.randint(0, size - 1))

    return indexes

