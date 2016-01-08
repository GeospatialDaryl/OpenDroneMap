import os
import subprocess
from modObjSfMGenerics import *

class SfMPhoto:
    """   SfMPhoto - a class for SfMPhotos
    """

    def __init__(self, inputJPG, objSfMJob):
        #general purpose
        verbose = False
        # object attributes
        self.dictStepVals           = {}
        self.pathToContainingFolder = os.path.split(inputJPG)[0]
        self.strFileName            = os.path.split(inputJPG)[1]
        self.strFileNameBase        = os.path.splitext(self.strFileName)[0]
        self.strFileNameExt         = os.path.splitext(self.strFileName)[1]
              
        
        #unpack objSfMConfig
        objSfMConfig = objSfMJob.objSfMConfig
        
        #start pipe for jhead
        cmdSrc = objSfMConfig.BIN_PATH + os.sep + objSfMConfig.dictOSBins['exeJhead'] + " " + objSfMConfig.CURRENT_DIR + os.sep + self.strFileName
        srcProcess = subprocess.Popen(cmdSrc, stdout=subprocess.PIPE)

        stdout, stderr = srcProcess.communicate()
        stringOutput = stdout.decode('ascii')

        #listOutput is the list of params to be processed
        listOutput_ori = stringOutput.splitlines()
        listOutput = remove_values_from_list(listOutput_ori,u"")

        intListCount = 0
        intNumCameraAtts = len(listOutput)

        flagDoneList = False

        if verbose:  print listOutput

        #register all values from the list of JHead Output
        for lines in listOutput:
            # check if we've read all atts
            intListCount += 1
            if intListCount == intNumCameraAtts: flagDoneList = True
            flagBogusValue = False

            #extract and proceed            
            firstColon = lines.find(":")
            tempKey =   lines[:firstColon].strip()
            tempVal = lines[firstColon+1:].strip()

            if verbose:   print tempKey,tempVal
            # all them values
            if tempKey == 'File name': self.fileName = tempVal
            elif tempKey == 'File size': self.fileSize= tempVal
            elif tempKey == 'File date': self.fileDate = tempVal
            elif tempKey == 'Camera make': self.cameraMake = tempVal
            elif tempKey == 'Camera model': self.cameraModel = tempVal
            elif tempKey == 'Date/Time': self.dateTime = tempVal
            elif tempKey == 'Resolution': self.resolution = tempVal
            elif tempKey == 'Flash used': self.flashUsed = tempVal
            elif tempKey == 'Focal length': self.focalLength = tempVal
            elif tempKey == 'CCD width': self.ccdWidth = tempVal
            elif tempKey == 'Exposure time': self.exposureTime = tempVal
            elif tempKey == 'Aperture': self.aperture = tempVal
            elif tempKey == 'Focus dist.': self.focusDist = tempVal
            elif tempKey == 'ISO equiv.': self.isoEquiv= tempVal
            elif tempKey == 'Whitebalance': self.whitebalance = tempVal
            elif tempKey == 'Metering Mode': self.meteringMode = tempVal
            elif tempKey == 'GPS Latitude': self.gpsLatitude = tempVal
            elif tempKey == 'GPS Longitude': self.gpsLongitude = tempVal
            elif tempKey == 'GPS Altitude': self.gpsAltitude = tempVal
            elif tempKey == 'JPEG Quality': self.jpgQuality = tempVal	
            else: 
                flagBogusValue = True
                print "    Found unknow attribute in photo exif "+tempKey
            
        #  better object attribute names; keep old for compatability
        #  shallow references point to same stack space
        self.fullPathAndName = self.fileName

        # attribute 'id' set to more specific of the maker or model
        try:
            if hasattr(self,"cameraMake"):
                self.make = self.cameraMake
                self.id = self.cameraMake + " " + self.cameraModel
        except:  pass


        try:
            if hasattr(self,"cameraModel"):
                self.model = self.cameraModel
                self.id = self.cameraMake + " " + self.cameraModel
        except:  pass

        # parse resolution field 
        try:
            match = re.search("([0-9]*) x ([0-9]*)",self.resolution)
            if match:
                self.width  = int(match.group(1).strip())
                self.height = int(match.group(2).strip())
        except:  pass

        #parse force-focal
        try:
            if not '--force-focal' in args:
                match = re.search(":[\ ]*([0-9\.]*)mm", self.focalLength)
                if match:
                    self.focal = float((match.group()[1:-2]).strip())
            else:
                self.focal = args['--force-focal']
        except: pass

        #parse force-ccd
        if 'ccd' in lines.lower():
            if not '--force-ccd' in args:
                try:
                    floats = extractFloat(self.ccdWidth)
                    self.ccd = floats[0]
                except:
                    try:
                        self.ccd = float(ccdWidths[self.id])
                    except: pass
            else:
                self.ccd = args['--force-ccd']

        try:                
            if hasattr(self,"id"):
                if verbose: print self.id
                self.ccd = float(objSfMConfig.dictCCDWidths[self.id])
        except:
            pass
        if verbose:  print intListCount

        #if flagDoneList:
        try:
            if self.width > self.height:
                self.focalpx = self.width * (self.focal / self.ccd)
            else:
                self.focalpx = self.height * (self.focal / self.ccd)

            self.isOk = True
            objSfMJob.good += 1
        
            print "     using " + self.fileName + "     dimensions: " + \
                  str(self.width) + "x" + str(self.height)\
                  + " | focal: " + str(self.focal) \
                  + "mm | ccd: " + str(self.ccd) + "mm"

        except:
            self.isOk = False
            objSfMJob.bad += 1

            try:
                print "\n    no CCD width or focal length found for "\
                      + self.fileName+ " - camera: \"" + self.id+ "\""
            except:
                print "\n    no CCD width or focal length found"

        #either way increment total count
            objSfMJob.count += 1

            #populate & update max/mins

            if hasattr(self,'ccdWidth'):
                if objSfMJob.minWidth == 0:
                    objSfMJob.minWidth = self.ccdWidth
                if objSfMJob.minHeight == 0:
                    objSfMJob.minHeight = self.height

                if objSfMJob.minWidth < self.width:
                    objSfMJob.minWidth = self.minWidth
                else:
                    objSfMJob.minWidth = self.width

                if objSfMJob.minHeight < self.height:
                    objSfMJob.minHeight = objSfMJob.minHeight
                else:
                    objSfMJob.minHeight = self.height

                if objSfMJob.maxWidth > self.width:
                    objSfMJob.maxWidth = objSfMJob.maxWidth
                else:
                    objSfMJob.maxWidth = self.width

                if objSfMJob.maxHeight > self.height:
                    objSfMJob.maxHeight = objSfMJob.maxHeight
                else:
                    objSfMJob.maxHeight = self.height

