import threading
import ctypes
import searchImage
import mouseHandle

class thread_with_exception(threading.Thread):
    def __init__(self,name,pictureDic):
        threading.Thread.__init__(self)
        self.picturesDic = pictureDic
        self.message =" "

    def run(self):
        while True:
            try:
                numImages = 0
                for pictureNames in self.picturesDic:
                    # Check for each photo
                    print("We're looking for: {}".format(pictureNames))
                    resultArray = searchImage.imageSearch(self.picturesDic[pictureNames])
                    # print Results
                    print(resultArray)
                    # if it found the photo then click location
                    if resultArray[0] is 'true':
                        print("image Found")
                        self.sendMessage("Looked for: {}".format(pictureNames))
                        self.sendMessage("image found percentage: {}".format(resultArray[3]))
                        self.sendMessage("Image Found!")
                        mouseHandle.clickPlace(resultArray[1], resultArray[2])
                        numImages += 1
                    else:
                        print("image not found nothing to do")
                        self.sendMessage("Looked for: {}".format(pictureNames))
                        self.sendMessage("image found percentage: {}".format(resultArray[3]))
                        self.sendMessage("image not found nothing to do")
            finally:
                print("Thread killed hopefully....")

    def get_id(self):
        if hasattr(self,'_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,0)
            print("Exception was raised")

    def sendMessage(self,message):
        self.message += message + "\n"

    def getMessage(self):
        sendmessage = self.message
        self.message =""
        return sendmessage




