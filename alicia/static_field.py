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

from alicia.element import *
from alicia.content import *
from alicia.utils import *



# Field ########################################################################
class StaticField(Element):
    """
        A field is a leaf element, as such it has a value.
        A static field cannot be modified.
    """

    # Constructor =========================================
    def __init__(self, content, name=None, weight=1.0):
        Element.__init__(self, name, True, weight)
        
        self.type = "StaticField"
        self.setName(name)
 
        self.content = content


    # Actioners ===========================================
    def getSize(self):
        """
            Return the size of the content.
        """
        return self.content.getSize()


    # Built-ins ===========================================
    def __str__(self):
        """
            Return a string representing the element.
            @return (string)representation
        """
        string = "[{0}: {1} ({2})]\n".format(self.name, self.compose(), self.content.type)
        return string


    # Fuzzing =============================================
    def compose(self):
        """
            Return the value of a field.
        """
        return self.content.current


    def commit(self):
        self.content.commit()


    def clean(self):
        """
            Clean the field after having fuzzed it.
        """
        self.content.clean()
        self.notifiable = True


    # Parsing =============================================
    def parse(self, value, backward=False, root=False):
        pass

