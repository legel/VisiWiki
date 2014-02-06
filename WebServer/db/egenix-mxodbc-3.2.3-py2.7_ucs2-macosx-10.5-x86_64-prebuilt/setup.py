#!/usr/bin/env python

""" Distutils Setup File for mxODBC.

"""
#
# Load configuration(s)
#
import egenix_mxodbc
configurations = (egenix_mxodbc,)

#
# Run distutils setup...
#
import mxSetup
mxSetup.run_setup(configurations)
