#!/usr/bin/python
from bs4 import BeautifulSoup
from sshtunnel import SSHTunnelForwarder
import requests
import os.path
import sys
import time

global studentNumber, studentPassword, socsPassword
studentNumber = ''
studentPassword = ''
socsPassword = ''

credentials = [studentNumber, studentPassword, socsPassword]

def update_progress(progress):
    print '\r[{0}] {1}%'.format('#'*(progress/10), progress)

def progress_bar():
    print('Fetching, your grades, hold on...')
    print 'Loading....  ',
    sys.stdout.flush()

    for i in range(10):
        if (i % 4) == 0: sys.stdout.write('\b/')
        elif (i % 4) == 1: sys.stdout.write('\b-')
        elif (i % 4) == 2: sys.stdout.write('\b\\')
        elif (i % 4) == 3: sys.stdout.write('\b|')
        sys.stdout.flush()
        time.sleep(0.2)
            
    print '\b\b done!'

def generate_config():
    # enter your login info
    studentNumber = raw_input("Enter your login info (GUID): \n")

    # by default, the password is the last 8 digits of your student card
    studentPassword = raw_input("Linux password (last 8 digits of your card): \n")

    # your socs password
    socsPassword = raw_input("SoCs password: \n")

    output = '%s\n%s\n%s' % (studentNumber, studentPassword, socsPassword)
    write_config(output)

def write_config(output):
    fname = 'config.txt'
    with open(fname, 'w') as fout:
        fout.write(output)

def read_config():
    global studentNumber, studentPassword, socsPassword
    file = open('config.txt', 'r')
    for detail in credentials:
         detail = file.readline().strip()

def login_to_socs(prt):
    #global studentNumber, studentPassword, socsPassword
    global r, session

    print 'login_to_socs: ' +studentNumber
    url = 'https://localhost:' + prt + '/ETHICS/'
    login = {
        'login': studentNumber,
        'pw': socsPassword
    }
    # auth
    requests.packages.urllib3.disable_warnings()
    r = session.post(url + 'login.cfm', data=login, verify=False, allow_redirects=True)
    return r

def generate_table(soup, marks):
    # get your name
    print(marks.h1.next_sibling.next_sibling.string)

    # get course name/ assignment/ grade into a list
    table = [[column for column in list(row.stripped_strings)[:3]] for row in marks.table('tr')]

    # create a format specifier for each column
    padding = 2
    colLens = [max(map(len, column)) + padding for column in zip(*table)]
    stringFormat = ''.join('{{:{}}}'.format(width) for width in colLens)

    # print the table
    for row in table:
        print(stringFormat.format(*row))

def start_server():
    # Setup our tunnel
    server = SSHTunnelForwarder(
        ssh_address=('sibu.dcs.gla.ac.uk', 22),
        ssh_username=studentNumber,
        ssh_password=studentPassword,
        remote_bind_address=('webapps.dcs.gla.ac.uk', 443))

    server.start()
    port = str(server.local_bind_port)

    # Scrape the SOCS site
    session = requests.Session()
    r = ''

    r = login_to_socs(port)
    server.stop()
    return r

if (not os.path.isfile('config.txt')):
    generate_config()

read_config()

print studentNumber

# Loading
progress_bar()

# Accessing socs
r = start_server()

# get the marks
soup = BeautifulSoup(r.text)
marks = soup.find("div", id="marksdiv")

generate_table(soup, marks)