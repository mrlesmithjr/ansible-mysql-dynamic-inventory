#!/usr/bin/env python
"""[summary]

Returns:
    [type]: [description]
"""

import argparse
import operator
import os
import json
import mysql.connector
from mysql.connector import Error


def main():
    """[summary]"""
    args = get_args()
    connection = connect(args)
    cursor = connection.cursor()
    main_menu(args, cursor)


def get_args():
    """[summary]

    Returns:
        [type]: [description]
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbhost", default="192.168.250.10")
    args = parser.parse_args()
    return args


def main_menu(args, cursor):
    """[summary]

    Args:
        args ([type]): [description]
        cursor ([type]): [description]
    """
    while True:
        os.system("clear")  # nosec B607
        menu_options = {"01": "Get Hosts", "99": "Exit"}
        menu_sorted = sorted(menu_options.items(), key=operator.itemgetter(0))
        menu_title = "Main Menu"
        print(f"\n{menu_title}:")
        for item in menu_sorted:
            print(f"{item[0]}. {item[1]}")
        option_id = input("\nOption ID: ")
        response = menu_options.get(option_id)
        if response is not None:
            if option_id == "01":
                get_hosts(args, cursor)
            elif option_id == "99":
                break
        else:
            print("Please choose a valid option.")
            input("Press Enter to try again: ")


def connect(args):
    """[summary]

    Args:
        args ([type]): [description]

    Returns:
        [type]: [description]
    """
    try:  # nosecB106
        connection = mysql.connector.connect(
            host=args.dbhost, user="ansible", passwd="ansible", database="ansible"
        )
        return connection
    except Error as e:  # pylint: disable=invalid-name
        print("Error while connecting to MySQL", e)


def get_hosts(_args, cursor):
    """[summary]

    Args:
        _args ([type]): [description]
        cursor ([type]): [description]
    """
    hosts = dict()
    cursor.execute("SELECT id, name FROM hosts;")
    for row in cursor.fetchall():
        host_id = row[0]
        name = row[1]

        cursor.execute(
            f"SELECT name, value FROM hostvars WHERE hostid='{host_id}'"  # nosec B608
        )
        host_vars = cursor.fetchall()
        hosts[name] = dict()
        hosts[name]["hostvars"] = dict()
        for hostvar in host_vars:
            hosts[name]["hostvars"][hostvar[0]] = hostvar[1]
    print(json.dumps(hosts, indent=4))
    input("Press Enter: ")


if __name__ == "__main__":
    main()
