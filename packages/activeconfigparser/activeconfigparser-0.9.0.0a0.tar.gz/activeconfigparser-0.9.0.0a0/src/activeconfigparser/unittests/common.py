#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; py-continuation-offset: 4 -*-
#===============================================================================
# Copyright Notice
# ----------------
# Copyright (c) 2021, National Technology & Engineering Solutions of Sandia, LLC (NTESS).
#    Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
#    certain rights in this software.
# Copyright (c) 2023, William McLendon
#
# License (3-Clause BSD)
# ----------------------
# Copyright (c) 2021, National Technology & Engineering Solutions of Sandia, LLC (NTESS).
#    Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
#    certain rights in this software.
# Copyright (c) 2023, William McLendon
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#===============================================================================
"""
Helper functions for testing
"""
import os

#===============================================================================
#
# Mock Helpers
#
#===============================================================================



def mock_function_noreturn(*args):
    """
    Mock a function that does not return a value (i.e., returns NoneType)
    """
    print("\nmock> f({}) ==> NoneType".format(args)) # pragma: no cover



def mock_function_pass(*args):
    """
    Mock a function that 'passes', i.e., returns a 0.
    """
    print("\nmock> f({}) ==> 0".format(args)) # pragma: no cover
    return 0                                  # pragma: no cover



def mock_function_fail(*args):
    """
    Mock a function that 'fails', i.e., returns a 1.
    """
    print("\nmock> f({}) ==> 1".format(args)) # pragma: no cover
    return 1                                  # pragma: no cover



#===============================================================================
#
# General Utility Functions
#
#===============================================================================



def find_config_ini(filename="config.ini", rootpath="."):
    """
    Recursively searches for a particular file among the subdirectory structure.
    If we find it, then we return the full relative path to `pwd` to that file.

    The _first_ match will be returned.

    Args:
        filename (str): The _filename_ of the file we're searching for. Default: 'config.ini'
        rootpath (str): The _root_ path where we will begin our search from. Default: '.'

    Returns:
        String containing the path to the file if it was found. If a matching filename is not
        found then `None` is returned.

    """
    output = None
    for dirpath, dirnames, filename_list in os.walk(rootpath):
        if filename in filename_list:
            output = os.path.join(dirpath, filename)
            break
    if output is None:
        raise FileNotFoundError("Unable to find {} in {}".format(filename, os.getcwd())) # pragma: no cover
    return output
