import time, math, ctypes #importing standard libaries
import pyautogui, tkinter  #importing pyautogui for logging mouse position and tkinter for calculating the dpi (installed with pip install tk)
from threading import Thread #importing threading libary to enalbe multiple threads

class movlen:
    def __init__(self) -> None:
        self.x_nums = []
        self.y_nums = []
        self.fulllengh_nums = []
        self.pixelsize = 0
        self.cmx = 0
        self.cmy = 0    
        self.full_len = 0
   
    def get_screensize(self):
        #https://stackoverflow.com/questions/54271887/calculate-screen-dpi
        # gets screensize
        width, _ = pyautogui.size()

        # convertion from millimeters to inches
        MM_TO_IN = 0.0393700787
        # Set process DPI awareness
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        # Create a tkinter window
        root = tkinter.Tk()
        # Get a DC from the window's HWND
        dc = ctypes.windll.user32.GetDC(root.winfo_id())
        # The the monitor phyical width
        # (returned in millimeters then converted to inches)
        mw = ctypes.windll.gdi32.GetDeviceCaps(dc, 4) * MM_TO_IN
        # The the monitor phyical height
        mh = ctypes.windll.gdi32.GetDeviceCaps(dc, 6) * MM_TO_IN
        # Get the monitor horizontal resolution
        dw = ctypes.windll.gdi32.GetDeviceCaps(dc, 8)
        # Get the monitor vertical resolution
        dh = ctypes.windll.gdi32.GetDeviceCaps(dc, 10)
        # Destroy the window
        root.destroy()

        # Diagonal DPI calculated using Pythagoras
        ddpi = math.hypot(dw, dh) / math.hypot(mw, mh)

        # calculates the pixelsize based on the dpi
        self.pixelsize = ((width / ddpi) * 2.56) / width

    def logmousemov(self):
        lastposx = 0
        lastposy = 0
        while True:
            pos = pyautogui.position()
            if(pos.x != lastposx or pos.y != lastposy):
                #calclulates the diffrent between two yx numbers
                if lastposx == 0:
                    lastposx = pos.x
                #calclulates the diffrent between two y numbers
                if lastposy == 0:
                    lastposy = pos.y
                #saves the lengh moved to a array
                self.x_nums.append(pos.x - lastposx)                    
                self.y_nums.append(pos.y - lastposy)
                #saves the Diagonal of the x and y value to an array
                self.fulllengh_nums.append(math.sqrt((pos.x - lastposx)  * (pos.x - lastposx)  + (pos.y - lastposy) * (pos.y - lastposy)))
                #change last position of x and y
                lastposx = pos.x                
                lastposy = pos.y
            time.sleep(0.01)
            
    def cmd(self):
        while(True):
            i = input()
            if i == "mov":
                self.savedata()
                print(self.convert(self.full_len * self.pixelsize, "full lengh moved on screen:"))
                print(self.convert(self.cmx * self.pixelsize, "lengh moved on x Axes:"))
                print(self.convert(self.cmy * self.pixelsize, "lengh moved on y Axes:"))
            elif i == "screensize":
                print(self.getscreensize())
            elif i == "help":
                print("mov: calculates the distance you moved on your screen in cm")
                print("screensize: prints the physical screen size in cm")
            else:
                print(i, "is an unknown command")            

    def convert(self, val, parameter):
        #Converts cm in to m and km
        if val / 100000 >= 1:
            km = val / 100000
            val = val / 100000
            split = str(val).split(".")
            m = (val - int(split[0])) * 100
            val = (val - int(split[0])) * 100
            split = str(val).split(".")
            cm = (val - int(split[0])) * 100
            return(parameter +" %.0f km, " % km + " %.0f m, " % m + " %.2f cm" % cm)
        elif val / 100 >= 1:
            m = val / 100
            val = val / 100
            split = str(val).split(".")
            cm = (val - int(split[0])) * 100
            return(parameter + " %.0f m, " % m + "%.2f cm" % cm)
        else:
            return(parameter + " %.2f cm" % val)
    
    def savedata(self):
        #get the diff in pixel for x values
        for i in self.x_nums:
            if i > 0:
                pass
            elif i == 0:
                pass
            else: 
                i = i * -1
            self.cmx += i
        #gets the diff in pixel for y values
        for i in self.y_nums:
            if i > 0:
                pass
            elif i == 0:
                pass
            else: 
                i = i * -1
            self.cmy += i
        #gets the diff for fulllengh
        for i in self.fulllengh_nums:
            if i > 0:
                pass
            elif i == 0:
                pass
            else: 
                i = i * -1
            self.full_len += i
        self.x_nums.clear()
        self.y_nums.clear()
        self.fulllengh_nums.clear()

    def getscreensize(self):
        width, height= pyautogui.size()
        return ("width: %.2f cm" % (self.pixelsize * width)) + ("\nheight: %.2f cm" % (self.pixelsize * height))

    def autosave(self):
        while(True):
            self.savedata()
            time.sleep(300)
                
    def main(self):
        cmd_thread = Thread(target=self.cmd)
        cmd_thread.start()
        mouselog_thread = Thread(target=self.logmousemov)
        mouselog_thread.start()
        autosave_thread = Thread(target=self.autosave)
        autosave_thread.start()
        self.get_screensize()

if __name__ == "__main__":
    mov = movlen()
    mov.main()