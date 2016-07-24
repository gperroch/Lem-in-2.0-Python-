# -*- coding: utf-8 -*-
import sys
import re
import curses
import time
#from visu import *


try:
    fd = open(sys.argv[1], 'r')
except:
    print 'An error occured while trying to open the file.'
    exit(1)

lines = fd.readlines()
lines = [line.strip() for line in lines]
for line in lines:
    print (line)

class Room:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = {}
        self.ant_number = 0
        self.map = []
        self.index = -1
        self.status = ""

cmd = ""
rooms = {}
total = 0
nbant = 0
for line in lines:
    if line == "##start" or line == "##end":
        cmd = line
    elif re.match(r'^[0-9A-Za-z]{1,} [0-9]{1,} [0-9]{1,}$', line):
        newRoom = Room(line.split(' ')[0], int(line.split(' ')[1]), int(line.split(' ')[2]))
        rooms[newRoom.name] = newRoom
        total += 1
        if cmd != "":
            newRoom.status = cmd
            cmd = ""
    elif re.match(r'^[0-9]{1,}$', line):
        nbant = int(line)

for line in lines:
    if re.match(r'^[0-9a-zA-Z]{1,}\-[0-9a-zA-Z]{1,}$', line):
        A = rooms[line.split('-')[0]]
        B = rooms[line.split('-')[1]]
        A.neighbors[line.split('-')[1]] = B
        B.neighbors[line.split('-')[0]] = A

#indexage
start = ""
end = ""
for value in rooms.values():
    if value.status == "##start":
        start = value
    if value.status == "##end":
        end = value
    if start and end:
        break

end.index = 0
#while end.index == -1:
while total > 1:
    for room in rooms.values():
        if room.index >= 0:
            for subroom in room.neighbors.values():
                if subroom.index == -1 or subroom.index > (room.index + 1):
                    if subroom.index == -1:
                        total -= 1
                    subroom.index = room.index + 1
#########

# MAPPING #
for room in rooms.values():
    for neighbor in room.neighbors.values():
        if neighbor.index < room.index:
            room.map.append(neighbor)
#    print room.map
###########

# DEPLACEMENT #
start.ant_number = nbant
while end.ant_number < nbant:
    for room in rooms.values():
        #print room.name
        if room.ant_number and room.index == 1:
            print "L%d-%s" % (room.ant_number, end.name)
            room.ant_number = 0
            end.ant_number += 1
        elif room.ant_number and room.status == "##start":
            next_step = 0
            for neighbor in room.map:
                if neighbor.ant_number == 0 and neighbor.index < room.index:
                    next_step = neighbor
                    break
            if next_step.ant_number == 0 and next_step.index < room.index:
                next_step.ant_number = room.ant_number
                room.ant_number -= 1
                print "L%d-%s" % (next_step.ant_number, next_step.name)
        elif room.ant_number and room.status == "":
            next_step = 0
            for neighbor in room.map:
                if neighbor.ant_number == 0 and neighbor.index < room.index:
                    next_step = neighbor
                    break
            if next_step.ant_number == 0 and next_step.index < room.index:
                next_step.ant_number = room.ant_number
                room.ant_number = 0
                print "L%d-%s" % (next_step.ant_number, next_step.name)

###############

def resume():
    print "Résumé des pièces"
    print rooms
    for room in rooms.values():
        print "---------------------------"
        print "%s: (%d,%d) index: %d" % (room.name, room.x, room.y, room.index)
        print room.neighbors

#resume()
#deplacement()
