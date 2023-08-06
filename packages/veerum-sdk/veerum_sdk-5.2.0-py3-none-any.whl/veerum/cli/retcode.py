"""
Standard return code values for the Veerum CLI

.. _Reserved linux exit codes
   http://www.tldp.org/LDP/abs/html/exitcodes.html
"""

OK = 0
GENERAL_ERROR = 1

# IO error codes
WOULD_OVERWRITE_EXISTING = 100
NOT_A_FILE = 101
NOT_A_DIRECTORY = 102

# General error codes
AUTHENTICATION_FAILED = 124
CONFIGURATION_ERROR = 125
NOT_IMPLEMENTED = 126
