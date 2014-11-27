#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2010, Nikita Kazeev with special thanks to
# Timur Iskhodzhanov
# Alexander Travov
# Alex Bochkarev
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# Description:
# A simple script for authorization in the mipt network
# Wrote for login page present at 12 December, 2010

from urllib import urlopen
from hashlib import md5
import re
from sys import stderr
from glib import set_application_name
import argparse

def get_creditals():
    return ('535195', 'dolboutka')

def login():
    login_page_url = "http://login.telecom.mipt.ru/"
    try:
        login_page = urlopen(login_page_url)
        login_page = login_page.read()
    except:
        stderr.write("Error while accessing login page. Likely to be a networking problem.\n")
        exit(-1)

    try:
        found = re.search('(?<=<INPUT type=hidden name=chalangeack value=)\w*',
                          login_page)
        chalangeack = found.group(0)
    except:
        stderr.write("Error while manipulating login page. Maybe its format has changed.\n")
        exit(-2)

    (login, password) = get_creditals()

    password_hash = md5(chalangeack + password).hexdigest()

    res_page = urlopen(login_page_url + "bin/login.cgi?chalangeack=" +
                    chalangeack + "&login=" + login + "&password=" + password_hash)
    res_page = res_page.read()

    if re.search("Авторизация прошла успешно.", res_page) == None:
        stderr.write("Invalid response. Authorization is almost certainly incomplete. Probably invalid creditals.\n")
        exit(-3)
    else:
        print "Login: Success"
        exit(0)

def logout():
    logout_page_url = "http://login.telecom.mipt.ru/bin/logout.cgi"
    try:
        logout_page = urlopen(logout_page_url)
        logout_page = logout_page.read()
    except:
        stderr.write("Error while accessing logout page. Likely to be a networking problem.\n")
        exit(-1)

    if re.search("Выход выполнен.", logout_page) == None:
        stderr.write("Invalid response. Log out is almost certainly incomplete.\n")
        exit(-3)
    else:
        print "Logout: Success"
        exit(0)


parser = argparse.ArgumentParser(description='Log in/out mipt telecom account')
parser.add_argument('-in', '--log-in', action='store_true', help='log in')
parser.add_argument('-out', '--log-out', action='store_true', help='log out')

args = parser.parse_args()

if args.log_in:
    login()
elif args.log_out:
    logout()
else:
    parser.print_help()
