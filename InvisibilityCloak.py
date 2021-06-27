#import libraries
import cv2
import numpy as np

from tkinter import*
from PIL import ImageTk, Image

"""Function to create bg image to replace with red cloak""" 

def makeBgImage():
    #Open front camera(0) and record feed
    cap = cv2.VideoCapture(0) 
    
    #Loop for the time camera is on
    while cap.isOpened():
        # Read data from current instance or frame
        ret, back = cap.read()
        #If frame read successfully, do the following
        if ret:
            #Show current frame and label as image.jpg
            cv2.imshow("image.jpg", back)
            #If q pressed in every 5 units of time 
            if cv2.waitKey(5) == ord('q'):
                #Save the current frame image as image.jpg
                cv2.imwrite('image.jpg', back)
                #Break the loop
                break
    
    #Release all space occupied by video and close the window
    cap.release()
    cv2.destroyAllWindows()

"""Function to replace red cloth's pixels with bg image"""

def makeInvisible():
    #Open front camera(0) and record feed 
    cap = cv2.VideoCapture(0)
    
    #Loop for the time camera is on    
    while cap.isOpened():
        # Read data from current instance or frame
        ret, frame = cap.read()
        #If frame read successfully, do the following
        
        if ret:
            #Convert BGR to HSV representaion of image as 
            #HSV is similar to how our eyes percieve colours
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                        
            #Defining lower range of red
            l_red = np.array([0, 120, 120])
            u_red = np.array([10, 255, 255])
            mask1 = cv2.inRange(hsv, l_red, u_red)
                       
            # Defining upper range for red color detection
            lower_red = np.array([170,120,70])
            upper_red = np.array([180,255,255])
            mask2 = cv2.inRange(hsv,lower_red,upper_red)
              	
        	# Addition of the two masks to generate the final mask.
            mask = mask1+mask2
            
            #Using morphology to only detect pixels that are largely grouped together
            #Inputs: image, morph type, kernel(a 0*0 kernel of 1's)            
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((0, 0), np.uint8))
            #Another morphology function which close small holes in object, dilation then erosion
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
                     	
            # Replacing pixels corresponding to cloak with the background pixels.
            frame[np.where(mask==255)] = back[np.where(mask==255)]
            cv2.imshow('Display',frame)
            
            #To come out of loop, press q
            if cv2.waitKey(5) == ord('q'):
                break
    
    #Release all space occupied by video and close the window
    cap.release()
    cv2.destroyAllWindows()
    
"""Function for initial UI window"""

def window():    
    root= Tk() 
    root.title('Invisibility Cloak')
    root.iconbitmap('./Hogwarts.ico') #add path to icon image
    root.configure(width=500, height=300) #Size of window
    hp_img=ImageTk.PhotoImage(Image.open("hp.png")) #change hp image
    
    m1 = PanedWindow()
    m1.pack(fill=BOTH, expand=1)
    
    m2 = PanedWindow(m1, orient=VERTICAL)
    m1.add(m2)
    
    txt="""WELCOME TO HARRY POTTER INVISIBILITY CLOAK!\n\nGet ready with a red cloth
    to make your cloak. Firstly, we will click a background image without you in it.
    For that, click the button below and wait for window to open. When it does, get
    out of the screen and press 'q' to take picture. Then another window will open
    which will record your live video and replace pixels of your cloth with your
    background image. To quit, again press 'q'.\n\nRead the above instructions then
    press the button."""
    
    top = Label(m2, text=txt)
    m2.add(top)
    
    bottom = Label(m2, image=hp_img, background='black')
    m2.add(bottom)
    
    btn = Button(root, text="Make me invisible",bg='#AF7AC5',command= root.destroy).pack()
    
    root.mainloop()

"""main code"""
window()
makeBgImage()
#Read the image file we just saved to be used in next function
back = cv2.imread('./image.jpg') 
makeInvisible()
