# Distributed Group Membership

## Introduction

This service maintains at each machine in the system, a list of the other machines that are connected and up. This membership list needs to be updated when:
* A machine joins the group
* A machine voluntarily leaves the group
* A machine crashes from the group

A machine failure must be reflected in at least one membership lists within 3 seconds called time-bounded completeness, and it must be provided no matter what the network latencies are. A machine failure, join or leave must be reflected within 6 seconds at all membership lists.

## Requirements

python2.7

## Logs

Generated log files include:
* clientdebug.log: Generated from client.py
* intro.log: Generated from intro.py
* serverdebug.log: Generated from server.py
* node.log: Generated from node.py

Make your logs are verbose as possible. At least you must log:
* Each time a change is made to the local membership list (join, leavel or failure)
* Each time a failure is detected or communicated from one machine to another

## File List
### Distributed Grep
* client.py: Client code
* server-names.txt: File input with the hostnames of servers
* server.py: Server code

### Group Membership
* console.py: Code for each node
* failure_detector.py: Failure Detection code for each node
* intro.py: Code for introducer
* memlist: Membership List
* node.py: Code for node to handle commandline commands
* util.py: Has basic broadcast and unicast functionality

## Commands

ls - list the membership list

li - list self's id

join - join the group

leave - voluntarily leave the group

exit - exit program

## Code Example

### Start Introducer

python intro.py

### Start Node

python console.py

### Start distributed grep server

python server.py &

### Start distributed grep client

python client.py server-names.txt 'grep <command> <files>'
