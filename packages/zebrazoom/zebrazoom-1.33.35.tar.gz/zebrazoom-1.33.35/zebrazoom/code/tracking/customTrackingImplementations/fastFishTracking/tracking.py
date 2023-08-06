from zebrazoom.code.tracking.customTrackingImplementations.fastFishTracking.utilities import calculateAngle, distBetweenThetas
from zebrazoom.code.tracking.customTrackingImplementations.fastFishTracking.detectMovementWithTrackedDataAfterTracking import detectMovementWithTrackedDataAfterTracking
from zebrazoom.code.tracking.customTrackingImplementations.fastFishTracking.detectMovementWithRawVideoInsideTracking import detectMovementWithRawVideoInsideTracking
from zebrazoom.code.tracking.customTrackingImplementations.fastFishTracking.getListOfWellsOnWhichToRunTheTracking import getListOfWellsOnWhichToRunTheTracking
from zebrazoom.code.tracking.customTrackingImplementations.fastFishTracking.backgroundSubtractionOnWholeImage import backgroundSubtractionOnWholeImage
from zebrazoom.code.tracking.customTrackingImplementations.fastFishTracking.backgroundSubtractionOnlyOnROIs import backgroundSubtractionOnlyOnROIs
import zebrazoom.videoFormatConversion.zzVideoReading as zzVideoReading
from zebrazoom.code.extractParameters import extractParameters
import zebrazoom.code.util as util
import zebrazoom.code.tracking
import numpy as np
import queue
import math
import time
import cv2

class Tracking(zebrazoom.code.tracking.BaseTrackingMethod):
  
  def __init__(self, videoPath, wellPositions, hyperparameters):
    self._videoPath = videoPath
    self._wellPositions = wellPositions
    self._hyperparameters = hyperparameters
    self._auDessusPerAnimalIdList = None
    self._firstFrame = self._hyperparameters["firstFrame"]
    self._lastFrame = self._hyperparameters["lastFrame"]
    self._nbTailPoints = self._hyperparameters["nbTailPoints"]
    self._previousFrames = None
    self._trackingDataPerWell = [np.zeros((self._hyperparameters["nbAnimalsPerWell"], self._lastFrame-self._firstFrame+1, self._nbTailPoints, 2)) for _ in range(len(self._wellPositions))]
    self._lastFirstTheta = np.zeros(len(self._wellPositions))
    self._lastFirstTheta[:] = -99999
    self._listOfWellsOnWhichToRunTheTracking = [i for i in range(0, len(self._wellPositions))]
    self._times2 = np.zeros((self._lastFrame - self._firstFrame + 1, 5))
    self._printInterTime = False


  def run(self):
    
    ### Step 1 (out of 2): Tracking:
    
    # Getting video reader
    cap = zzVideoReading.VideoCapture(self._videoPath)
    if (cap.isOpened()== False):
      print("Error opening video stream or file")
    
    # Simple background extraction with first and last frame of the video + Getting list of wells on which to run the tracking
    if self._firstFrame != 1:
      cap.set(cv2.CAP_PROP_POS_FRAMES, self._firstFrame - 1)
    ret, self._background = cap.read()
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1)
    ret, frame = cap.read()
    if self._hyperparameters["chooseWellsToRunTrackingOnWithFirstAndLastFrame"]:
      self._listOfWellsOnWhichToRunTheTracking = getListOfWellsOnWhichToRunTheTracking(self, self._background[:,:,0], frame[:,:,0])
    print("listOfWellsOnWhichToRunTheTracking:", self._listOfWellsOnWhichToRunTheTracking)
    self._background = cv2.max(frame, self._background) # INCONSISTENT!!! should be changed!
    self._background = cv2.cvtColor(self._background, cv2.COLOR_BGR2GRAY) # INCONSISTENT!!! should be changed!
    cap.set(cv2.CAP_PROP_POS_FRAMES, self._firstFrame - 1)
    
    # Initializing variables
    times  = np.zeros((int(cap.get(cv2.CAP_PROP_FRAME_COUNT) + 1), 2))
    ret = True
    
    # Going through each frame of the video
    startTime = time.time()
    k = self._firstFrame - 1
    while (ret and k <= self._lastFrame):
      time1 = time.time()
      ret, frame = cap.read()
      time2 = time.time()
      if ret:
        if self._hyperparameters["backgroundSubtractionOnWholeImage"] or k == self._firstFrame - 1:
          backgroundSubtractionOnWholeImage(self, frame, k)
        else:
          backgroundSubtractionOnlyOnROIs(self, frame, k)
      
      time3 = time.time()
      times[k, 0] = time2 - time1
      times[k, 1] = time3 - time2
      k += 1
    
    ### IS THIS BELLOW REALLY NECESSARY? AND IF SO WHY?
    for wellNumber in range(len(self._wellPositions)):
      for numAnimal in range(self._hyperparameters["nbAnimalsPerWell"]):
        self._trackingDataPerWell[wellNumber][numAnimal][0:self._lastFrame-2] = self._trackingDataPerWell[wellNumber][numAnimal][1:self._lastFrame-1]
    
    endTime = time.time()
    
    cap.release()
    
    print("")
    print("Color to grey:"           , np.median(self._times2[:,0]))
    print("Bout detection:"          , np.median(self._times2[:,1]))
    print("Background substraction:" , np.median(self._times2[:,2]))
    print("Gaussian blur:"           , np.median(self._times2[:,3]))
    print("Tracking on each well:"   , np.median(self._times2[:,4]))
    
    loadingImagesTime       = np.median(times[:,0])
    processingImagesTime    = np.median(times[:,1])
    percentTimeSpentLoading = loadingImagesTime / (loadingImagesTime + processingImagesTime)
    print("Median time spent on: Loading images:", loadingImagesTime, "; Processing images:", processingImagesTime)
    print("Percentage of time spent loading images:", percentTimeSpentLoading*100)
    print("Total tracking Time:", endTime - startTime)
    print("Tracking Time (without loading image):", (endTime - startTime) * (1 - percentTimeSpentLoading))
    print("Total tracking fps:", k / (endTime - startTime))
    print("Tracking fps (without loading image):", k / ((endTime - startTime) * (1 - percentTimeSpentLoading)))
    print("")
    
    ### Step 2 (out of 2): Extracting bout of movements:
    
    if self._hyperparameters["detectMovementWithRawVideoInsideTracking"] and self._hyperparameters["thresForDetectMovementWithRawVideo"]:
    
      trackingHeadingAllAnimalsList = [[[((calculateAngle(self._trackingDataPerWell[wellNumber][animalNumber][i][0][0], self._trackingDataPerWell[wellNumber][animalNumber][i][0][1], self._trackingDataPerWell[wellNumber][animalNumber][i][1][0], self._trackingDataPerWell[wellNumber][animalNumber][i][1][1]) + math.pi) % (2 * math.pi) if len(self._trackingDataPerWell[wellNumber][0][i]) > 1 else 0) for i in range(0, self._lastFrame)] for animalNumber in range(0, self._hyperparameters["nbAnimalsPerWell"])] for wellNumber in range(0, len(self._wellPositions))]
      
      return {wellNumber: extractParameters([self._trackingDataPerWell[wellNumber], trackingHeadingAllAnimalsList[wellNumber], [], 0, 0, self._auDessusPerAnimalIdList[wellNumber]], wellNumber, self._hyperparameters, self._videoPath, self._wellPositions, self._background) for wellNumber in range(0, len(self._wellPositions))}
    
    else:
      
      outputData = detectMovementWithTrackedDataAfterTracking(self)
      
      return outputData


zebrazoom.code.tracking.register_tracking_method('fastFishTracking.tracking', Tracking)
