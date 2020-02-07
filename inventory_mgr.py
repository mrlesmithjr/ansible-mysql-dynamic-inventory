#!/usr/bin/env python


import argparse
import operator
import os
import json
import mysql.connector
from mysql.connector import Error


def main():
    args = get_args()
    connection = connect(args)
    cursor = connection.cursor()
    main_menu(args, connection, cursor)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dbhost', default='192.168.250.10')
    args = parser.parse_args()
    return args


def main_menu(args, connection, cursor):
    while True:
        os.system('clear')
        menu_options = {'01': 'Host Management',
                        '02': 'Group Management',
                        '99': 'Exit'}
        menu_sorted = sorted(menu_options.items(), key=operator.itemgetter(0))
        menu_title = 'Main Menu'
        print('\n{0}:'.format(menu_title))
        for item in menu_sorted:
            print('{0}. {1}'.format(item[0], item[1]))
        option_id = raw_input('\nOption ID: ')
        response = menu_options.get(option_id)
        if response is not None:
            if option_id == '01':
                host_management(args, connection, cursor)
            elif option_id == '02':
                group_management(args, cursor)
            elif option_id == '99':
                break
        else:
            print('Please choose a valid option.')
            raw_input('Press Enter to try again: ')


def connect(args):
    try:
        connection = mysql.connector.connect(
            host=args.dbhost, user='ansible', passwd='ansible',
            database='ansible')
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)


def host_management(args, connection, cursor):
    while True:
        os.system('clear')
        menu_options = {'01': 'Get Hosts',
                        '02': 'Add Host',
                        '99': 'Back'}
        menu_sorted = sorted(menu_options.items(), key=operator.itemgetter(0))
        menu_title = 'Main Menu'
        print('\n{0}:'.format(menu_title))
        for item in menu_sorted:
            print('{0}. {1}'.format(item[0], item[1]))
        option_id = raw_input('\nOption ID: ')
        response = menu_options.get(option_id)
        if response is not None:
            if option_id == '01':
                get_hosts(args, cursor)
            elif option_id == '02':
                add_host(args, connection, cursor)
            elif option_id == '99':
                break
        else:
            print('Please choose a valid option.')
            raw_input('Press Enter to try again: ')


def get_hosts(args, cursor):
    os.system('clear')
    hosts = dict()
    cursor.execute("SELECT id, name FROM hosts;")
    for row in cursor.fetchall():
        host_id = row[0]
        name = row[1]
        cursor.execute(
            "SELECT name, value FROM hostvars WHERE hostid='{0}'".format(
                host_id))
        host_vars = cursor.fetchall()
        hosts[name] = dict()
        hosts[name]['hostvars'] = dict()
        for hostvar in host_vars:
            hosts[name]['hostvars'][hostvar[0]] = hostvar[1]
    print(json.dumps(hosts, indent=4))
    raw_input('Press Enter: ')


def add_host(args, connection, cursor):
    while True:
        os.system('clear')
        host = raw_input('Enter host to add: ')
        if host is not None:
            cursor.execute(
                "SELECT id FROM hosts WHERE name='{0}'".format(host))
            host_check = cursor.fetchone()
            if host_check is None:
                cursor.execute(
                    "INSERT INTO hosts (name) VALUES ('{0}');".format(host))
                connection.commit()
                print(cursor.lastrowid)
                raw_input('Host: [{0}] successfully added.'.format(host))
                break
            else:
                print('Host [{0}] already exists.'.format(host))
                raw_input('Press Enter to Contine: ')


def group_management(args, cursor):
    while True:
        os.system('clear')
        menu_options = {'01': 'Get Groups',
                        '02': 'Add Groups',
                        '99': 'Back'}
        menu_sorted = sorted(menu_options.items(), key=operator.itemgetter(0))
        menu_title = 'Main Menu'
        print('\n{0}:'.format(menu_title))
        for item in menu_sorted:
            print('{0}. {1}'.format(item[0], item[1]))
        option_id = raw_input('\nOption ID: ')
        response = menu_options.get(option_id)
        if response is not None:
            if option_id == '01':
                get_groups(args, cursor)
            # elif option_id == '02':
            #     add_hosts(args, cursor)
            elif option_id == '99':
                break
        else:
            print('Please choose a valid option.')
            raw_input('Press Enter to try again: ')


def get_groups(args, cursor):
    os.system('clear')
    groups = dict()
    cursor.execute("SELECT id, name FROM groups;")
    for row in cursor.fetchall():
        group_id = row[0]
        name = row[1]
        cursor.execute(
            "SELECT name, value FROM groupvars WHERE groupid='{0}'".format(
                group_id))
        group_vars = cursor.fetchall()
        groups[name] = dict()
        groups[name]['vars'] = dict()
        for groupvar in group_vars:
            groups[name]['vars'][groupvar[0]] = groupvar[1]
    print(json.dumps(groups, indent=4))
    raw_input('Press Enter: ')


if __name__ == '__main__':
    main()
