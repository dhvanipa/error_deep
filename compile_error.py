#!/usr/bin/python
#    Copyright 2017 Joshua Charles Campbell
#
#    This file is part of UnnaturalCode.
#    
#    UnnaturalCode is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    UnnaturalCode is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with UnnaturalCode.  If not, see <http://www.gnu.org/licenses/>.

from six import integer_types

class CompileError(object):
    def __init__(self, 
                 filename=None, 
                 line=None, 
                 column=None, 
                 functionname=None,
                 text=None,
                 errorname=None):
        assert line is not None
        assert isinstance(line, integer_types)
        self.filename = filename
        self.line = line
        self.functionname = functionname
        self.text = text
        self.errorname = errorname
        if column is not None:
            assert isinstance(column, integer_types)
        self.column = column

"""
Compile result should be a list of CompileError objects,
or if compile was successful, None (no list at all).
"""

