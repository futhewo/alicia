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
OVERFLOW    = 0
FUZZING     = 1


# For 'mutation' type
ADD         = 0
MUTATION    = 1
SWAP        = 2
REMOVE      = 3



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
        self.overflow       = True
        
        # Misc
        self.fuzzingNumber  = 100
        self.overflowNumber = 10
        self.randomness     = 20 # 20%
        self.charRepeat     = 32
        self.subElemRepeat  = 32


        # Generating random fields
        self.defaultMinSize = 128
        self.defaultMaxSize = 128


# Construction of the current configuration object.
configuration = Configuration()
