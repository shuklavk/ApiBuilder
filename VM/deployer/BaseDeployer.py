# Currently all this class does is run the code from the location provided.
# It does not make special considerations for port numbers because the assumption
# is the code is already pointed to the appropriate portnumber.

# IMPORTANT: If the logic around the port number changes, please be sure to come back and
# edit this class accordingly.

# Abilities of this class include the following:
#   - Creating a daemon process that runs the code / Should check if there is already a running process with this code
#   - Killing the daemon process if it is currently running the user's server
#   - Doing any necessary cleanup after stopping the user's service
#   - Restarting the daemon process with the exact same code / environment

# Future considerations/abilities of this class:
#   - Should set up / reinstall any necessary libraries and environmental variables for the server
#   - Should be able to clear an environment of all injected libraries and variables

from abc import ABCMeta, abstractmethod

class BaseDeployer(object):
    __metaclass__ = ABCMeta

    def __init__(self, source_directory):
        self.source_directory = source_directory
        self.pid = 0
        self.isActive = False
        self.pidObj = None

    @abstractmethod
    def deploy(self):
        pass

    @abstractmethod
    def end(self):
        pass

    @abstractmethod
    def teardown(self):
        pass

    @abstractmethod
    def restart(self):
        pass



