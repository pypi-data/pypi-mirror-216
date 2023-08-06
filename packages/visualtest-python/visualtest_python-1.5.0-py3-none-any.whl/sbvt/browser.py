import os
import time
import shutil
import math
import logging
import json
from sys import getsizeof
from .imagetools import ImageTools
from .timer import StopWatch
from .api import Api
from selenium.webdriver.common.by import By

log = logging.getLogger(f'vt.{os.path.basename(__file__)}')

# defaults - can be overridden with limits parameter
DEFAULT_MAX_IMAGE_SIZE_MB = 20  # 20MB
DEFAULT_MAX_TIME_MIN = 3.5  # minutes (really for mobiles)

class Browser:
    """
    Class for wrapping selenium driver and controlling the remote browser in order to generate screenshots.
    Used by VisualTest class and should not be instantiated directly. 

    Args:
        driver: selenium webdriver with active session
        limits: Dictionary of values to change default limits for during creation fullpage images (not recommended)
            - MAX_IMAGE_PIXELS (int): Max fullpage image size. (default INT32 or 2^31)
            - MAX_TIME_MIN (float): Max time to create fullpage image.  Default is 3.5 minutes. Can be set to a max of 10 minutes. 
    Returns:
        Class instance
    """

    def __init__(self, driver, limits: dict = {}):

        # setup api
        self._userAgentScript = Api.getToolkit('user-agent')
        self._domCaptureScript = Api.getToolkit('dom-capture')
        self._freezePageScript = Api.getToolkit('freeze-page')
        self._chromeOsVersion = Api.getToolkit('chrome-os-version')
        self._detectChromeHeadless = Api.getToolkit('detect-chrome-headless')
        self._api = Api()
        log.info(f'Capabilities from driver: {driver.capabilities}')
        self._driver = driver
        self._userAgentInfo = self.getNavigatorUserAgentData(self._driver)
        self._deviceInfo = self._api.getDeviceInfo(self._userAgentInfo, driver.capabilities)
        log.info(f'Final device info: {self._deviceInfo}')

        # check browser running in headless mode or not after getting user-agent script
        self._headless = self.detectHeadlessMode(driver)

        log.info(f'limits: {limits}')
        if 'MAX_IMAGE_PIXELS' in limits:
            ImageTools.setMaxImagePixels(limits['MAX_IMAGE_PIXELS'])

        if 'MAX_TIME_MIN' in limits:
            self.MAX_TIME_MIN = limits['MAX_TIME_MIN']
        else:
            self._MAX_TIME_MIN = DEFAULT_MAX_TIME_MIN

        # default options
        self._scrollMethod = 'CSS_TRANSLATE'
        self._debug = False
        self._debugDir = None

    @property
    def scrollMethod(self):
        return self._scrollMethod

    @scrollMethod.setter
    def scrollMethod(self, s):
        scroll_options = ['CSS_TRANSLATE', 'JS_SCROLL']
        if s in scroll_options:
            self._scrollMethod = s
        else:
            raise Exception(f'Invalid scrollMethod: "{s}". Options are {str(scroll_options)}')

    @property
    def capabilities(self):
        return self._driver.capabilities

    @property
    def debugDir(self):
        return self._debugDir

    @debugDir.setter
    def debugDir(self, debugDir):
        
        if type(debugDir) == str or debugDir == None:
            self._debugDir = debugDir
        else:
            raise Exception(f'Argument must be a string!')

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, debug):
        if type(debug) == bool:
            self._debug = debug
        else:
            raise Exception(f'Argument must be a boolean!')

    @property
    def MAX_TIME_MIN(self):
        return self._MAX_TIME_MIN

    @MAX_TIME_MIN.setter
    def MAX_TIME_MIN(self, minutes):
        if type(minutes) != int:
            raise Exception(f'MAX_TIME_MIN must be an integer')
        if minutes not in range(0, 11):
            raise Exception(f'MAX_TIME_MIN must be between 0 and 10 minutes')
        self._MAX_TIME_MIN = minutes

    def getNavigatorUserAgentData(self, driver):
        """ Using a custom predefined script, get info from browser's navigator.userAgent """
        agent = driver.execute_script(f'return {self._userAgentScript};')
        log.info(f'Browser info interpreted from navigator.userAgent: {agent}')
        if 'browserName' in agent and agent['browserName'] in ['chrome','edge','opera','samsunginternet']:
            log.info(f'getting osVersion for chrome-based browser')
            osVersion = driver.execute_async_script(self._chromeOsVersion)
            if osVersion:
                agent['osVersion'] = osVersion
            log.info(f'osVersion for chrome-based browser: {agent["osVersion"]}')

        return agent

    def detectHeadlessMode(self, driver):
        headless = None
        agent = self._userAgentInfo
        if 'browserName' in agent and agent['browserName'] in ['chrome', 'edge', 'opera', 'samsunginternet']:
            headless = driver.execute_script(f'return {self._detectChromeHeadless};')
            log.info(f'headless flag for chrome-based browser: {headless}')
        if driver.capabilities['browserName'] == 'firefox' and driver.capabilities['moz:headless']:
            headless = driver.capabilities['moz:headless']
            log.info(f'headless flag for firefox browser: {headless}')
        return headless

    def captureDom(self, driver, type=""):
        """ Using a custom predefined script, capture the webpage's DOM element information """
        domString = driver.execute_script(f'return {self._domCaptureScript};')

        # add screenshot type and dump back to JSON string
        dom = json.loads(domString)
        dom['screenshotType'] = type
        domString = json.dumps(dom)
        # log.debug(f'Dom-capture: {dom}')

        return dom

    def _findElement(self, cssSelector):
        return self._driver.find_element(By.CSS_SELECTOR, cssSelector)

    def _clearIgnoreElements(self):
        script = 'delete window.sbvt'
        self._driver.execute_script(script)

    def _injectIgnoreElements(self, ignoreElements):
        script = 'window.sbvt = { ignoreElements: %s }' % json.dumps(ignoreElements)
        self._driver.execute_script(script)

    def _freezePage(self):
        return self._driver.execute_script(f'return {self._freezePageScript};')

    def _getPageDimensions(self):
        script = """
            return JSON.stringify({
                "document": {
                    "height": document.documentElement.clientHeight,
                    "width": document.documentElement.clientWidth
                },
                "body": {
                    "height": document.body.clientHeight,
                    "width": document.body.clientWidth
                },
                "windowInner": {
                    "height": window.innerHeight,
                    "width":  window.innerWidth
                },
                "fullpage": {
                    "height": Math.max(window.document.body.offsetHeight,window.document.body.scrollHeight, window.document.documentElement.offsetHeight, window.document.documentElement.scrollHeight),
                    "width": Math.max(window.document.body.offsetWidth, window.document.documentElement.offsetWidth)
                },
                "devicePixelRatio": window.devicePixelRatio,
                "initialScroll": {
                    x: window.scrollX, 
                    y: window.scrollY
                }
            })
        """

        jsonDimensions = self._driver.execute_script(script)
        log.info(f'Webpage Dimensions: {jsonDimensions}')
        dimensions = json.loads(jsonDimensions)

        # for now, take the window.inner dimensions as viewport
        # there may be cases where we need the documentElement or body on older browsers
        self.viewportHeight = dimensions['windowInner']['height']
        self.viewportWidth = dimensions['windowInner']['width']
        self.fullpageHeight = dimensions['fullpage']['height']
        self.fullpageWidth = dimensions['fullpage']['width']
        self.devicePixelRatio = dimensions['devicePixelRatio']
        log.info(f'devicePixelRatio: {self.devicePixelRatio}')
        # validate the viewport from javascript matches 
        # what we actually get from a png
        imageBinary = self._driver.get_screenshot_as_png()
        testImageWidth, testImageHeight = ImageTools.getImageSize(imageBinary)
        log.info(f'Size Test: image dimensions: {testImageWidth}x{testImageHeight}')

        self._cropEachBottom = None
        self._cropEachTop = None

        expectedWidth = math.ceil(self.viewportWidth * self.devicePixelRatio)
        expectedHeight = math.ceil(self.viewportHeight * self.devicePixelRatio)

        # have to allow 1px difference for devicePixelRatio that has a fraction
        isExpectedWidth = expectedWidth - 1 <= testImageWidth <= expectedWidth + 1
        isExpectedHeight = expectedHeight - 1 <= testImageHeight <= expectedHeight + 1

        if (isExpectedWidth and isExpectedHeight):
            log.info(f'Size Test: image dimensions are exactly {self.devicePixelRatio}x the javascript viewport size')
        else:
            if (isExpectedWidth and not isExpectedHeight):
                log.info(f'Size Test: Image matches expected width but not height')
            else:
                log.info(f'Size Test: Neither height nor width matches between size-test image and javascript values')

            if self._deviceInfo['osName'] == 'android':
                # androids have extra white space at bottom of each screen capture
                self._cropEachBottom = testImageHeight - expectedHeight
                log.info(
                    f'Size Test: Android device has {self._cropEachBottom}px extra pixels to crop on each image at the bottom')
            elif self._deviceInfo['osName'] == 'ios':
                # iOSs have toolbars at top of each screen capture for iPads
                # but both on iPhones in portrait (mixed on landscape)
                # we cannot tell how much extra is top or bottom
                self._cropEachTop = testImageHeight - expectedHeight
                log.info(
                    f'Size Test: iOS device has {self._cropEachTop}px extra pixels to crop on each image (top and/or bottom)')
            else:
                raise Exception(f'Size Test: Unknown platform to handle when javascript values do not match image size')

    def _getInitialPageState(self):

        script = """
            return JSON.stringify({
                "scrollX": window.scrollX, 
                "scrollY": window.scrollY,
                "overflow": document.body.style.overflow,
                "transform": document.body.style.transform
            })
        """

        pageState = self._driver.execute_script(script)
        log.info(f'Webpage initial state: {pageState}')
        self.initialPageState = json.loads(pageState)

    def _getNumberOfPagesToScroll(self):

        # how many viewports do we have to scroll within the fullpage
        totalPages = math.ceil(self.fullpageHeight / self.viewportHeight)

        """ 
        LIMITING NUM OF PAGES SCROLLED
            The number of viewport heights (pages) we will scroll should
            be less than the MAX_IMAGE_PIXELS based on viewportWidth * viewportHeight
            Example: 
                vw = 1366 //viewport width
                vh = 683  //viewport height
                How many pages (viewport heights) can we scroll to be 
                less than or equal to MAX_IMAGE_PIXELS?

                pages = max / (vw * vh * ratio)
                pages = 5000 * 15000 / 1366 * 683 * 2 ~= 40
            But this won't matter as we'll test image file size as we go
        """
        log.debug(f'MAX_IMAGE_PIXELS: {ImageTools.getMaxImagePixels()}')
        maxPages = math.floor(
            ImageTools.getMaxImagePixels() / (self.viewportWidth * self.viewportHeight * self.devicePixelRatio))
        log.debug(f'maxPages based on MAX_IMAGE_PIXELS / (vw * vh * ratio): {maxPages}')

        if totalPages > maxPages:
            log.info('Total Pages was greater than max, so decreasing amount of possible screenshots')
            totalPages = maxPages

        return totalPages

    def _getScrollOffset(self):
        return self._driver.execute_script(
            'if (window.pageYOffset) return window.pageYOffset;else if (window.document.documentElement.scrollTop)'
            'return window.document.documentElement.scrollTop;else return window.document.body.scrollTop;')

    def _checkScrollingLimits(self, pageIndex, totalPages):

        # tuple for (hitLimit, reason)
        result = (False, None)

        # check time running so far
        elapsedTimeSecs = self.fullpageStopWatch.timeElapsed()
        elapsedTimeDisplay = f'{elapsedTimeSecs}s' if elapsedTimeSecs <= 120 else f'{round(elapsedTimeSecs / 60, 3)}m'
        log.debug(f'Fullpage elapsed time: {elapsedTimeDisplay}')
        # if we are on the last page or we didn't scroll, set done to true
        if pageIndex == totalPages - 1:
            log.info(f'STOPPING scroll and capture because on last of totalPages')
            result = (True, 'HIT_BOTTOM')
        elif self.approxDiskSize > DEFAULT_MAX_IMAGE_SIZE_MB * 1000 * 1000:
            log.info(f'STOPPING scroll and capture because image size is >= {DEFAULT_MAX_IMAGE_SIZE_MB}MB')
            result = (True, 'MAX_IMAGE_SIZE')
        elif elapsedTimeSecs / 60 > self._MAX_TIME_MIN:
            # if we are running out of time, set done to true
            log.info(f'STOPPING scroll and capture because exceeded MAX_TIMEOUT: {self._MAX_TIME_MIN} minutes')
            result = (True, 'MAX_TIME_LIMIT')
        elif self._scrollMethod == 'JS_SCROLL':
            # if we didn't scroll the full viewport (stopped early like when page is shorter than expected on mobiles)
            expectedScrollOffset = self.viewportHeight * pageIndex
            currentScrollOffset = math.ceil(self._getScrollOffset())  # ceil for mobiles that return decimal value
            if currentScrollOffset < expectedScrollOffset:
                log.info(f'STOPPING scroll and capture because we hit the bottom of the page sooner than expected')
                result = (True, 'HIT_BOTTOM')

        return result

    def _scrollPage(self, pageIndex):

        pixels = self.viewportHeight * pageIndex

        if self._scrollMethod == 'CSS_TRANSLATE':
            # transform page by -100vh for each page number
            # script = f'document.body.style.transform="translateY(-{100 * pageIndex}vh)"'
            script = f'document.body.style.transform="translateY(-{pixels}px)"'
            log.info(f'Scrolling with CSS_TRANSLATE: {script}')
            self._driver.execute_script(script)
            return True
        elif self._scrollMethod == 'JS_SCROLL':

            # to ensure we scrolled, check scroll offset before and after
            lastScrollOffset = self._getScrollOffset()

            # scroll by viewport height times page number
            script = f'window.scroll(0,{pixels})'
            self._driver.execute_script(script)
            log.info(f'Scrolling with JS_SCROLL: {script}')

            currentScrollOffset = self._getScrollOffset()
            log.info(f'Scroll offset before: {lastScrollOffset}, scroll offset after: {currentScrollOffset}')

            # if scroll offset is same as last scroll offset, 
            # we are waiting on the browser to finish the scroll task
            # or we have reached the bottom earlier than expected
            if lastScrollOffset == currentScrollOffset:
                log.info(
                    f'Last y offset same as current, waiting a few seconds to give browser time to scroll and testing offset again')
                time.sleep(4)  # wait a few seconds and test again
                currentScrollOffset = self._getScrollOffset()
                log.info(f'Scroll offset before: {lastScrollOffset}, scroll offset after: {currentScrollOffset}')
                if lastScrollOffset == currentScrollOffset:
                    log.info(
                        f'Last y offset same as current even after waiting a few seconds, done with screen captures')

            return lastScrollOffset < currentScrollOffset
        else:
            raise Exception(f'Invalid scroll method: {self._scrollMethod}')

    def _loadLazyContent(self, totalPages, waitTimeMs):
        log.info(f'Loading lazy content by scrolling entire page with wait time of: {waitTimeMs}ms')
        currentPage = 1
        while (currentPage <= totalPages):
            pixels = self.viewportHeight * currentPage
            script = f'window.scroll(0,{pixels})'
            self._driver.execute_script(script)
            log.info(f'Scrolling with JS_SCROLL: {script}')
            time.sleep(waitTimeMs / 1000)
            currentPage += 1
        
        self._driver.execute_script('window.scrollTo(0,0)')
        time.sleep(waitTimeMs / 1000)
        
    def _fullpageHeightChanged(self):

        changed = False
        # check if page has grown for lazy-loading or infinite scroll
        script = 'return Math.max(window.document.body.offsetHeight,window.document.body.scrollHeight, window.document.documentElement.offsetHeight, window.document.documentElement.scrollHeight)'
        newFullpageHeight = self._driver.execute_script(script)
        if newFullpageHeight != self.fullpageHeight:
            term = 'grew' if newFullpageHeight > self.fullpageHeight else 'shrank'
            log.info(f'Fullpage height {term}, was {self.fullpageHeight}, now is {newFullpageHeight}')
            self.fullpageHeight = newFullpageHeight
            changed = True

        return changed

    def takeFullpageScreenshot(self, name, options):
        """
        Will take a fullpage screenshot and place the image at the path provided. \n
        Note this places a temporary folder at the current directory with the name sbTemp-{time}
        Args:
            path (str): the directory for where to save the image
            lazyload (int): if set, will scroll the page to load any content first and wait the number of milliseconds provided between each scroll
        """
        imageBinary = bytearray()  # New empty byte array

        if self._deviceInfo['osName'] == 'ios':
            raise Exception('iOS devices do no currently support fullpage screenshots.')

        log.info(f'Taking full page for image name "{name}" screenshot at URL: {self._driver.current_url}')

        # limit how long we let a screenshot run
        self.fullpageStopWatch = StopWatch()
        self.fullpageStopWatch.start()

        # create images directory for debug
        debugImageDir = None
        debugImageName = None
        debugImagePath = None
        if self._debug and self._debugDir:
            debugImageDir = os.path.join(self._debugDir, f'{name}-fullpage')
            os.makedirs(debugImageDir)

        # get initial page state for returning to later (must do before hiding scrollbar)
        self._getInitialPageState()

        # hide scroll bar for accurate dimensions
        hideScrollBarResult = self._driver.execute_script('return document.body.style.overflow="hidden";')
        log.info(f'PREP: Hide scrollbar result: {hideScrollBarResult}')

        # update the dimensions of the browser window and webpage
        self._getPageDimensions()

        # how many viewports fit into the fullpage 
        totalPages = self._getNumberOfPagesToScroll()
        log.info(f'Total pages to scroll: {totalPages}')

        reasonStopped = None

        # handle single page as special case
        if totalPages == 1:
            # take the selenium screenshot as final fullpage
            log.info(f'Taking single screenshot for single page')

            pageStopWatch = StopWatch()
            pageStopWatch.start()
            totalPageTime = 0

            # freezePage script
            freezePageResult = None
            if 'freezePage' in options:
                if options['freezePage']:
                    freezePageResult = self._freezePage()
            else:
                freezePageResult = self._freezePage()

            imageBinary = self._driver.get_screenshot_as_png()

            if self._debug:
                debugImageName = '0.png'
                debugImagePath = os.path.join(debugImageDir, debugImageName)
                with open(debugImagePath, 'wb') as outfile:
                    outfile.write(imageBinary)
                    outfile.close()

            if self._cropEachBottom:
                imageBinary = ImageTools.cropBottom(imageBinary, self._cropEachBottom, debugImagePath)
                
            if self._cropEachTop:
                imageBinary = ImageTools.cropTop(imageBinary, self._cropEachTop, debugImagePath)

            reasonStopped = 'IS_SINGLE_PAGE'

            # capture dom AFTER creating screenshot but BEFORE displaying scrollbar again (else get vertical offset on dom elements to image)
            self.dom = self.captureDom(self._driver, 'fullpage')

            log.info(f'Setting document.body.style.overflow back to initial state: {self.initialPageState["overflow"]}')
            self._driver.execute_script(f'document.body.style.overflow="{self.initialPageState["overflow"]}"')

            pageTime = pageStopWatch.stop()
            averagePageTime = round(pageTime, 2)

        else:

            # scroll browser back to initial position
            log.info(f'PREP: Scrolling to top of page')
            self._driver.execute_script('window.scrollTo(0,0)')

            # handle lazy-loaded content if setting provided
            if 'lazyload' in options:
                if options['lazyload'] is not None:
                    self._loadLazyContent(totalPages, options['lazyload'])

            # freezePage script
            freezePageResult = None
            if 'freezePage' in options:
                if options['freezePage']:
                    freezePageResult = self._freezePage()
            else:
                freezePageResult = self._freezePage()

            # to hide bottom fixed elements, this is a trick that works on most modern browsers
            log.info(f'PREP: Hiding bottom fixed elements: document.body.style.transform="translateY(0)"')
            self._driver.execute_script(f'document.body.style.transform="translateY(0)"')
            time.sleep(0.5) #some browsers need a little time to apply (Safari)

            done = False
            pageIndex = 0
            screenshots = []
            self.approxDiskSize = 0

            pageStopWatch = StopWatch()
            pageStopWatch.start()
            totalPageTime = 0

            # main loop for scroll and capture
            while not done:
                log.info(f'-- PAGE {pageIndex} --')
                scrolled = True

                # don't scroll for first pageIndex
                if pageIndex > 0:

                    # scroll and check scrolled correctly
                    scrolled = self._scrollPage(pageIndex)

                    # check if the page height changed
                    if self._scrollMethod == 'JS_SCROLL' and self._fullpageHeightChanged():
                        newTotalPages = self._getNumberOfPagesToScroll()
                        if newTotalPages > totalPages:
                            totalPages = newTotalPages
                            log.info(f'Total pages is now {totalPages}')
                            # if grew, scroll again to same position to ensure 
                            # handles infinite-scroll or lazy loaded content
                            self._scrollPage(pageIndex)

                # check if we should stop scrolling due to a limit
                hitLimit, reasonStopped = self._checkScrollingLimits(pageIndex, totalPages)

                # take the selenium screenshot
                if self._deviceInfo["browserName"].capitalize() == 'Safari':
                    screenshotElement = self._driver.find_element(By.TAG_NAME, 'body')
                    viewportImage = screenshotElement.screenshot_as_png
                else:
                    viewportImage = self._driver.get_screenshot_as_png()
                
                if self._debug:
                    debugImageName = f'{pageIndex}.png'
                    debugImagePath = os.path.join(debugImageDir, debugImageName)
                    with open(debugImagePath, 'wb') as outfile:
                        outfile.write(viewportImage)
                        outfile.close()

                if self._cropEachBottom:
                    viewportImage = ImageTools.cropBottom(viewportImage, self._cropEachBottom, debugImagePath)

                if self._cropEachTop:
                    viewportImage = ImageTools.cropTop(viewportImage, self._cropEachTop, debugImagePath)

                # crop image as necessary
                if self._scrollMethod == 'CSS_TRANSLATE':

                    """
                    When using translate, the last page will be shifted up past the true
                    bottom of the page. We need to crop off the extra "white" space that 
                    will be included in this last screenshot.

                    To calculate, get the remainder of "viewport" modulo "fullpage", which
                    is number of pixels we want to keep from the top. Subtract that from the 
                    viewport height to get the number of pixels to crop off at the bottom.

                    Multiply by devicePixelRatio to get the actual pixels for image crop.
                    """

                    cropHeight = self.viewportHeight - (self.fullpageHeight % self.viewportHeight)
                    numPixels = cropHeight * self.devicePixelRatio

                    if pageIndex == totalPages - 1 and numPixels > 0:
                        log.info(f'Cropping bottom of last image: {numPixels}px')
                        viewportImage = ImageTools.cropBottom(viewportImage, numPixels, debugImagePath)  # will reference cropped file

                elif self._scrollMethod == 'JS_SCROLL':

                    """
                    When using window.scrollTo(), the last page will not scroll a full
                    viewport and our last image will have content at the top that duplicates
                    content from previous screenshot. So, we need to crop the top of the image
                    to create a seamless stitch.

                    To calculate, subtract the scrolled offset from total viewports scrolled
                    and multiply by devicePixelRatio to get the actual pixels for image crop.
                    """
                    cropHeight = pageIndex * self.viewportHeight - self._getScrollOffset()
                    numPixels = cropHeight * self.devicePixelRatio
                    if hitLimit and reasonStopped == 'HIT_BOTTOM' and numPixels > 0:
                        log.info(f'Cropping top of last image: {numPixels}px')
                        viewportImage = ImageTools.cropTop(viewportImage, numPixels, debugImagePath)  # will reference cropped file

                screenshots.append(viewportImage)
                self.approxDiskSize += getsizeof(viewportImage)

                # we are done if we didn't actually scroll or hit a scrolling limit
                done = not scrolled or hitLimit
                pageTime = pageStopWatch.stop()
                totalPageTime += pageTime
                log.debug(f'Scroll and capture page time: {pageTime}s')

                # increment pageIndex
                pageIndex += 1

            averagePageTime = round(totalPageTime / pageIndex, 2)

            if self._scrollMethod == 'CSS_TRANSLATE':
                # put back to the top while capturing don
                self._driver.execute_script(f'document.body.style.transform="translateY(0)"')

            elif self._scrollMethod == 'JS_SCROLL':
                #scroll back to the top
                self._driver.execute_script('window.scrollTo(0,0)')
                time.sleep(0.75) # wait a half sec to allow dom to settle before capturing

            # capture dom AFTER creating screenshot but BEFORE setting back to initial states
            self.dom = self.captureDom(self._driver, 'fullpage')

            # Setting document.body.style.transform back
            log.info(f'Setting document.body.style.transform back to initial state: {self.initialPageState["transform"]}')
            self._driver.execute_script(f'document.body.style.transform="{self.initialPageState["transform"]}"')
            
            # Setting scroll position back
            log.info(f'Scrolling back to initial scroll offset ({self.initialPageState["scrollX"]},{self.initialPageState["scrollY"]})')
            self._driver.execute_script(
                f'window.scrollTo({self.initialPageState["scrollX"]},{self.initialPageState["scrollY"]})')
            
            # Showing scrollbar again by setting overflow back
            log.info(f'Setting document.body.style.overflow back to initial state: {self.initialPageState["overflow"]}')
            self._driver.execute_script(f'document.body.style.overflow="{self.initialPageState["overflow"]}"')

            # TODO: technically we could return control back to user here??

            # build the fullpage image from individual screenshots
            log.info(f'Stitching screenshots for final fullpage image')
            imageBinary = ImageTools.stitchImages(screenshots)
        

        # validate final fullpage image dimensions
        imageWidth, imageHeight = ImageTools.getImageSize(imageBinary)

        expectedImageWidth = self.fullpageWidth * self.devicePixelRatio
        expectedImageHeight = self.fullpageHeight * self.devicePixelRatio

        totalFullpageTime = self.fullpageStopWatch.stop()
        log.info(f'Total fullpage time duration: {totalFullpageTime} seconds')
        result = {
            'imagePath': None,
            'imageSize': {
                'width': imageWidth,
                'height': imageHeight
            },
            'expectedSize': {
                'width': expectedImageWidth,
                'height': expectedImageHeight
            },
            'devicePixelRatio': self.devicePixelRatio,
            'reasonStopped': reasonStopped,
            'duration': f'{totalFullpageTime} seconds',
            'averagePageTime': f'{averagePageTime} seconds',
            'url': self._driver.current_url,
            'freezePageResult': freezePageResult
        }

        log.info(f'Result: {result}')
        result['dom'] = self.dom #add dom after logging result
        result['imageBinary'] = imageBinary

        return result


    def takeElementScreenshot(self, options):
        """
        Will take an element screenshot and place the image at the path provided. \n
        Args:
            element (WebElement): The reference to the Selenium WebElement to capture a screenshot of
            path (str): the directory for where to save the image
        """
        # measure how long it takes
        self.watch = StopWatch()
        self.watch.start()

        imageBinary = bytearray()  # New empty byte array

        # freezePage script
        freezePageResult = None
        if 'freezePage' in options:
            if options['freezePage']:
                freezePageResult = self._freezePage()
        else:
            freezePageResult = self._freezePage()

        # update the dimensions of the browser window and webpage
        self._getPageDimensions()

        # selenium.webdriver.firefox.webelement.FirefoxWebElement
        log.debug(f'type of element is {type(options["element"])}')
        log.info(f'Taking element screenshot of element')
        imageBinary = options["element"].screenshot_as_png

        # capture dom AFTER creating screenshot
        self.dom = self.captureDom(self._driver, 'element')

        # validate final fullpage image dimensions
        imageWidth, imageHeight = ImageTools.getImageSize(imageBinary)

        totalTime = self.watch.stop()
        result = {
            'imagePath': None,
            'imageSize': {
                'width': imageWidth,
                'height': imageHeight
            },
            'duration': f'{totalTime} seconds',
            'url': self._driver.current_url,
            'freezePageResult': freezePageResult
        }

        log.info(f'Result: {result}')
        result['dom'] = self.dom #add dom after logging result
        result['imageBinary'] = imageBinary

        return result

    def takeViewportScreenshot(self, options):
        """
        Will take a screenshot of the browser viewport and place the image at the path provided. \n
        Args:
            path (str): the directory for where to save the image
        """
        log.info(f'Taking screenshot of viewport')

        # measure how long it takes
        self.watch = StopWatch()
        self.watch.start()

        imageBinary = bytearray()  # New empty byte array

        # freezePage script
        freezePageResult = None
        if 'freezePage' in options:
            if options['freezePage']:
                freezePageResult = self._freezePage()
        else:
            freezePageResult = self._freezePage()

        # get initial page state for returning to later (must do before hiding scrollbar)
        self._getInitialPageState()

        # hide scroll bar for accurate dimensions
        hideScrollBarResult = self._driver.execute_script('return document.body.style.overflow="hidden";')
        log.info(f'PREP: Hide scrollbar result: {hideScrollBarResult}')

        # update the dimensions of the browser window and webpage
        self._getPageDimensions()

        if self._deviceInfo["browserName"].capitalize() == 'Safari':
            screenshotElement = self._driver.find_element(By.TAG_NAME, 'body')
            imageBinary = screenshotElement.screenshot_as_png
        else:
            imageBinary = self._driver.get_screenshot_as_png()

        if self._cropEachBottom:
            imageBinary = ImageTools.cropBottom(imageBinary, self._cropEachBottom)

        if self._cropEachTop:
            imageBinary = ImageTools.cropTop(imageBinary, self._cropEachTop)

        # capture dom AFTER creating screenshot but BEFORE displaying scrollbar again (else get vertical offset on dom elements to image)
        self.dom = self.captureDom(self._driver, 'viewport')

        log.info(f'Setting document.body.style.overflow back to initial state: {self.initialPageState["overflow"]}')
        self._driver.execute_script(f'document.body.style.overflow="{self.initialPageState["overflow"]}"')

        # validate final fullpage image dimensions
        imageWidth, imageHeight = ImageTools.getImageSize(imageBinary)

        expectedImageWidth = self.viewportWidth * self.devicePixelRatio
        expectedImageHeight = self.viewportHeight * self.devicePixelRatio

        totalTime = self.watch.stop()
        log.info(f'Total viewport capture time duration: {totalTime} seconds')
        result = {
            'imagePath': None,
            'imageSize': {
                'width': imageWidth,
                'height': imageHeight
            },
            'expectedSize': {
                'width': expectedImageWidth,
                'height': expectedImageHeight
            },
            'devicePixelRatio': self.devicePixelRatio,
            'duration': f'{totalTime} seconds',
            'url': self._driver.current_url,
            'freezePageResult': freezePageResult
        }

        log.info(f'Result: {result}')
        result['dom'] = self.dom #add dom after logging result
        result['imageBinary'] = imageBinary
        return result


