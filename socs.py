from bs4 import BeautifulSoup
from sshtunnel import SSHTunnelForwarder
import requests

# enter your login info
studentNumber = ''

# by default, the password is the last 8 digits of your student card
studentPassword = ''

# your socs password
socsPassword = ''


# No changes necessary after this line #
# ------------------------------------ #

print('Fetching, your grades, hold on...')


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


def login_to_socs(prt):
    global r, session
    url = 'https://localhost:' + prt + '/ETHICS/'
    login = {
        'login': studentNumber,
        'pw': socsPassword
    }
    # auth
    requests.packages.urllib3.disable_warnings()
    r = session.post(url + 'login.cfm', data=login, verify=False, allow_redirects=True)


login_to_socs(port)
server.stop()


# get the marks
soup = BeautifulSoup(r.text)
marks = soup.find("div", id="marksdiv")


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