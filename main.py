from choice import ChoiceWizard as Choice
from net import NetWizard as Net
from merger import DataMerger as Merger
import json
import time
import os


def __main__():
    if os.path.exists('./extracted') is False:
        os.mkdir('./extracted')
    Choice().run()
    Net().run()
    Merger().run()
    
__main__()