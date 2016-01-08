import os
import multiprocessing
import json

# # #
# 0 - the defs
# # #
class SfMInstanceConfig:    
    # the defs
    def __init__(self):
        self.CURRENT_DIR = os.getcwd()
        self.BIN_PATH_ABS = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        self.PYOPENCV_PATH = os.path.join(self.BIN_PATH_ABS, 'lib/python2.7/dist-packages')
        self.OPENSFM_PATH = os.path.join(self.BIN_PATH_ABS, "src/OpenSfM")
        self.CORES = multiprocessing.cpu_count()
        osType = os.name
        dictOSBins = {}
    
        if osType == 'posix':
            BIN_PATH = self.BIN_PATH_ABS + os.sep +"bin"
            dictOSBins['exeJhead']   = 'jhead'
            dictOSBins['exeSift']    = 'vlsift'
        elif os.name == 'nt':
            BIN_PATH = self.BIN_PATH_ABS + os.sep +"bin_win"
            dictOSBins['exeJhead']   = 'jhead.exe'
            dictOSBins['exeSift']    = 'SimpleSift.exe'
        
        self.dictOSBins = dictOSBins
        self.BIN_PATH = BIN_PATH
        
        def get_ccd_widths():
            """Return the CCD Width of the camera listed in the JSON defs file."""
            with open(self.BIN_PATH_ABS + '/ccd_defs.json') as jsonFile:
                return json.load(jsonFile)  
        
        self.dictCCDWidths = get_ccd_widths()

