# STMPY Components

This repository shows some examples how to build components in Python based
on MQTT for communication, JSON for serialization and STMPY for the
implementation of state machines.

The code examples are given for educational purposes, not professional deployment.


## Installation and Dependencies

    pip install paho-mqtt
    pip install stmpy



## TimerManager

This is a specific example of a component that listens to MQTT for incoming
commands and reacts. The component realizes a manager for timers that can be
started from a voice assistant.

Documented source code: https://falkr.github.io/stmpy-components/TimerManager.m.html


## MQTT Paho

Paho provides communication via MQTT.

* [Paho Description](https://pypi.python.org/pypi/paho-mqtt/)
* [Paho Source Code](https://github.com/eclipse/paho.mqtt.python)


## JSON

JSON supports to serialize data objects into strings, and back again.

* [JSON Description](https://docs.python.org/3/library/json.html)


## STMPY

STMPY provides support for state machine in Python.

* [STMPY Documentation](https://falkr.github.io/stmpy/)
* [STMPY API Documentation](https://falkr.github.io/stmpy/stmpy/)
* [Source Code on Github](https://github.com/falkr/stmpy)
* [Jupyter Notebooks with Examples](https://github.com/falkr/stmpy-notebooks)
