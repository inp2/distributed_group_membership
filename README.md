# Distributed Group Membership

## Introduction

This service maintains at each machine in the system, a list of the other machines that are connected and up. This membership list needs to be updated when:
* A machine joins the group
* A machine voluntarily leaves the group
* A machine crashes from the group

## Motivation

## Requirements

python2.7

## Message Format

## Logs

Make your logs are verbose as possible. At least you must log:
* Each time a change is made to the local membership list (join, leavel or failure)
* Each time a failure is detected or communicated from one machine to another

## File List

## Basic Code

## Code Example

### Start Introducer Node

python intro.py

### Start Nodes

python console.py

### Run Basic Command-line Commands
id - List the node's id
ls - List the membership list
join - Join the cluster
leave - Voluntarly leave the cluster
exit - Exit the program
