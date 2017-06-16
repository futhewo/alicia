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



# RandomField #############################################
class RandomField(Field):
    """
        A field with an ever changing random value.
    """
    def __init__(self, minSize=0, maxSize=0, name=None):
        Field.__init__(self, "", minSize, maxSize, [], name, False, False, False)

        if name is None:
            self.name = "RandomField {0}".format(self.elementId)
        self.type = "RandomField"

        value = ""
        for index in range(rand.randint(self.minSize, self.maxSize)):
            value += chr(rand.randint(0, 255))
        self.default = value
        self.value = value


    def clean(self):
        """
            Clean the field after having fuzzed it.
    """
        self.default = ""
        for i in range(rand.randint(self.minSize, self.maxSize)):
            self.default += chr(rand.randint(0, 255))
        self.value = self.default
        self.notifiable = True

