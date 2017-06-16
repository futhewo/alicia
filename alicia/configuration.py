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
# Global configuration of a fuzzing session. Used to configure default behaviour.



# Imports #####################################################################
import random



# Constants ###################################################################
# For 'fuzzing' type
NOPE        = 0
FUZZING     = 1
OVERFLOWING = 2
RANDOMING   = 3

# For 'mutation' type
MOVING      = 0
REMOVING    = 1
ADDING      = 2
REPEAT      = 3
MUTATION    = 4
SNIPEADD    = 5
SNIPEMUTE   = 6



# Specifics ###################################################################
elementId = 0



# Configuration ###############################################################
class Configuration:
    """
        Configure the project.
    """

    def __init__(self):
        # Verbosity
        self.verbose        = True
    
        # Flags
        self.fuzzing        = True
        self.overflowing    = True
        self.randoming      = False
        
        # Misc
        self.fuzzingNumber  = 100
        self.overflowNumber = 10
        self.randomNumber   = 100
        self.randomRate     = 20
        self.charRepeat     = 32
        self.subElemRepeat  = 32


        # Generating random fields
        self.defaultMinSize = 128
        self.defaultMaxSize = 128

        # Overflow
        # The overlowing pattern is of size randint(overflowMin, overflowMax) ** agressivity
        self.agressivity    = 1
        self.overflowMin    = 100
        self.overflowMax    = 200


# Construction of the current configuration object.
conf = Configuration()
