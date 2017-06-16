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
# Unit-tests of Alicia automata



# Imports #####################################################################
from nose.tools import *

from alicia.automata import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass



# Transition ###################################################################
def test_transition__init__():
    exiting = Transition("a", "b")
    assert_equals(exiting.inputElement,     "a")
    assert_equals(exiting.outputElement,    "b")
    assert_equals(exiting.pointedState,     None)
    assert_equals(exiting.idTransition,     0)
    assert_equals(exiting.name,             "Transition 0")

    state = State()
    transition = Transition("Hello", "Hallo", state, "Transitionen")
    assert_equals(transition.inputElement,  "Hello")
    assert_equals(transition.outputElement, "Hallo")
    assert_equals(transition.pointedState,  state)
    assert_equals(transition.idTransition,  1)
    assert_equals(transition.name,          "Transitionen")
   

def test_transition__str__():
    state = State()
    transition = Transition("Hello", "Hallo", state, "Transitionen")
    assert_equals(str(transition), "Transitionen: -Hello/Hallo-> (State 1)")

 
def test_transition_isExiting():
    exiting = Transition("a", "b")
    assert_equals(exiting.isExiting(),    True)
    
    state = State()
    transition = Transition("Hello", "Hallo", state, "Transitionen")
    assert_equals(transition.isExiting(), False)



# State ########################################################################
def test_state__init__():
    emptyState = State()
    assert_equals(emptyState.transitions,   [])
    assert_equals(emptyState.idState,       3) # Already 3 states constructed above.
    assert_equals(emptyState.name,          "State 3")

    exiting = Transition("a", "out")
    moving = Transition("b", "in", emptyState)
    centralState = State([exiting, moving], "Central State")
    assert_equals(centralState.transitions, [exiting, moving])
    assert_equals(centralState.idState,     4)
    assert_equals(centralState.name,        "Central State")


def test_state__str():
    emptyState = State()
    exiting = Transition("a", "out")
    moving = Transition("b", "in", emptyState)
    centralState = State([exiting, moving], "Central State")
    assert_equals(str(centralState), "(Central State)\n\tTransition 7: -a/out->\n\tTransition 8: -b/in-> (State 5)")
    

def test_state_next():
    emptyState = State()
    exiting = Transition("a", "out")
    moving = Transition("b", "in", emptyState)
    centralState = State([exiting, moving], "Central State")
    assert_equals(centralState.next("a"),   exiting)
    assert_equals(centralState.next("b"),   moving)
    assert_equals(centralState.next("c"),   None)

    

# Automata #####################################################################
def test_automata__init__():
    emptyAutomata = Automata([], [])
    assert_equals(emptyAutomata.idAutomata,     0)
    assert_equals(emptyAutomata.name,           "Automata 0")
    assert_equals(emptyAutomata.states,         [])
    assert_equals(emptyAutomata.enteringTransitions, [])
    assert_equals(emptyAutomata.currentState,   None)

    emptyState = State()
    centralState = State()
    entering = Transition("Hello", "Hallo", centralState)
    automata = Automata([emptyState, centralState], [entering], "My automata")
    assert_equals(automata.idAutomata,   1)
    assert_equals(automata.name,         "My automata")
    assert_equals(automata.states,       [emptyState, centralState])
    assert_equals(automata.enteringTransitions, [entering])
    assert_equals(automata.currentState,   None)


def test_automata__str__():
    emptyState = State()
    centralState = State()
    entering = Transition("Hello", "Hallo", centralState)
    automata = Automata([emptyState, centralState], [entering], "My automata")
    assert_equals(str(automata), '[My automata\nStates: State 11, State 12\nTransitions: Transition 12: -Hello/Hallo-> (State 12)]')


def test_automata_enter():
    emptyState = State()
    centralState = State()
    entering = Transition("Hello", "Hallo", centralState)
    automata = Automata([emptyState, centralState], [entering], "My automata")
        
    assert_equals(automata.enter("Hello"), "Hallo")
    assert_equals(automata.currentState, centralState)

    assert_equals(automata.enter("Test"), "")
    assert_equals(automata.currentState, None)

def test_automata_next():
    emptyState = State()
    exiting = Transition("Bye", "Auf wiedersehen")
    moving = Transition("What?", "Was?")
    moving2 = Transition("Uh!", "Ach!", emptyState)
    centralState = State([exiting, moving, moving2], "Central State")
    entering = Transition("Hello", "Hallo", centralState)
    moving.pointedState = centralState
    automata = Automata([emptyState, centralState], [entering], "My automata")

    automata.enter("Hello")
    assert_equals(automata.next("What?"), "Was?")
    assert_equals(automata.currentState, centralState)
    assert_equals(automata.next("Bye"), "Auf wiedersehen")
    assert_equals(automata.currentState, None)


    automata.enter("Hello")
    assert_equals(automata.next("Uh!"), "Ach!")
    assert_equals(automata.currentState, emptyState)
    assert_equals(automata.enter("Test"), "")
    assert_equals(automata.currentState, None)

