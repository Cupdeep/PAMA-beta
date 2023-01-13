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
    global Tmp
    
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
    from machine import I2C, Pin

    global i2c, accel
    global Tmp

    for i in range(5):
        
        accel_dict = accel.get_values()
        Tmp = accel_dict['Tmp']
        AccX = accel_dict['AcX']+11100-3500
        AccY = accel_dict['AcY']+1880-890
        AccZ = accel_dict['AcZ']-20000+7300-2980
        GypoX = accel_dict['GyX']+360
        GypoY = accel_dict['GyY']-150
        GypoZ = accel_dict['GyZ']+500
        
        print("Tmp ",Tmp,"\t  AccX ",AccX,"\t  AccY", AccY,"\t  AccZ", AccZ,"\tGypoX", GypoX,"\tGypoY", GypoY,"\tGypoZ", GypoZ)
        utime.sleep(0.5)
    return

def oled_display():
        
     # Display Image & text on I2C driven ssd1306 OLED display 
    from machine import Pin, I2C
    from ssd1306 import SSD1306_I2C
    import framebuf
    import utime
    
    global oled
    global Tmp
    
    buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    txt = str(Tmp)
    # Load the raspberry pi logo into the framebuffer (the image is 32x32)
    fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)

    # Clear the oled display in case it has junk on it.
    oled.fill(0)

    # Blit the image from the framebuffer to the oled display
    oled.blit(fb, 96, 0)

    for i in range(5):
        
        # Add some text
        oled.text("Raspberry Pi",5,5)    # First line text
        oled.text(txt,5,15)           # Second line text
        oled.blit(fb, 96, 0)
                                           
        # Flush up the screen and ready to display
        oled.show()                     # Display Image & text on I2C driven ssd1306 OLED display
        utime.sleep(0.5)                  # Display last for a time
        oled.fill(0) 
        
        oled.text("Raspberry Pi",5,5)   # First line text
        oled.text("Pico ATE",5,15)      # Second line text
        oled.blit(fb, 96, 0)
        
                           # Flush up the screen and ready to display
        oled.show()                     # Display Image & text on I2C driven ssd1306 OLED display
        utime.sleep(0.5)                  # Display last for a time
        oled.fill(0)
    oled.fill(0)
    oled.show() 