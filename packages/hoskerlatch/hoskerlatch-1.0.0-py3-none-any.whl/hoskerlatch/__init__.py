"""
This module defines functions which "latch" and "unlatch" folders.
"""

# Local imports.
from .latcher import Latcher
from .unlatcher import Unlatcher

#############
# FUNCTIONS #
#############

def latch(path_to, password, **kwargs):
    """ "Latch" a given folder. """
    latcher = Latcher(path_to, **kwargs)
    latcher.latch(password)
    return latcher.path_to_encrypted

def unlatch(path_to, password):
    """ "Unlatch" an encrypted folder. """
    unlatcher = Unlatcher(path_to)
    unlatcher.unlatch(password)
    return unlatcher.path_to_decrypted
