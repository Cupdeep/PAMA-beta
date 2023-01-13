#from p import source_data()

def global_pipe():
    
    from machine import I2C, Pin
    import mpu6050
    from ssd1306 import SSD1306_I2C
    
    print('This is a global pipe\n')
    
    #here is global variables
    global a
    
    global b
    
    # buses variables:
    global i2c                   
    
    # mpu6050 variables:
    global accel
    global gl_Tmp, gl_AccX
    
    # HX711 variables
    global c
    
    # OLED variables
    global oled
    
    # PWM variables
    global e          
    
    #here is buses initialization and devices config
    #initialising I2C:
    
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)       # Init I2C using pins GP8 & GP9 (default I2C0 pins)
    #i2c = I2C(0, scl=Pin(1), sda=Pin(0))
    print("I2C configuration: ")
    print("    Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
    print("    Configuration: "+str(i2c)+"\n")                   # Display I2C config
    #print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
    #print("I2C Configuration: "+str(i2c))                   # Display I2C config

    
    accel = mpu6050.accel(i2c)                              # Init gyroscoper sensor
    oled = SSD1306_I2C(128, 32, i2c)                  # Init oled display(WIDTH=128, HEIGHT=32)
    
def read_gypo():
    import utime
    import mpu6050
    from machine import I2C, Pin #_thread
    
    #lock = _thread.allocate_lock()
    
    #lock.acquire()
    
    
    global i2c, accel
    #global gl_Tmp , gl_AccX


    for i in range(1):
        
        i2c.start
        accel_dict = accel.get_values()
        i2c.stop
        
        Tmp = accel_dict['Tmp']
        AccX = accel_dict['AcX']
        AccY = accel_dict['AcY']
        AccZ = accel_dict['AcZ']
        GypoX = accel_dict['GyX']
        GypoY = accel_dict['GyY']
        GypoZ = accel_dict['GyZ']      
        #print("Tmp ",Tmp,"\t  AccX ",AccX,"\t  AccY", AccY,"\t  AccZ", AccZ,"\tGypoX", GypoX,"\tGypoY", GypoY,"\tGypoZ", GypoZ)
        #utime.sleep(0.5)
        
        
      
    #gl_Tmp = Tmp
    #print(gl_Tmp)
    return Tmp, AccX, AccY, AccZ, GypoX, GypoY, GypoZ
    
    
def oled_display(msg0, msg1, msg2, msg3, msg4, msg5, msg6):
    
     # Display Image & text on I2C driven ssd1306 OLED display 
    from machine import Pin, I2C #_thread
    from ssd1306 import SSD1306_I2C
    import framebuf
    import utime
    
    #lock = _thread.allocate_lock()
    
    #lock.acquire()
    
    
    #buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    txt0 = msg0
    txt1 = msg1
    txt2 = msg2
    txt3 = msg3
    txt4 = msg4
    txt5 = msg5
    txt6 = msg6
    
    # Load the raspberry pi logo into the framebuffer (the image is 32x32)
    #fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)

    # Clear the oled display in case it has junk on it.
    #oled.fill(0)

    # Blit the image from the framebuffer to the oled display
    #oled.blit(fb, 96, 0)

    for i in range(1):
        
        # Add some text
        #i2c.start
        oled.fill(0)
        oled.text(txt1,5,5)            # First line text
        oled.text(txt2,5,15)           # Second line text
        oled.text(txt3,5,25)           # third line text
        
        oled.text(txt4,64,5)            # First line text
        oled.text(txt5,64,15)           # Second line text
        oled.text(txt6,64,25)           # third line text
        #oled.blit(fb, 96, 0)
                                           
        # Flush up the screen and ready to display
        oled.show()                     # Display Image & text on I2C driven ssd1306 OLED display
        #i2c.stop
        utime.sleep(0.2)                  # Display last for a time
        



def setServoAngle(angle, latency, lastduty):
    import utime
    from machine import Pin, PWM
    
    # the global duty was set for the inital location (becos the servo dosent know actually where it is)
    duty = lastduty
    
    # initalise servo speed by latency 
    latency = 500
    
    # Construct PWM object, with Servo1 on GPIO Pin(16).
    pwm = machine.PWM(Pin(6))
    
    # Set the PWM frequency @50Hz, T = 20ms
    pwm.freq(50)
    
    #convert destination degree to setduty
    setduty = round((angle / 90 + 0.5)*3276)
    
    # the global duty was set for the inital location (becos the servo dosent know actually where it is)
    #global duty
    
    #global latency
    
    # initialise a step for fineturn the approaching prosess
    direction = 1
    
    # setup an approaching prosess
    while abs(duty - setduty) > 60 : # servo dead_zone=5us, so shall >5LSB @LSB=3.2768 bit/us
        duty += direction
        if duty > setduty:
            #duty = 255
            direction = -1
        elif duty < setduty:
            #duty = 0
            direction = 1
        pwm.duty_u16(duty)
        #sleep(0.001)               # while @second it cant be set into less than 0.001 and lost its function
        utime.sleep_us(latency)     # using this dont forget import utime(not from utime import sleep)
        
        
    pwm.deinit()
    return duty
# the global duty was set for the inital location (becos the servo dosent know actually where it is)
#duty = 5000

# initalise servo speed by latency   
#latency = 500

#while 1:
#    setAngle = int(input("Input a Servo Angle in degree: "))
#    setServoAngle(setAngle)
    
#pwm.deinit()
setServoAngle(0, 500, 5000)    