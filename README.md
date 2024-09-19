# rcp-python
This is a simple Python-based remote copy utility. It is based on Paramiko library to
establish remote ssh connections.

Before the usage one needs to install paramiko SSH library as so:

```
$ pip3 isntalling paramiko
```

Usage:
```
$ python3 rcp.py --src [folder or file] --dst [folder] --host [remote host] --port [remote port] --user [remote username] --password [remote password]
```
Example usage:

```
$ python3 rcp.py --src test.txt --dst ~ --host 192.168.0.20 --port 22 --user root --password 123456
```