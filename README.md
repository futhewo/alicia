# Alicia 0.200

## What is it ?

Alicia is a fuzz-test generator. You must first define a grammar, then Alicia will provide mutation elements from this grammar according to several either generic, or specific (linked to data-type) oracles.
It was designed to *fuzz* black-box equipment and as such does not provide any feedback or debugging probe.

# Features

Alicia features several key elements:
* Grammar definition framework based on a tree representation with nodes and fields (leaves)
* Grammar mutation framework based on generic (mutation, add, remove, swap, for nodes and generic fields) or specific (linked to the data-type of fields) oracles
* Several data-types (known as Contents): Integer (both little and big-endian), String, BitArray, Careful
* Grammar parsing: parse inputs and try to identify them as elements from the grammar
* Communication automata: use its generation and parsing capacity to communicate with a neighboring element using the same grammar
* Automata fuzzing: fuzz some messages in this automata, or the order of messages


# Model

## Architecture

Exchanges are modelized in an automata. This automata is composed of states and transitions leading from one state to another state. A transition is trigggered when a specific message *input* is received, which then produced a specific *output* message.

A message is modelized as a tree. This tree contains *Elements* that can either be nodes or leaves. The nodes of this tree are:
* *Node*: returns a concatenation of his subelements.
* *Choice*: returns one of his subelements.

The leaves of the tree are the fields of the message, they can either be structural fields or simple data fields.

The sructural fields are: 
* *SizeField*: computes the size of a node.
* *CountField*: computes the number of occurences of another element.
* *PaddingField*: pads a node up to a given size.

The data fields are:
* *StaticField*: is never modified.
* *CloseField*: can be modified, but not in size.
* *OpenField*: can be modified, in all possible ways.

Fields are associated to a *Content*, an object that holds the value and the type of the data the field holds.
The contents are:
* *Content*: very lousy datatype.
* *BinaryContent*: binary datatype, acts as if there is no type specified.
* *CarefulContent*: very conservative datatype.
* *IntegerContent*: integer data.
* *StringContent*: string data.

## Fuzzing

Fuzzing can be applied on every object described before. If this object as subelements, it will be applied on its subelements. For example, below is what happens when we fuzz one of the previous element:
* automata: TODO
* node: may add, mute, swap or remove subelements ; or may fuzz one of its subelements (nodes or fields).
* choice: may change the choosen ; or may fuzz one of its subelements (nodes or fields).
* static field: do nothing.
* close field: may mute or swap one of its character ; or may fuzz its content.
* open field: may add, mute, swap or remove characters ; or may fuzz its content.
* size field: fuzzed as a close field.
* content: apply specific datatype fuzzing oracle. 

