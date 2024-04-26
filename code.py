import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer
import adafruit_fancyled.adafruit_fancyled as fancy
import adafruit_fancyled.fastled_helpers as helpers
import time
from math import floor, sqrt, fabs, pow, sin, exp, pi, ceil
import random

import digitalio

import adafruit_imageload
from displayio import Bitmap, Palette
import os

def readHexSelector(valList):

    x = 0
    for i, v in enumerate(valList):
        if v:
            x += 2**i

    strList = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

    return strList[x]


def hexSelectorReadPins(pinObjs):
    vOut = []

    for p in pinObjs:
       # print('{} for {}'.format(p.value, p))
        vOut.append(p.value)

    print('{} = vOut'.format(vOut))
    return vOut


fastRainbow = {
    "hexCode": "0",
    "timePerSparkle": 0.3,  # seconds
    "gradientSteps": 3,
    "nSparkles": 10,
    "brightness": 0.5,
    "panelCycle": 600,
    "mixRatio": 0.4,
    "mixColor": fancy.CRGB(1.0, 1.0, 1.0),
    "panelDisplayType": "rainbow",
    "sparkleBlendBend": "sinusoid",
    "imageFilePath": "",
    "initialColor": 0x000000,
    "allowedColors": [],
}

fastFadeRainbow = {
    "hexCode": "1",
    "timePerSparkle": 0.2,  # seconds
    "gradientSteps": 4,
    "nSparkles": 10,
    "brightness": 0.5,
    "panelCycle": 600,
    "mixRatio": 0.4,
    "mixColor": None,
    "panelDisplayType": "rainbow",
    "sparkleBlendBend": "sinusoid",
    "imageFilePath": "",
    "initialColor": 0x000000,
    "allowedColors": [],
}


percolatingRainbowHour = {
    "hexCode": "2",
    "timePerSparkle": 3,  # seconds
    "gradientSteps": 25,
    "nSparkles": 10,
    "brightness": 0.5,
    "panelCycle": 3600,
    "mixRatio": 0.2,
    "mixColor": fancy.CRGB(0.0, 0, 0),
    "panelDisplayType": "rainbow",
    "sparkleBlendBend": "linear",
    "imageFilePath": "/pics/test",
    "initialColor": 0x000000,
    "allowedColors": [],
}

brightPercRainbowHour = {
    "hexCode": "3",
    "timePerSparkle": 4,  # seconds
    "gradientSteps": 25,
    "nSparkles": 10,
    "brightness": 0.5,
    "panelCycle": 3600,
    "mixRatio": 0.2,
    "mixColor": fancy.CRGB(1.0, 1.0, 1.0),
    "panelDisplayType": "rainbow",
    "sparkleBlendBend": "sinusoid",
    "imageFilePath": "/pics/test",
    "initialColor": 0x000000,
    "allowedColors": [],
}

dummyHolder1 = {
    "hexCode": "4",
    "timePerSparkle": 1,  # seconds
    "gradientSteps": 10,
    "nSparkles": 10,
    "brightness": 0.5,
    "panelCycle": 3600,
    "mixRatio": 0.2,
    "mixColor": fancy.CRGB(1.0, 0.0, 1.0),
    "panelDisplayType": "images",
    "sparkleBlendBend": "sinusoid",
    "imageFilePath": "/pics/test",
    "initialColor": 0x000000,
    "allowedColors": [],
}

dummyHolder2 = {
    "hexCode": "5",
    "timePerSparkle": 1,  # seconds
    "gradientSteps": 10,
    "nSparkles": 10,
    "brightness": 0.5,
    "panelCycle": 3600,
    "mixRatio": 0.2,
    "mixColor": fancy.CRGB(1.0, 0.0, 1.0),
    "panelDisplayType": "images",
    "sparkleBlendBend": "sinusoid",
    "imageFilePath": "/pics/test",
    "initialColor": 0x000000,
    "allowedColors": [],
}

waterlillies = {
    "hexCode": "6",
    "timePerSparkle": 4,  # seconds
    "gradientSteps": 25,
    "nSparkles": 10,
    "brightness": 0.5,
    "panelCycle": 3600,
    "mixRatio": 0.2,
    "mixColor": fancy.CRGB(1.0, 1.0, 1.0),
    "panelDisplayType": "mondrian",
    "sparkleBlendBend": "sinusoid",
    "imageFilePath": "",
    "initialColor": 0x000000,
    "allowedColors": [0x345573, 0x6085A6, 0x4C6F73, 0x6F8C51, 0xF2DC6D],
}

starryNight = {
    "hexCode": "7",
    "timePerSparkle": 3,  # seconds
    "gradientSteps": 15,
    "nSparkles": 5,
    "brightness": 0.5,
    "panelCycle": 3600,
    "mixRatio": 0.9,
    "mixColor": fancy.CRGB(1.0, 1.0, 1.0),
    "panelDisplayType": "mondrian",
    "sparkleBlendBend": "sinusoid",
    "imageFilePath": "",
    "initialColor": 0x000000,
    "allowedColors": [0x000000, 0x1D5880, 0xAEAE00, 0x77FA66, 0x9F9F35, 0x1066A0],
}

mondrian = {
    "hexCode": "8",
    "timePerSparkle": 3,  # seconds
    "gradientSteps": 15,
    "nSparkles": 5,
    "brightness": 0.5,
    "panelCycle": 3600,
    "mixRatio": 0.9,
    "mixColor": fancy.CRGB(0.0, 0.0, 0.0),
    "panelDisplayType": "mondrian",
    "sparkleBlendBend": "sinusoid",
    "imageFilePath": "",
    "initialColor": 0xAAAAAA,
    "allowedColors": [
        0x000000,
        0xAA0000,
        0xAAAA00,
        0x0000BB,
        0xAAAAAA,
        0xAAAAAA,
        0xAAAAAA,
        0xAAAAAA,
    ],
}
# Excellent clock
rainbowSweep = {
    "hexCode": "9",
    "timePerSparkle": 0.1,  # seconds
    "gradientSteps": 3,
    "nSparkles": 20,
    "brightness": 0.9,
    "panelCycle": 3600,
    "mixRatio": 0.2,
    "mixColor": None,
    "panelDisplayType": "rainbow",
    "sparkleBlendBend": "linear",
    "imageFilePath": "/pics/test",
    "initialColor": 0x000000,
    "allowedColors": [],
}


imageAMinute = {
    "hexCode": "A",
    "timePerSparkle": 1,  # seconds
    "gradientSteps": 4,
    "nSparkles": 10,
    "brightness": 0.5,
    "panelCycle": 180,
    "mixRatio": 0.9,
    "mixColor": fancy.CRGB(1.0, 1.0, 1.0),
    "panelDisplayType": "images",
    "sparkleBlendBend": "sinusoid",
    "imageFilePath": "/pics/test",
    "initialColor": 0x000000,
    "allowedColors": [],
}

rapidGradients = {
    "hexCode": "B",
    "timePerSparkle": 0.8,  # seconds
    "gradientSteps": 4,
    "nSparkles": 10,
    "brightness": 0.5,
    "panelCycle": 3600,
    "mixRatio": 0.3,
    "mixColor": fancy.CRGB(1.0, 1.0, 1.0),
    "panelDisplayType": "images",
    "sparkleBlendBend": "sinusoid",
    "imageFilePath": "/pics/gradients",
    "initialColor": 0x000000,
    "allowedColors": [],
}

rothko = {
    "hexCode": "C",
    "timePerSparkle": 0.2,  # seconds
    "gradientSteps": 4,
    "nSparkles": 20,
    "brightness": 0.5,
    "panelCycle": 240,
    "mixRatio": 1.0,
    "mixColor": None,
    "panelDisplayType": "images",
    "sparkleBlendBend": "sinusoid",
    "imageFilePath": "/pics/rothko",
    "initialColor": 0x000000,
    "allowedColors": [],
}

fruits = {
    "hexCode": "D",
    "timePerSparkle": 0.2,  # seconds
    "gradientSteps": 4,
    "nSparkles": 10,
    "brightness": 0.5,
    "panelCycle": 240,
    "mixRatio": 1.0,
    "mixColor": None,
    "panelDisplayType": "images",
    "sparkleBlendBend": "sinusoid",
    "imageFilePath": "/pics/fruit",
    "initialColor": 0x000000,
    "allowedColors": [],
}

smash = {
    "hexCode": "E",
    "timePerSparkle": 0.2,  # seconds
    "gradientSteps": 3,
    "nSparkles": 40,
    "brightness": 0.5,
    "panelCycle": 240,
    "mixRatio": 1.0,
    "mixColor": None,
    "panelDisplayType": "images",
    "sparkleBlendBend": "sinusoid",
    "imageFilePath": "/pics/smash",
    "initialColor": 0x000000,
    "allowedColors": [],
}

dummyImages = {
    "hexCode": "F",
    "timePerSparkle": 0.2,  # seconds
    "gradientSteps": 3,
    "nSparkles": 40,
    "brightness": 0.5,
    "panelCycle": 240,
    "mixRatio": 1.0,
    "mixColor": None,
    "panelDisplayType": "images",
    "sparkleBlendBend": "sinusoid",
    "imageFilePath": "/pics/test",
    "initialColor": 0x000000,
    "allowedColors": [],
}

configList = [
    percolatingRainbowHour,
    brightPercRainbowHour,
    fastRainbow,
    imageAMinute,
    rapidGradients,
    waterlillies,
    dummyHolder1,
    dummyHolder2,
    fastFadeRainbow,
    mondrian,
    rothko,
    fruits,
    smash,
    starryNight,
    dummyImages,
    rainbowSweep,
]



pinList = [board.D10, board.D9, board.D7, board.D2]

pinObjs = []
for pL in pinList:

    pinHere = digitalio.DigitalInOut(pL)
    pinHere.direction = digitalio.Direction.INPUT
    pinHere.pull =  digitalio.Pull.UP
    pinObjs.append(pinHere)


hexCode = readHexSelector(hexSelectorReadPins(pinObjs))
pickConfig = [i for i in (configList) if i["hexCode"] == hexCode][0]


# Numeric parameters
timePerSparkle = pickConfig["timePerSparkle"]  # seconds
gradientSteps = pickConfig["gradientSteps"]
nSparkles = pickConfig["nSparkles"]
brightness = pickConfig["brightness"]
timePerPanel = pickConfig["panelCycle"]  # note variable basis change.
mixRatio = pickConfig["mixRatio"]

# mixColor = fancy.CRGB(1.0, 1.0, 1.0)
mixColor = pickConfig["mixColor"]
allowedColors = pickConfig["allowedColors"]
initialBackground = pickConfig["initialColor"]

# String parameters
imageFilePath = pickConfig["imageFilePath"]
panelDisplayType = pickConfig["panelDisplayType"]
sparkleBlendBend = pickConfig["sparkleBlendBend"]


# Constants
currentImageNum = 0
pixel_pin = board.D13
pixel_width = 8
pixel_height = 8


global lastImageLoaded
lastImageLoaded = ""


class percoloid(object):

    imgAll = []
    pltAll = []

    def __init__(
        self,
        pArray,
        correctionType=sparkleBlendBend,
        gSteps=gradientSteps,
        transitionColor=mixColor,
        cTime=timePerSparkle,
        pTime=timePerPanel,
        imageFiles=[],
        plType=panelDisplayType,
        initImg=[],
        initPlt=[],
    ):

        self.midColor = transitionColor
        self.nSteps = gSteps
        self.stepCode = correctionType
        self.cycleTime = cTime
        self.pixArray = pArray
        self.panelCycle = pTime
        self.birthTime = time.monotonic_ns() / 1e9
        self.imageFiles = imageFiles
        self.panelType = plType
        self.allowedColors = allowedColors
        self.resetFlag = False

        type(self).imgAll = initImg
        type(self).pltAll = initPlt

        self.reset()

    def reset(self):
        self.startTime = time.monotonic_ns() / 1e9
        self.correctedTic = 0
        self.correctedStep = 0
        self.ticDelay = random.random() * self.cycleTime
        self.X, self.Y, self.N = self.pickApixel()
        self.defineStartColor()
        self.supplyTargetColor()
        self.generateGradients()

    def defineStartColor(self, mode="match"):

        if mode == "match":
            # Start color is whatever is already there
            self.startColor = fancy.unpack(self.pixArray.pixel(self.X, self.Y))

        elif mode == "images":
            self.startColor = self.palette[self.image[self.X * pixel_width + self.Y]]

    def display(self):
        self.pixArray.pixel(self.X, self.Y, self.colorNow.pack())

    def loadNextImage(self, nextToLoad):

        global lastImageLoaded
        lastImageLoaded = nextToLoad

        imgPath = imageFilePath + "/" + nextToLoad

        # second output being 'self.palette' yields a yellow error
        i, p = adafruit_imageload.load(imgPath, bitmap=Bitmap, palette=Palette)
        self.setImage(i, p)  # this needs to be for all pixels!
        # self.pixArray.fill(0x000000)

    def supplyTargetColor(self):

        timeNow = (
            ((time.monotonic_ns() / 1e9) - self.birthTime + self.cycleTime)
            % self.panelCycle
        ) / self.panelCycle

        if self.panelType == "rainbow":
            colorTarget = fancy.CRGB(fancy.CHSV(timeNow, 1.0, brightness))
            colorNow = fancy.mix(self.startColor, colorTarget, mixRatio)
            # colorNow = fancy.CRGB(1.0, 0, 1.0)

        elif self.panelType == "images":

            # panelTime is float from 0 -> 1 with time through *entire* cycle of images
            panelTime = (
                ((time.monotonic_ns() / 1e9) - self.birthTime + self.cycleTime)
                % self.panelCycle
            ) / self.panelCycle

            panelNext = floor(panelTime * len(self.imageFiles))

            if panelNext >= len(self.imageFiles):
                panelNext = panelNext - 1
            elif panelNext < 0:
                panelNext == 0

            nextImageLoaded = self.imageFiles[panelNext]

            if lastImageLoaded == nextImageLoaded:
                # Nothing needed here but a pass
                pass

            else:
                # first time hitting this image. time to load.
                self.loadNextImage(nextImageLoaded)

            colorNext = type(self).pltAll[
                type(self).imgAll[self.X * pixel_width + self.Y]
            ]
            colorCorrect = helpers.applyGamma_video(fancy.unpack(colorNext), [1, 1, 2])


            colorNow = fancy.mix(self.startColor, colorCorrect, mixRatio)

        elif self.panelType == "mondrian":

            # colorNext = self.allowedColors
            colorNext = self.allowedColors[random.randrange(len(self.allowedColors))]
            colorCorrect = helpers.applyGamma_video(fancy.unpack(colorNext), [1, 1, 1.9])
            colorNow = fancy.mix(self.startColor, colorCorrect, mixRatio)

        else:
            colorNow = fancy.CRGB(0, 0.01, 1)

        self.endColor = colorNow

    def pulseWaveCorrect(self, pts, stepCode="sinusoid"):

        if stepCode == "circle":
            pwm_val = self.nSteps * sqrt(
                1.0 - pow((fabs(2.0 * (float(pts) / self.nGradSteps) - 1.0)), 2)
            )

        elif stepCode == "sinusoid":
            pwm_val = (self.nGradSteps) * 2*sin(float(pts))

        elif stepCode == "linear":
            pwm_val = (self.nGradSteps - 1) * (float(pts))

        elif stepCode == "expRamp":
            l = self.nGradSteps * exp(float(pts))

        elif stepCode == "burst":

            if pts > (self.nGradSteps / 2):
                pwm_val = 2
            else:
                pwm_val = 1

        else:
            pwm_val = -1

        return pwm_val

    def pickApixel(self):

        pN = random.randrange(pixel_width * pixel_height)
        pixX, pixY = self.indexToXY(pN)

        return pixX, pixY, pN


    def generateGradients(self):

        if self.midColor is None:
            transColor = fancy.mix(self.startColor, self.endColor, 0.5)
        else:
            transColor = self.midColor

        colorlist = []
        colorlist.append(self.startColor)
        for i in range(self.nSteps):
            colorlist.append(
                fancy.mix(self.startColor, transColor, float(i) / (self.nSteps))
            )

        colorlist.append(transColor)

        for i in range(self.nSteps):
            colorlist.append(
                fancy.mix(transColor, self.endColor, float(i) / (self.nSteps))
            )

        colorlist.append(self.endColor)

        self.gradient = colorlist
        self.nGradSteps = len(self.gradient)

    def stepNow(self):

        self.correctedTime = (
            (time.monotonic_ns() / 1e9) - self.ticDelay - self.startTime
        )/self.cycleTime

        self.correctedTime = float(int(self.correctedTime*self.nGradSteps))/self.nGradSteps
        self.correctedStep = int(self.pulseWaveCorrect(self.correctedTime))

        self.resetFlag = False

        #('{}, {}'.format(self.nGradSteps, self.correctedStep))

        if self.correctedStep >= self.nGradSteps:
            # End case
            #self.correctedStep = len(self.gradient)

            self.colorNow = self.endColor
            # self.display()
            # Reset
            self.resetFlag = True
            # self.reset()

        elif self.correctedStep < 0:
            # Delay
            self.correctedStep = 0
            self.colorNow = self.gradient[self.correctedStep]

        else:
            # Btw 0-1
            #print('{}, {}'.format(self.nGradSteps, self.endColor))
            self.colorNow = self.gradient[self.correctedStep]

    def indexToXY(self, indVal):
        pixX = floor(float(indVal) / pixel_width)
        pixY = indVal % pixel_height

        return pixX, pixY

    def applyBitmap(self, img, plt):

        for i in range(pixel_width * pixel_height):
            x, y = self.indexToXY(i)
            self.pixArray.pixel(x, y, plt[img[i]])

        self.setImage(img, plt)

    def setImage(self, img, plt):
        self.image = img
        self.palette = plt
        type(self).imgAll = img
        type(self).pltAll = plt

    def tic(self):
        self.stepNow()
        self.display()

        if self.resetFlag:
            self.reset()


# Set up LED board connection
pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height,
    brightness=0.05,
    auto_write=False,
)

# Set up frame buffer
pixel_framebuf = PixelFramebuffer(pixels, pixel_width, pixel_height, alternating=False)
pixel_framebuf.fill(initialBackground)
pixel_framebuf.display()


if panelDisplayType == "images":
    imgFiles = os.listdir(imageFilePath)

    imgPath = imageFilePath + "/" + imgFiles[currentImageNum]
    img, plt = adafruit_imageload.load(imgPath, bitmap=Bitmap, palette=Palette)
    addBitmaps = True

else:
    imgFiles = []
    img = []
    plt = []
    addBitmaps = False


percList = []
# Instantiate class
for i in range(nSparkles):
    percList.append(
        percoloid(pixel_framebuf, imageFiles=imgFiles, initImg=img, initPlt=plt)
    )



while True:



    for perc in percList:
        perc.tic()

    pixel_framebuf.display()
