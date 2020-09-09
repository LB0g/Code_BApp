from guizero import * #Import all class from a module (here guizero)
#App, Text, PushButton, TextBox, Slider, Box, Combo, Window, info, Waffle 


from picamera import PiCamera
from time import sleep
camera = PiCamera()

import time
import datetime
day = datetime.datetime.now()

import os #Import code save in another file

import RPi.GPIO as GPIO #Import GPIO library
GPIO.setmode(GPIO.BOARD) #Set the numeration of the GPIO (Board)
GPIO.setwarnings(False)

#Attribute each electronic part to a GPIO (number)
LED1 = 11 #blue LED
LED2 = 29 #brightfield
LED3 = 22 #red

LED = LED1, LED2, LED3
GPIO.setup(LED, GPIO.OUT)

jaune = 7
GPIO.setup(jaune,GPIO.OUT)

#Control LED intensity with modulation of the voltage
pwm_blue = GPIO.PWM(LED1, 100) #when pwm = 100, the LED receive the maximal voltage, can play between 0 and 100
pwm_bf = GPIO.PWM(LED2, 100)
pwm_red = GPIO.PWM(LED3, 100)
pwm_blue.start(0) #start with pwm=0 and so the LED is off
pwm_bf.start(0)
pwm_red.start(0)

#Control of motors. Pins corresponding to each motor and the sequence of halfsteps in the rotor when the motor is activated.
Xcontrol_pins = [13,15,16,18]
Ycontrol_pins = [32,36,38,40]
Zcontrol_pins = [31,33,35,37]

halfstep_seq = [
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1]
        ]

# Values x y z /0
x2 = []
y2 = []
z2 = []
# Positions xy of fixed points /0
axy = []
bxy = []
cxy = []
dxy = []
# For experiments:
# [0,1] = positions xy depending on each other (a/0, b/a, c/b...).  [2,3] = z1,z2
A = []
B = []
C = []
D = []


        ######################################################################################################################################
##########################################################FONCTIONS SETUP#########################################################################################################################
        ######################################################################################################################################


def IF_CLOSED(): #Open a warning window when exit button is clicked. If yes clicked: close the app and the camera review.
    if app.yesno("Close", "Do you really want to exit?"): #
        camera.stop_preview()
        pwm_blue.ChangeDutyCycle(0)
        pwm_bf.ChangeDutyCycle(0)
        app.destroy()

        ######################################################################################################################################

                #CONTROL LIGHTS
        
def BF_ON(): #Light up the LED if it is off
    pwm_bf.ChangeDutyCycle(intensity_bf.value)
    bf_on.tk.configure(background='white')
    
    
def BF_OFF():
    pwm_bf.ChangeDutyCycle(0)
    bf_on.tk.configure(background='#D3D3D3')

def INTENSITY_LIGHT_BF():
    if intensity_bf.value != 0 :
        pwm_bf.ChangeDutyCycle(intensity_bf.value)
    else :
        pwm_bf.ChangeDutyCycle(0)
        
def BLUE_ON(): #Light up the LED depending on the intensity chosen with the slider
    pwm_blue.ChangeDutyCycle(intensity_blue.value)
    blue_on.tk.configure(background='blue')
    
def BLUE_OFF():
    pwm_blue.ChangeDutyCycle(0)
    blue_on.tk.configure(background='#D3D3D3')

def INTENSITY_LIGHT_BLUE():
    if intensity_blue.value != 0 :
        pwm_blue.ChangeDutyCycle(intensity_blue.value)
    else :
        pwm_blue.ChangeDutyCycle(0)
        
def RED_ON(): #Light up the LED depending on the intensity chosen with the slider
    pwm_red.ChangeDutyCycle(intensity_red.value)
    red_on.tk.configure(background='red')
    
def RED_OFF():
    pwm_red.ChangeDutyCycle(0)
    red_on.tk.configure(background='#D3D3D3')

def INTENSITY_LIGHT_RED():
    if intensity_red.value != 0 :
        pwm_red.ChangeDutyCycle(intensity_red.value)
    else :
        pwm_red.ChangeDutyCycle(0)

 
        ######################################################################################################################################

                    #CONTROL CAMERA
    
    
def PREVIEW_CAMERA(): #Start the preview live. Change the bacvkground of the pushbutton when ON.
    camera.start_preview(fullscreen=False, window = (10,100, 640,880)) #ON camera and choose the window dimensions and place in the screen
    preview.tk.configure(background='#C2F732') 
    camera.hflip = True
    
def CAPTURE_CAMERA(): #Take on picture
    date = day.strftime("%y%m%d_%H%M")
    camera.capture('/home/pi/Desktop/%s_%s.jpg' % (name_picture.value, date)) #Name of the single picture taken depending on what is write in the textbox
    
def OFF_CAMERA():
    camera.stop_preview()
    preview.tk.configure(background='#D3D3D3')
    apply_resolution.tk.configure(background='#D3D3D3')
    
def BRIGHTNESS_CAMERA():
    camera.brightness = camera_brightness.value #Modify the brightness depending on the value with the slider value in the box light

def CONTRAST_CAMERA():
    camera.contrast = camera_contrast.value
          
def RESOLUTION_CAMERA(): #Change the resolution by chosing in the Combobox (appears brown in the app).
    camera.framerate = 15 #enable the maximal resolution
    size_image = str(camera_resolution.value) #Take the value of the Combobox
    dimensions = size_image.split(", ") #Need  to divide the text of the Combobox and change it in a list. Then the values are modified into integers to be read as the new resolution.
    w_image=dimensions[0]
    h_image=dimensions[1]
    camera.resolution = int(w_image), int(h_image)
    apply_resolution.tk.configure(background='#842E1B') #Change the background of the pushbutton when the new resolution is set.
    
    
         ######################################################################################################################################
   
                    #CONTROL MOTOR


def X_PINS(): #Set the GPIO used to control the motor for the X axis.
    for pin in Xcontrol_pins:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,0)
        
def MOVE_XForw(): #Define the direction of the motor rotation and the time between each range of halfsteps. Anticlockwise (when the motor is mounted on the microscope)
    for halfstep in range(8):
        for pin in range(4):
            GPIO.output(Xcontrol_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.001)
    

def MOVE_XBack(): #Clockwise
    for halfstep in reversed(range(8)):        
        for pin in range(4):                
            GPIO.output(Xcontrol_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.001)
  
def RESET_MOTORX(): #Reset the step cycle to zero. Switch off the GPIO controlling the motor X.
    for pin in Xcontrol_pins:
        GPIO.output(pin, GPIO.LOW)
        
        #The following functions are the same as  the four previous ones but for Ymotor and Zmotor.
def Y_PINS():
    for pin in Ycontrol_pins:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,0)
                            
def MOVE_YForw():
    for halfstep in range(8):
        for pin in range(4):
            GPIO.output(Ycontrol_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.001)
        
def MOVE_YBack():
    for halfstep in reversed(range(8)):        
        for pin in range(4):                
            GPIO.output(Ycontrol_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.001)

def RESET_MOTORY():
    for pin in Ycontrol_pins:
        GPIO.output(pin, GPIO.LOW)

def Z_PINS():
    for pin in Zcontrol_pins:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,0)
        
def MOVE_ZDown():
    for halfstep in range(8):
        for pin in range(4):
            GPIO.output(Zcontrol_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.001)

def MOVE_ZUp():
    for halfstep in reversed(range(8)):        
        for pin in range(4):                
            GPIO.output(Zcontrol_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.001)

def RESET_MOTORZ():
    for pin in Zcontrol_pins:
        GPIO.output(pin, GPIO.LOW)


def XFORWARD(): #Control the Xmotor with the pushbutton. #Keep the number of steps done in the list x2, it will be positive numbers here. Anticlockwise.
    w = int(nb_step.value)
    x2.append(w)
    x_position = Text(XYZ_box, text = sum(x2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[5,2]) #Write the position in the GUI
    X_PINS() 
    for i in range(w): #Same as the function MOVE_XForw nut we can control the speed of the motors withe the combobox speed.
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(jaune, GPIO.HIGH)
                GPIO.output(Xcontrol_pins[pin], halfstep_seq[halfstep][pin])
            if speed.value == 'fast':
                time.sleep(0.001)
            if speed.value == 'medium':
                time.sleep(0.01) 
            if speed.value == "slow":
                time.sleep(0.1)
    RESET_MOTORX()

def XBACKWARD(): #Same as previous but Clockwise. the number of steps traveled will be negative in this direction: -w.
    w = int(nb_step.value)
    x2.append(-w)
    x_position = Text(XYZ_box, text = sum(x2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[5,2])
    X_PINS()
    for i in range(w):
        for halfstep in reversed(range(8)):
            for pin in range(4):
                GPIO.output(Xcontrol_pins[pin], halfstep_seq[halfstep][pin])
            if speed.value == 'fast':
                time.sleep(0.001)
            if speed.value == 'medium':
                time.sleep(0.01) 
            if speed.value == "slow":
                time.sleep(0.1)
    RESET_MOTORX()
    
    
def YFORWARD(): #Here keep the steps traveled in the y2 list.
    w = int(nb_step.value)
    y2.append(w)
    y_position = Text(XYZ_box, text = sum(y2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[9,2])
    Y_PINS()
    for i in range(w):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(Ycontrol_pins[pin], halfstep_seq[halfstep][pin])
            if speed.value == 'fast':
                time.sleep(0.001)
            if speed.value == 'medium':
                time.sleep(0.01) 
            if speed.value == "slow":
                time.sleep(0.1)
    RESET_MOTORY()
            
def YBACKWARD():
    w = int(nb_step.value)
    y2.append(-w)
    y_position = Text(XYZ_box, text = sum(y2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[9,2])
    Y_PINS()
    for i in range(w):
        for halfstep in reversed(range(8)):
            for pin in range(4):
                GPIO.output(Ycontrol_pins[pin], halfstep_seq[halfstep][pin])
            if speed.value == 'fast':
                time.sleep(0.001)
            if speed.value == 'medium':
                time.sleep(0.01) 
            if speed.value == "slow":
                time.sleep(0.1)
    RESET_MOTORY()


def ZDOWN():
    w = int(Znb_step.value)
    z2.append(-w)
    Text(XYZ_box, text = sum(z2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[12,2])
    Z_PINS()
    for i in range(w):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(Zcontrol_pins[pin], halfstep_seq[halfstep][pin])
            if speed.value == 'fast':
                time.sleep(0.001)
            if speed.value == 'medium':
                time.sleep(0.01) 
            if speed.value == "slow":
                time.sleep(0.1)
    RESET_MOTORZ()

def ZUP():
    w = int(Znb_step.value)
    z2.append(w)
    Text(XYZ_box, text = sum(z2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[12,2])
    Z_PINS()
    for i in range(w):
        for halfstep in reversed(range(8)):
            for pin in range(4):
                GPIO.output(Zcontrol_pins[pin], halfstep_seq[halfstep][pin])
            if speed.value == 'fast':
                time.sleep(0.001)
            if speed.value == 'medium':
                time.sleep(0.01) 
            if speed.value == "slow":
                time.sleep(0.1) 
    RESET_MOTORZ()
    
def SET_0(): #reset both list x2 and y2 to set the position 0 in the stage. The differents steps measurements and maked positions (A, B, C, D) will be relative to this 0.
    x2.clear()
    y2.clear()
    x_position = Text(XYZ_box, text = "  0  ", size=15, font="Corbel", color="red", bg='#303030', grid=[5,2]) 
    y_position = Text(XYZ_box, text = "  0  ", size=15, font="Corbel", color="red", bg='#303030', grid=[9,2])
        
    
def RESET(): #Remove all colored dots of the waffle representing the stage. Erase the position chosen for the differents points (A,B,C,D) and so clear the lists.
    axy.clear()
    bxy.clear()
    cxy.clear()
    dxy.clear()
    A.clear()
    B.clear()
    C.clear()
    D.clear()
    
    
def SET_FOCUS(): #Reset the z2 list to set up the 0 value in the z axis.
    z2.clear()
    z_position = Text(XYZ_box, text = "  0  ", size=15, font="Corbel", color="red", bg='#303030', grid=[12,2])

def GOTO_FOCUS(): #Move the Z motor to the 0 position chosen with the SET_FOCUS function. Need to reset the z2 list to tell the programm that motor Z is at the point 0.
    Z_PINS()
    for i in range (sum(z2)): #Here it is assumed that the focus point or the 0 is the lowest point defined. So if the pusbutton is clicked, the objective will go down and if the value in the z2 list <0, nothing will happend.
        MOVE_ZDown()
    z2.clear()
    RESET_MOTORZ()

def GOTO_ZERO(): #Move the motors till the 0 position set by the function SET_0. Depending on the sum of the values in the lists x2 and y2.
    X_PINS()   
    if sum(x2) > 0:
        for i in range(abs(sum(x2))):            
            MOVE_XBack()           
    if sum(x2) < 0:
        for i in range(abs(sum(x2))):
            MOVE_XForw()
    Y_PINS()    
    if sum(y2) > 0:
        for i in range(abs(sum(y2))):
            MOVE_YBack()
    if sum(y2) < 0:
        for i in range(abs(sum(y2))):
            MOVE_YForw()
    x2.clear()
    x_position = Text(XYZ_box, text = sum(x2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[5,2])
    RESET_MOTORX()
    y2.clear()
    y_position = Text(XYZ_box, text = sum(y2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[9,2])
    RESET_MOTORY()
    
def SAVE_POSITION_A(): #Write the position on the stage (x,y), read and write the value on slider x y
    axy.clear() #clear the list containing the coordinates xy for the a point before adding new ones
    A.clear()
    axy.append(sum(x2)) #add the x position to the list 
    axy.append(sum(y2)) #add the y position to the list
    A.append(sum(x2))  
    A.append(sum(y2))
    Text(position_box, axy, color='white', bg='#2A0A0A', grid = [2,4]) #write the coordinates of position a
    save_pos_a.tk.configure(background='#9FFC5D')
    
def SAVE_POSITION_AZ1(): #Position z start stack, read and write the z value on the slider
    del A[2:] #delete the 3rd item in the list if there is one to save the new z1 value.
    A.append(sum(z2))
    pos_az1 = sum(z2)
    Text(position_box, pos_az1, color='white', bg='#2A0A0A', grid = [4,4])
    save_pos_az1.tk.configure(background='#9FFC5D')
     
def SAVE_POSITION_AZ2(): #Position z end stack
    del A[3:]
    A.append(sum(z2))
    pos_az2 = sum(z2) #Write the position(/0) on the GUI
    Text(position_box, pos_az2, color='white', bg='#2A0A0A', grid = [6,4])
    save_pos_az2.tk.configure(background='#9FFC5D')

def GOTOA(): #go to the position a. ATTENTION: need to be at the 0 of the stage to find the right position. 
    x_position=axy[0] #take the first value in axy list corresponding to the x coordinate
    y_position=axy[1]
    X_PINS()
    for i in range(int(x_position)):
        MOVE_XForw()
    Y_PINS()    
    for i in range(int(y_position)):
        MOVE_YForw()
    x2.clear() # Empty the list to put the value Axy and keep the same 0.
    x2.append(axy[0])
    x_position = Text(XYZ_box, text = sum(x2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[5,2])
    RESET_MOTORX()
    y2.clear()
    y2.append(axy[1])
    y_position = Text(XYZ_box, text = sum(y2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[9,2])
    RESET_MOTORY()
    
def SAVE_POSITION_B():
    bxy.clear()
    B.clear()
    bxy.append(sum(x2)) # coordinates / 0  
    bxy.append(sum(y2))  
    B.append(sum(x2) - axy[0]) # x coordinate of B depending on A
    B.append(sum(y2) - axy[1]) # y coordinate of B depending on A
    Text(position_box, bxy, color='white', bg='#2A0A0A', grid = [2,5])
    save_pos_b.tk.configure(background='red')
    
def SAVE_POSITION_BZ1():
    del B[2:]
    B.append(sum(z2))
    pos_bz1 = sum(z2)
    Text(position_box, pos_bz1, color='white', bg='#2A0A0A', grid = [4,5])
    save_pos_bz1.tk.configure(background='red')
    
def SAVE_POSITION_BZ2():
    del B[3:]
    B.append(sum(z2))
    pos_bz2 = sum(z2)
    Text(position_box, pos_bz2, color='white', bg='#2A0A0A', grid = [6,5])
    save_pos_bz2.tk.configure(background='red')

def GOTOB(): #go to the position a. ATTENTION: need to be at the 0 of the stage to find the right position. 
    x_position=bxy[0] #take the first value in axy list corresponding to the x coordinate
    y_position=bxy[1]
    X_PINS()
    for i in range(int(x_position)):
        MOVE_XForw()
    Y_PINS()    
    for i in range(int(y_position)):
        MOVE_YForw()
    x2.clear()
    x2.append(bxy[0])
    x_position = Text(XYZ_box, text = sum(x2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[5,2])
    RESET_MOTORX()
    y2.clear()
    y2.append(bxy[1])
    y_position = Text(XYZ_box, text = sum(y2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[9,2])
    RESET_MOTORY()

def SAVE_POSITION_C():
    cxy.clear() 
    C.clear()
    cxy.append(sum(x2)) # coordinates / 0
    cxy.append(sum(y2))  
    C.append(sum(x2) - bxy[0]) # x coordinate of C depending on B
    C.append(sum(y2) - bxy[1]) 
    Text(position_box, cxy, color='white', bg='#2A0A0A', grid = [2,6])
    save_pos_c.tk.configure(background='yellow')
    
def SAVE_POSITION_CZ1():
    del C[2:]
    C.append(sum(z2))
    pos_cz1 = sum(z2)
    Text(position_box, pos_cz1, color='white', bg='#2A0A0A', grid = [4,6])
    save_pos_cz1.tk.configure(background='yellow')
    
def SAVE_POSITION_CZ2():
    del C[3:]
    C.append(sum(z2))
    pos_cz2 = sum(z2)
    Text(position_box, pos_cz2, color='white', bg='#2A0A0A', grid = [6,6])
    save_pos_cz2.tk.configure(background='yellow')

def GOTOC(): #go to the position a. ATTENTION: need to be at the 0 of the stage to find the right position. 
    x_position=cxy[0] #take the first value in axy list corresponding to the x coordinate
    y_position=cxy[1]
    X_PINS()
    for i in range(int(x_position)):
        MOVE_XForw()
    Y_PINS()    
    for i in range(int(y_position)):
        MOVE_YForw()
    x2.clear()
    x2.append(cxy[0])
    x_position = Text(XYZ_box, text = sum(x2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[5,2])
    RESET_MOTORX()
    y2.clear()
    y2.append(cxy[1])
    y_position = Text(XYZ_box, text = sum(y2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[9,2]) 
    RESET_MOTORY()

def SAVE_POSITION_D():
    dxy.clear()
    D.clear()
    dxy.append(sum(x2))  
    dxy.append(sum(y2))  
    D.append(sum(x2) - cxy[0]) 
    D.append(sum(y2) - cxy[1])    
    Text(position_box, dxy, color='white', bg='#2A0A0A', grid = [2,7])
    save_pos_d.tk.configure(background='#74DDFF')
    

def SAVE_POSITION_DZ1():
    del D[2:]
    D.append(sum(z2))
    pos_dz1 = sum(z2)
    Text(position_box, pos_dz1, color='white', bg='#2A0A0A', grid = [4,7])
    save_pos_dz1.tk.configure(background='#74DDFF')
    
def SAVE_POSITION_DZ2():
    del D[3:]
    D.append(sum(z2))
    pos_dz2 = sum(z2)
    Text(position_box, pos_dz2, color='white', bg='#2A0A0A', grid = [6,7])
    save_pos_dz2.tk.configure(background='#74DDFF')

def GOTOD(): #go to the position a. ATTENTION: need to be at the 0 of the stage to find the right position. 
    x_position=dxy[0] #take the first value in axy list corresponding to the x coordinate
    y_position=dxy[1]
    X_PINS()
    for i in range(int(x_position)):
        MOVE_XForw()
    Y_PINS()    
    for i in range(int(y_position)):
        MOVE_YForw()
    x2.clear()
    x2.append(dxy[0])
    x_position = Text(XYZ_box, text = sum(x2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[5,2])
    RESET_MOTORX()
    y2.clear()
    y2.append(dxy[1])
    y_position = Text(XYZ_box, text = sum(y2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[9,2])
    RESET_MOTORY()


         ######################################################################################################################################

                #Experiment


def OPEN_EXPERIMENT_WINDOW(): #when the pushbutton Experiment is pressed, the window for setting the experiment will open
    experiment.show(wait=True)
    
def GET_FOLDER(): #Choose the folder in which the picures will be saved during the experiement.
    path.value = app.select_folder()
    print(path)

def START_EXPERIMENT(): #Info message to confirm the begginin of the experiment.
    launch_exp = app.yesno("Settings experiment", "Do you want to validate the settings?")
    if launch_exp == True: #If yes is pressed the experiment start
        app.info("Settings", "The experiment will start.")
        EXPERIMENT()
    else: #If no, the program doesnt start the experiment and the user can change the settings.
        app.error("Settings", "You can modify the settings")

def EXPERIMENT():#try camera.capture_sequence to take pictures rapidly (cf 4.5 Picamera doc)
    delta_t = (int(total_time.value))/int(nb_exp.value) #interval between 2 pictures in minutes
    PIC = int(nb_exp.value) + 2 # define how many times the stacks or pictures for each position will be taken. +2 to have a picture at t=0 and at the end of the total time of the experiemnt.
    GOTO_FOCUS()
    GOTO_ZERO()
    count = 0 
    print(nb_exp.value)
    print(PIC)
    while count < PIC:
        for L in range(PIC): #take pictures depending the interval and the total time of the experiment
            GOTO_NEXT() #Take all pictures/stacks for each position
            GOTO_FOCUS() #Go back to the 0 position for the Z
            GOTO_ZERO() #Go back to the 0 position in XY
            dt_min = delta_t * 60 
            print(dt_min)
            time.sleep(dt_min) #Pause during the interval time in secondes
            count = count + 1 #Increment the count to move on oi the loop
            print(count)
            print("PIC", PIC)
    app.info("Experiment", "The experiment is finished")       #When all the pictures/stacks have been taken, an information window is oppened.

def GOTO_NEXT(): # ATTENTION: need to be at the 0 of the stage to find the right position. Which is done with the function EXPERIMENT.
    coordinates = [A, B, C, D] # the list coordinates contains all lists with the positions of the different points set. In those lists, the xy positions are relative to the point before meaning B is relative to A, C to B, D to C and A to 0.
    for point in coordinates:
        try:
            GOTO_FOCUS() # Lower the z position to not scratch the objective when moving
            x_position=point[0]  #take the first pos_ value in coordinates list corresponding to the x. Then move the Xmtor and the ymotor to the right position.
            y_position=point[1]
            X_PINS()
            for i in range(int(x_position)):
                if x_position >= 0:
                    MOVE_XForw()
                if x_position <= 0:
                    MOVE_XBack()     
            Y_PINS()                   
            for i in range(int(y_position)):
                if y_position >= 0:
                    MOVE_YForw()
                if y_position <= 0:
                    MOVE_YBack()
            if brght.value == 1 : # light on the wanted LED depending on the checkbox ticked (Brightfield or Blue LED)
                GPIO.output(LED2, GPIO.HIGH)
            if blue.value == 1 :
                GPIO.output(LED1, GPIO.HIGH)
            time.sleep(1) # Let the time after light on to not have a flash on the pictures 
            day = datetime.datetime.now() #Set the time of the taken picture
            date = day.strftime("%y%m%d_%H%M") #Set the way to write the date: year month day_hour/minute
            if point == A: # if it is the first point in coordinates so the position A, the Zmotor will move till the Az1 position defined and take pictures till the Az2 position is reached.
                print("A")
                Z_PINS()
                for i in range (A[2]): # A[2] = Az1 value
                    MOVE_ZUp()
                count = A[2]
                while count <= (A[3]): # A[3] = Az2 value
                    MOVE_Z_STACKS()
                    camera.capture('%s/%s_A_%s_%s.jpg'% (path.value, save_exp.value, date, count)) # The name of the picture changes every time: name of the experiment choose by the user in the TextBox, the date and the hour and then the count of steps made during the stack.
                    count = count + steps_stack.value
                z2.clear() 
                z2.append(A[3]) #Clear all lists for positions of motor and reset to the current position in this case point A.
                x2.clear()
                x2.append(axy[0])
                y2.clear()
                y2.append(axy[1])
            if point == B:
                print("B")
                Z_PINS()
                for i in range (B[2]):
                    MOVE_ZUp()
                count = B[2]
                while count <= (B[3]):
                    MOVE_Z_STACKS()
                    camera.capture('%s/%s_B_%s_%s.jpg'% (path.value, save_exp.value, date, count))
                    count = count + steps_stack.value
                z2.clear()
                z2.append(B[3])
                x2.clear()
                x2.append(bxy[0])
                y2.clear()
                y2.append(bxy[1])
            if point == C:
                print("C")
                Z_PINS()
                for i in range (C[2]):
                    MOVE_ZUp()
                count = C[2]
                while count <= C[3]:
                    MOVE_Z_STACKS()
                    camera.capture('%s/%s_C_%s_%s.jpg'% (path.value, save_exp.value, date, count))
                    count = count + steps_stack.value
                z2.clear()
                z2.append(C[3])
                x2.clear()
                x2.append(cxy[0])
                y2.clear()
                y2.append(cxy[1])
            if point == D:
                print("D")
                Z_PINS()
                for i in range (D[2]):
                    MOVE_ZUp()
                count = D[2]
                while count <= D[3]:
                    MOVE_Z_STACKS()
                    camera.capture('%s/%s_D_%s_%s.jpg'% (path.value, save_exp.value, date, count))
                    count = count + steps_stack.value
                z2.clear()
                z2.append(D[3])
                x2.clear()
                x2.append(dxy[0])
                y2.clear()
                y2.append(dxy[1])
            RESET_MOTORX()
            RESET_MOTORY()
            RESET_MOTORZ()
            GPIO.output(LED, GPIO.LOW)
            time.sleep(1)     
        except: # if all positions have been explored or if some point as not been defined, the LED is turned off and it will pause till the next time. (time.sleep in the EXPERIMENT function)
            GPIO.output(LED, GPIO.LOW)
            print("dans le cul lulu")        

def STEPS_STACK(): #give a funtion to have the slider widget controlling the number of steps between 2 images for stacks.
    print(steps_stack.value)

def MOVE_Z_STACKS(): #Move the Z motor UP according to the number of steps defined with the STEPS_STACK function.
    w = int(steps_stack.value)
    Z_PINS()
    for i in range(w):
        MOVE_ZUp()
    RESET_MOTORZ()
        
 
 
 
###########################################################APPLICATION DESIGN###################################################


app = App("BApp", width=1100, height=760) #Name the application and set up the size of the window
app.tk.configure(background='black') #Background in the application

app.when_closed = IF_CLOSED


         ######################################################################################################################################

                    #LIGHT BOX


light_box = Box(app, layout="grid", width="fill", align="top", border=True) #Create a box containing widgets in the application. Layout="grid" allow to place each element in the box where we want. 
light_box.tk.configure(background='black') #Change background
light_box.set_border(1, "white")
Text(light_box, text = "Light Control", size=15, font="Corbel", color="orange", bg="black", grid =[0,0]) #Add a text lign 

Text(light_box, text="Brightfield", color="white", bg="black", grid=[1,1])
bf_on= PushButton(light_box, command=BF_ON, text="ON", grid = [2,1]) #Add a pushbutton link to a command defined before
intensity_bf = Slider(light_box, command=INTENSITY_LIGHT_BF, start=1, end=100, grid=[3,1])
bf_off= PushButton(light_box, command=BF_OFF, text="OFF", grid = [4,1])

Text(light_box, text="                      ", color="#00CDFF", bg="black", grid=[5,1])

Text(light_box, text="Blue", color="#00CDFF", bg="black", grid=[6,1])
blue_on = PushButton(light_box, command=BLUE_ON, text="ON", grid = [7,1])
intensity_blue = Slider(light_box, command=INTENSITY_LIGHT_BLUE, start=1, end=100, grid=[8,1])
blue_off= PushButton(light_box, command=BLUE_OFF, text="OFF", grid = [9,1])

Text(light_box, text="                      ", color="#00CDFF", bg="black", grid=[10,1])

Text(light_box, text="Red", color="red", bg="black", grid=[11,1])
red_on = PushButton(light_box, command=RED_ON, text="ON", grid = [12,1])
intensity_red = Slider(light_box, command=INTENSITY_LIGHT_RED, start=1, end=100, grid=[13,1])
red_off= PushButton(light_box, command=RED_OFF, text="OFF", grid = [14,1])





         ######################################################################################################################################

                    #CAMERA BOX


camera_box = Box(app, layout="grid", width="fill", align="top", border=True)
camera_box.tk.configure(background='#303030')
camera_box.set_border(1, "white")
Text(camera_box, text = "Camera Control", size=15, font="Corbel", color="#F6DC12", bg='#303030', grid = [0,0])

preview = PushButton(camera_box, command=PREVIEW_CAMERA, text="Preview", grid = [0,1])

Text(camera_box, text=" ", bg='#303030', grid=[1,1])

capture = PushButton(camera_box, command=CAPTURE_CAMERA, text="Capture", grid = [2,1])

Text(camera_box, text = "Save as", bg='#303030', color='white', grid = [3,1])
name_picture = TextBox(camera_box, grid =[4,1])

PushButton(camera_box, command=OFF_CAMERA, text="OFF", grid = [6,1], align="right")

Text(camera_box, text=" ", bg='#303030', grid=[1,2])

Text(camera_box, text="Brightness", bg='#303030', color='white', grid = [0,4])
camera_brightness = Slider(camera_box, command=BRIGHTNESS_CAMERA, start=0, end=100, grid = [0,3]) #Add a slider widget. Need to give a name (here camera_brightness) to refer to the value chosen with the slider.

Text(camera_box, text="Contrast", bg='#303030', color='white', grid = [1,4])
camera_contrast = Slider(camera_box, command=CONTRAST_CAMERA, start=0, end=100, grid = [1,3])

Text(camera_box, text="Resolution", bg='#303030', color='white', grid = [3,3])
camera_resolution = Combo(camera_box, options=[ "640, 480","960, 720", "1440, 1080", "1920, 1440", "2592, 1944"], grid=[4,3]) 
camera_resolution.tk.configure(background='#842E1B')
apply_resolution = PushButton(camera_box, command=RESOLUTION_CAMERA, text="Apply", grid=[5,3])



         ######################################################################################################################################

                #MOTOR BOX


XYZ_box = Box(app, layout="grid", width="fill", align="top", border=True)
XYZ_box.tk.configure(background="black")
XYZ_box.set_border(1, "white")
Text(XYZ_box, text="Motor Control", font="Corbel", size=15, color="cyan", bg="black", grid=[0,0])

Text(XYZ_box, text="speed xy:", color="white", bg="black", grid=[1,1])
speed = Combo(XYZ_box, options=["fast", "slow", "medium"], grid=[2,1])
Text(XYZ_box, text="steps xy:", color="white", bg="black", grid=[1,3])
nb_step = TextBox(XYZ_box, grid=[2,3])

Text(XYZ_box, text="x", font="Times New Roman", size=15, color="white", bg="black", grid=[5,1])
PushButton(XYZ_box, command=XBACKWARD, text="<", grid=[4,2])
PushButton(XYZ_box, command=XFORWARD, text=">", grid=[6,2])

Text(XYZ_box, text="y", font="Times New Roman", size=15, color="white", bg="black", grid=[8,2])
PushButton(XYZ_box, command=YFORWARD, text='^', grid=[9,1])
PushButton(XYZ_box, command=YBACKWARD, text="v", grid=[9,3])

Text(XYZ_box, text=" ", bg="black", grid=[3,3])
Text(XYZ_box, text="       ", bg="black", grid=[7,3])
Text(XYZ_box, text="                           ", bg="black", grid=[10,3])
Text(XYZ_box, text="                           ", bg="black", grid=[15,3])

x_position = Text(XYZ_box, text = sum(x2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[5,2])
y_position = Text(XYZ_box, text = sum(y2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[9,2])


Text(XYZ_box, text="z", font="Times New Roman", size=15, color="white", bg="black", grid=[11,2])

PushButton(XYZ_box, command=ZUP, text="^", grid=[12,1])
PushButton(XYZ_box, command=ZDOWN, text="v", grid=[12,3])
Text(XYZ_box, text="speed z:", color="white", bg="black", grid=[13,1])
Text(XYZ_box, text="steps z:", color="white", bg="black", grid=[13,3])
Zspeed = Combo(XYZ_box, options=["fast","slow", "medium"], grid=[14,1])
Znb_step = TextBox(XYZ_box, grid=[14,3])

z_position = Text(XYZ_box, text = sum(z2), size=15, font="Corbel", color="#F6DC12", bg='#303030', grid=[12,2])

PushButton(XYZ_box, command=GOTO_FOCUS, text="Go to Focus", grid=[15,3])





         ######################################################################################################################################



position_box = Box(app, layout="grid", width="fill", height="fill", align="right", border=True)
position_box.tk.configure(background='black')
position_box.set_border(1, "white")
Text(position_box, text="Set coordinates", font="Corbel", size=15, color="#CC0066", bg="black", grid=[0,0])

PushButton(position_box, command=SET_0, text="SET 0", grid=[0,1])
PushButton(position_box, command=SET_FOCUS, text="Set focus",grid=[2,1])

Text(position_box, text=" ", bg="black", grid=[0,2])

Text(position_box, text="Set position:", font="Times New Roman", size='12', color="white", bg='black', grid=[0,3])
Text(position_box, text="xy", font="Times New Roman", size='12', color="white", bg='black', grid=[2,3])
Text(position_box, text="Start:", font="Times New Roman", size='12', color="white", bg='black', grid=[4,3])
Text(position_box, text="End:", font="Times New Roman", size='12', color="white", bg='black', grid=[6,3])
PushButton(position_box, command=GOTO_ZERO, text="Go to 0", grid=[8,3])

save_pos_a = PushButton(position_box, command=SAVE_POSITION_A, text="A", grid=[1,4])
save_pos_az1 = PushButton(position_box, command=SAVE_POSITION_AZ1, text="Az1", grid=[3,4])
save_pos_az2 = PushButton(position_box, command=SAVE_POSITION_AZ2, text="Az2", grid=[5,4])
PushButton(position_box, command=GOTOA, text="Go to A", grid=[7,4])

save_pos_b = PushButton(position_box, command=SAVE_POSITION_B, text="B", grid=[1,5])
save_pos_bz1 = PushButton(position_box, command=SAVE_POSITION_BZ1, text="Bz1", grid=[3,5])
save_pos_bz2 = PushButton(position_box, command=SAVE_POSITION_BZ2, text="Bz2", grid=[5,5])
PushButton(position_box, command=GOTOB, text="Go to B", grid=[7,5])

save_pos_c = PushButton(position_box, command=SAVE_POSITION_C, text="C", grid=[1,6])
save_pos_cz1 = PushButton(position_box, command=SAVE_POSITION_CZ1, text="Cz1", grid=[3,6])
save_pos_cz2 = PushButton(position_box, command=SAVE_POSITION_CZ2, text="Cz2", grid=[5,6])
PushButton(position_box, command=GOTOC, text="Go to C", grid=[7,6])

save_pos_d = PushButton(position_box, command=SAVE_POSITION_D, text="D", grid=[1,7])
save_pos_dz1 = PushButton(position_box, command=SAVE_POSITION_DZ1, text="Dz1", grid=[3,7])
save_pos_dz2 = PushButton(position_box, command=SAVE_POSITION_DZ2, text="Dz2", grid=[5,7])
PushButton(position_box, command=GOTOD, text="Go to D", grid=[7,7])

Text(position_box, text="                           ", bg="black", grid=[9,0])

EXP = PushButton(position_box, command=OPEN_EXPERIMENT_WINDOW, text="Experiment", grid=[10,5])
EXP.tk.configure(background='#FF8C00')

         ######################################################################################################################################

                    #SET EXPERIMENT


experiment = Window(app, title="Set Experiment", width=1000, height=200, bg="white", visible=False)
exp_box = Box(experiment, layout="grid", width="fill", height="fill", align="bottom", border=True)
exp_box.tk.configure(background='#2A0A0A')

Text(exp_box, text="Experiment", size=15, font="Corbel", color="#FF8C00",bg='#2A0A0A', grid=[0,0])

launch_exp = PushButton(exp_box, command=START_EXPERIMENT, text="START EXPERIMENT", align="right", grid=[10,0])
launch_exp.tk.configure(background='#FF8C00')

Text(exp_box, text="Save as ", color="white", bg='#2A0A0A', grid=[0,1])
save_exp = TextBox(exp_box, grid =[1,1])

PushButton(exp_box, command=GET_FOLDER, text="Select folder", grid=[3,1])
path = Text(exp_box, bg='#2A0A0A', color='white', grid =[4,1])

Text(exp_box, text=" ", bg='#2A0A0A', grid=[0,2])

Text(exp_box, text="[Time]", color="white", bg='#2A0A0A', grid=[0,3]) #Time interval between 2 stacks
nb_exp = TextBox(exp_box, grid=[1,3]) 

Text(exp_box, text="Total time", color="white", bg='#2A0A0A', grid=[2,3]) #Total time of the experiment
total_time = TextBox(exp_box, grid=[3,3])
Text(exp_box, text="minutes", color="white", bg='#2A0A0A', grid=[4,3])

Text(exp_box, text="   steps stack:", color="white", bg="#2A0A0A", grid=[5,3])
steps_stack = Slider(exp_box, command=STEPS_STACK, start=0, end=20, grid = [6,3])

Text(exp_box, text=" ", bg='#2A0A0A', grid=[0,4])

Text(exp_box, text="Illumination", color="white", bg='#2A0A0A', grid=[0,5])
brght = CheckBox(exp_box, text="Brightfield",  grid=[1,5])
brght.tk.configure(background='white')

blue = CheckBox(exp_box, text="Blue LED", grid=[3,5])
blue.tk.configure(background='#00BFFF')
                    
red = CheckBox(exp_box, text="Red LED", grid=[5,5])
red.tk.configure(background='red')


app.display()