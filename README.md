# SoCsConnect
A small command line utility to retrieve student grades from SoCs online system

**Run a vitual environment**
If you don't want to have the dependencies on your system.

```bash
mkvirtualenv socs-connect
```

**Install dependancies**
```bash
pip install -r requirements.txt
```

**Change your username and password**
Got to the `socs.py` file. Look at the first few lines:
```python
# enter your login info
studentNumber = ''

# by default, the password is the last 8 digits of your student card
studentPassword = ''

# your socs password
socsPassword = ''
```
**Run the script**
```bash
python socs.py
```
To be super hipster you could do
```bash
chmod +x socs.py
```
And from then on run it like so `./socs.py`