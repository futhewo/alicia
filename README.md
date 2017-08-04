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

# Example

**TODO**
