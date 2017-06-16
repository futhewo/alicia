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
# Automata structure
# Important assumption: automaton are hereby assume to be determinist, that means that from one state, or outside the automata (entering transition) an inputElement can only lead to one other state or (exclusive) the exit.



# Imports ##################################################################### 
from alicia.utils import *



# Specifics ###################################################################
idAutomata = 0
idState = 0
idTransition = 0



# Automata ####################################################################
class Automata:
    """
        An automata is a structure composed of states linked with transitions. These states can serve as start or end of the automata.
    """
    def __init__(self, states, enteringTransitions, name=None):
        """
            @param (List(State))states: states of the automata.
            @param (List(Transition))enteringTransitions: transitions entering the automata.
            @param (String)name: name of the automata
        """
        assert(type(states) is list)
        assert(type(enteringTransitions) is list)

        global idAutomata
        self.idAutomata = idAutomata
        idAutomata += 1
        self.name = name
        if self.name is None:
            self.name = "Automata {0}".format(self.idAutomata)

        self.states = states
        self.enteringTransitions = enteringTransitions

        # We start outside of the automata
        self.currentState = None


    def __str__(self):
        string = "[{0}\nStates: ".format(self.name) + ", ".join(map(lambda x: x.name, self.states)) + "\nTransitions: " + "\n\t".join(map(str, self.enteringTransitions)) + "]"
        return string


    def enter(self, inputElement):
        """
            Enter the automata with a specific input.
            @param (String)inputElement
            @return (String)outputElement
        """
        for enteringTransition in self.enteringTransitions:
            if enteringTransition.inputElement == inputElement:
                # Assumption: determinist automata
                self.currentState = enteringTransition.pointedState
                return enteringTransition.outputElement
        else:
            log("The inputElement {0} leads nowhere in the automata {1}.".format(inputElement, self.name))
            self.currentState = None
            return ""


    def next(self, inputElement):
        """
            Go the next state in the automata, guided by a specific input.
            @param (String)inputElement
            @return (String)outputElement
        """
        # We are outside the automata
        if self.currentState is None:
            # So we enter it
            self.enter(inputElement)

        else:
            transition = self.currentState.next(inputElement)
            if transition is None:
                log("The inputElement {0} leads nowhere in the automata {1} from the state {2}.".format(inputElement, self.name, self.currentState.name))
                return ""
            else:
                self.currentState = transition.pointedState
                return transition.outputElement


# State #######################################################################
class State:
    """
        A state is an element of an automata. It can lead to other states of the same automata through transitions.
    """
    def __init__(self, transitions=[], name=None):
        """
            @param (List(Transition))transitions: transitions going out of this state.
            @param (String)name
        """
        global idState
        self.idState = idState
        idState += 1
        self.name = name
        if self.name is None:
            self.name = "State {0}".format(self.idState)

        self.transitions = transitions


    def __str__(self):
        string = "({0})".format(self.name)
        if len(self.transitions) > 0:
            string += "\n\t"
            string += "\n\t".join(map(str, self.transitions))
        return string

    def next(self, inputElement):
        """
            @param (String)inputElement
            @return (Transition)transition: the transition executed by the input, None if no transitions match the input.
        """
        for transition in self.transitions:
            if inputElement == transition.inputElement:
                return transition
        else:
            return None


# Transition ##################################################################
class Transition:
    def __init__(self, inputElement, outputElement, pointedState=None, name=None):
        """
            @param (String)inputElement: input needed to execute this transition.
            @param (String)outputElement: output provided by this transition.
            @param (State)pointedState: state pointed by this transition, None for transitions exiting the automata.
            @param (String)name
        """
        global idTransition
        self.idTransition = idTransition
        idTransition += 1
        self.name = name
        if self.name is None:
            self.name = "Transition {0}".format(self.idTransition)

        self.inputElement = inputElement
        self.outputElement = outputElement
        self.pointedState = pointedState


    def __str__(self):
        if self.isExiting():
            return "{0}: -{1}/{2}->".format(self.name, self.inputElement, self.outputElement)
        else :
            return "{0}: -{1}/{2}-> ({3})".format(self.name, self.inputElement, self.outputElement, self.pointedState.name)


    def isExiting(self):
        """
            Tell if a transition exits the automata.
        """
        return self.pointedState is None 
