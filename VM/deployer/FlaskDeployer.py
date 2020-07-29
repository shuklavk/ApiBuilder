from deployer.BaseDeployer import BaseDeployer
import os
import subprocess
from onAppRunConfig.logConfig import generalLogger

class FlaskDeployer(BaseDeployer):

    # Since this is a flask app, we must run the server start code from the root directory
    def deploy(self):
        if self.isActive:
            return

        self.pidObj = subprocess.Popen(['python', self.source_directory + '/run.py'])
        #os.system('python ' + self.source_directory + '/run.py')
        print 'the pid of the user process is', self.pidObj.pid

        self.isActive = True

        generalLogger.info("API at " + self.source_directory + " successfully deployed")

    def end(self):
        if self.isActive:
            self.pidObj.kill()
            self.isActive = False

    def teardown(self):
        pass

    def restart(self):
        self.end()
        self.deploy()




