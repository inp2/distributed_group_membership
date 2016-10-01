# Distributed Group Membership

## Introduction

This service maintains at each machine in the system, a list of the other machines that are connected and up. This membership list needs to be updated when:
* A machine joins the group
* A machine voluntarily leaves the group
* A machine crashes from the group

A machine failure must be reflected in at least one membership lists within 3 seconds called time-bounded completeness, and it must be provided no matter what the network latencies are. A machine failure, join or leave must be reflected within 6 seconds at all membership lists.

## Motivation

## Requirements

python2.7

## Message Format

## Logs

Make your logs are verbose as possible. At least you must log:
* Each time a change is made to the local membership list (join, leavel or failure)
* Each time a failure is detected or communicated from one machine to another

## File List

## Commands

ls - list the membership list

li - list self's id

join - join the group

leave - voluntarily leave the group

exit - exit program



## Code Example
