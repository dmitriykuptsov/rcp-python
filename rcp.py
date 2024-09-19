#!/usr/bin/python3

# Copyright (C) 2024 strangebit
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Dmitriy Kuptsov"
__copyright__ = "Copyright 2024, strangebit"
__license__ = "GPL"
__version__ = "0.0.1b"
__maintainer__ = "Dmitriy Kuptsov"
__email__ = "dmitriy.kuptsov@strangebit.io"
__status__ = "development"

# Import the needed libraries
# RE library
import re
# SSH/SFTP client library
import paramiko
# Timing 
import time
#from time import time
# Arguments parser
import argparse
# Utils
from utils import list_files, hash_file
# Import OS file
import os

def main():
    """
    Main function which used to run the remote file copy commands

    """
    parser = argparse.ArgumentParser(
                        prog='rcp',
                        description='Copies files and folders to remote Unix machine')

    parser.add_argument("--src", dest="src", required=True, help="Source folder or file to be copied")
    parser.add_argument("--dst", dest="dst", required=True, help="Destination folder where the files will be copied to")
    parser.add_argument("--host", dest="host", required=True, help="Remote machine to connect to")
    parser.add_argument("--port", dest="port", required=True, help="Default port for the SSH server")
    parser.add_argument("--user", dest="user", required=True, help="Username to use for authentication on the remote machine")
    parser.add_argument("--password", dest="password", required=False, default=None, help="Password to be used for the connection")
    parser.add_argument("--identity", dest="id", required=False, default=None, help="SSH private key to use for authentication on the remote machine")
    args = parser.parse_args()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    if args.password != None:
        # Attempt to connect using password
        client.connect(hostname=args.host, port=args.port, username=args.user, password=args.password)
    else:
        # Attempt to connect using authentication key
        try:
            client.connect(hostname=args.host, port=args.port, username=args.user, key_filename=args.id)
        except Exception as e:
            print(e)
            print("All authentication combinations have failed...Bye...")
            exit(-1)
    for p in list_files(args.src):
        file = p.strip()
        hash_local = None
        try:
            hash_local = hash_file(file)
        except Exception as e:
            print("Error while copying the file %s %s" % (file, str(e)))
            continue
        print("Doing file copy operation: %s %s" % (hash_local, file))
        
        dst = "".join([args.dst, "/", file.strip()])
        _stdin, _stdout,_stderr = client.exec_command("sha256sum %s | awk -F\" \" '{print $1}'" % dst)
        
        hash_remote = _stdout.read().decode().strip()
        if hash_remote != hash_local:
            print("Copying file: %s to %s" % (file.strip(), dst.strip()))
            sftp = paramiko.SFTPClient.from_transport(client.get_transport())
            try:
                try:
                    sftp.put(localpath=file, remotepath=dst.strip())
                except:
                    dirname, basename = os.path.split(dst.rstrip('/'))
                    client.exec_command("mkdir -p %s" % dirname) 
                    sftp.put(localpath=file, remotepath=dst.strip())
            except Exception as e:
                print("Error while copying the file %s %s" % (dst, str(e)))
        else:
            print("Files are the same")
    client.close()
    
if __name__ == "__main__":
    main()