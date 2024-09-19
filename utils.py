
#!/usr/bin/python

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

# OS stuff
import os
# Hash stuff
import hashlib

def list_files(file_or_dir="."):
    stdout = os.popen("find %s -name '*'" % file_or_dir).readlines()
    return stdout

def hash_file(filename):
    if not filename:
        return None
    fd = open(filename, mode="rb")
    data = fd.read()
    h = hashlib.new("sha256")
    h.update(data)
    return h.hexdigest()