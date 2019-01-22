#! /usr/bin/env python

import argparse
import json
import mysql.connector
from mysql.connector import Error

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--list', default=False, action='store_true')
PARSER.add_argument('--host', default=None)
ARGS = PARSER.parse_args()

try:
    CONNECTION = mysql.connector.connect(
        host='192.168.250.10', user='ansible', passwd='ansible',
        database='ansible')
    CURSOR = CONNECTION.cursor()
except Error as e:
    print "Error while connecting to MySQL", e

INVENTORY = dict()

GROUPS = dict()
CURSOR.execute('SELECT id, name FROM groups;')
for row in CURSOR.fetchall():
    GROUPS[row[0]] = row[1]

CHILDGROUPS = dict()
CURSOR.execute('SELECT childid, parentid FROM childgroups;')
for row in CURSOR.fetchall():
    CHILDGROUPS[row[0]] = row[1]

GROUPVARS = dict()
CURSOR.execute('SELECT groupid, name, value FROM groupvars;')
for row in CURSOR.fetchall():
    group_lookup = GROUPVARS.get(row[0])
    if group_lookup is None:
        GROUPVARS[row[0]] = dict()
    GROUPVARS[row[0]][row[1]] = row[2]

HOSTS = dict()
CURSOR.execute('SELECT id, name FROM hosts;')
for row in CURSOR.fetchall():
    HOSTS[row[0]] = row[1]

HOSTGROUPS = dict()
CURSOR.execute('SELECT hostid, groupid FROM hostgroups;')
for row in CURSOR.fetchall():
    HOSTGROUPS[row[0]] = row[1]

for group_id, group_name in GROUPS.items():
    hosts = []
    for host_id, name in HOSTS.items():
        hostgroup_lookup = HOSTGROUPS.get(host_id)
        if hostgroup_lookup is not None:
            if hostgroup_lookup == group_id:
                hosts.append(name)
    child_lookup = CHILDGROUPS.get(group_id)
    if child_lookup is None:
        group_lookup = INVENTORY.get(group_name)
        if group_lookup is None:
            INVENTORY[group_name] = dict()
            INVENTORY[group_name]['children'] = dict()
            INVENTORY[group_name]['hosts'] = hosts
            INVENTORY[group_name]['vars'] = dict()
            for var_group_id, var in GROUPVARS.items():
                if var_group_id == group_id:
                    for k, v in var.items():
                        INVENTORY[group_name]['vars'][k] = v
    else:
        parent = GROUPS.get(child_lookup)
        group_lookup = INVENTORY.get(parent)
        if group_lookup is None:
            INVENTORY[parent] = dict()
            INVENTORY[parent]['children'] = dict()
            INVENTORY[parent]['hosts'] = hosts
            INVENTORY[parent]['vars'] = dict()
            for var_group_id, var in GROUPVARS.items():
                if var_group_id == group_id:
                    for k, v in var.items():
                        INVENTORY[parent]['vars'][k] = v
        INVENTORY[parent]['children'][group_name] = dict()
        INVENTORY[parent]['children'][group_name]['hosts'] = hosts
        INVENTORY[parent]['children'][group_name]['vars'] = dict()
        for var_group_id, var in GROUPVARS.items():
            if var_group_id == group_id:
                for k, v in var.items():
                    INVENTORY[parent]['children'][group_name]['vars'][k] = v

UNGROUPED_HOSTS = []
for host_id, name in HOSTS.items():
    hostgroup_lookup = HOSTGROUPS.get(host_id)
    if hostgroup_lookup is None:
        UNGROUPED_HOSTS.append(name)
INVENTORY['ungrouped'] = dict()
INVENTORY['ungrouped']['hosts'] = UNGROUPED_HOSTS

INVENTORY['_meta'] = dict()
INVENTORY['_meta']['hostvars'] = dict()

CURSOR.execute('SELECT hostid, name, value FROM hostvars;')
for row in CURSOR.fetchall():
    host = HOSTS.get(row[0])
    host_lookup = INVENTORY['_meta']['hostvars'].get(host)
    if host_lookup is None:
        INVENTORY['_meta']['hostvars'][host] = dict()
    INVENTORY['_meta']['hostvars'][host][row[1]] = row[2]

print json.dumps(INVENTORY, indent=4)
