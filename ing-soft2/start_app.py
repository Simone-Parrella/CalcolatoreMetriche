import sys
import os
from controller.StartAppContoller import StartAppController
import time
from view.App import IngSoftApp
from view.StartupErrorPage import StartupErrorPage

if __name__ == "__main__":
    """ entry point dell'applicazione """

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

    start = StartAppController()

    status = start.startComputationEndpoint()
    time.sleep(5)

    isInstalled, version = start.isGitInstalled()
    response = start.isComputeEndpointActive()

    if isInstalled:
        IngSoftApp(gitv=version, endpointStatus=status)
    else:
        StartupErrorPage()
