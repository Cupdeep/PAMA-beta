from machine import I2C, Pin, PWM
from utime import *

# definitions for global vars for masu in a module
#############################################################################################
#                                                                                           #
#  masu global vars                                                                         #
#                                                                                           #
#############################################################################################
gl_servo1_duty =  5000
gl_servo2_duty =  5000
gl_servo3_duty =  5000
gl_servo4_duty =  5000
gl_servo5_duty =  5000
gl_servo6_duty =  5000
gl_servo7_duty =  5000
gl_servo8_duty =  5000

# definition of word: from left PWM1-PWM8, "0" for free, "1" for busy
gl_servos_PWM_status = 0b0000_0000_0000_0000
# PWM global duty holder
gl_PWM_d1 = 1
gl_PWM_d2 = 1
# global latency_cycle_counter
gl_latency_counter = 0
# for store and retrieve the input instruction for masu
gl_MASU_input = ""

# leave for MASU status: high 4bit for input-writeable to inform masu, low 4bit for masu-writeable to inform outer
#bit7:  in case bit3=0, masu is free, outer func push in a new masu instruction, then set bit7
#bit3:  in a masu-cycle masu retrive the instruction, set bit3, gl_servos_PWM_status becomes busy
#       after several cycle, all bit in gl_servos_PWM_status is 0, means instruction finished, then bit3 clear to 0       
gl_masu_status = 0b0000_0000

# in this dict define the actions for servos
act_dict = {                                                                                               \
     "stand"  :[[100,10,0],[100,10,0],[2,500,30],[3,500,30],[4,500,30],[5,500,30],[6,500,30],[7,500,30]],  \
     "still"  :[[100,10,180],[100,10,90],[0,500,30],[0,500,30],[0,500,30],[0,500,30],[0,500,30],[0,500,30]],  \
     "squat"  :[[200,10,90],[0,10,90],[0,500,30],[0,500,30],[0,500,30],[0,500,30],[0,500,30],[0,500,30]],  \
}

   
# definitions for masu
#############################################################################################
#                                                                                           #
#  masu functions                                                                           #
#                                                                                           #
#############################################################################################
def init_PWM():
    # Construct PWM object, with Servo1 on GPIO Pin(16)
    pwm = PWM(Pin(2))
    
    # Set the PWM frequency @50Hz, T = 20ms
    pwm.freq(50)
    
# read instruction and load slice into matrix, then set gl_MASU_status bit1
def read_instruction():
    
   
    #global act_dict
    global gl_masu_status
    global drain_Matrix
    global gl_servo1_duty,gl_servo2_duty
    global gl_latency_counter
    global gl_MASU_input
    
    
    #print("reading_instruction")
    #print(act_dict["still"])
    #print(gl_MASU_input)
    if gl_MASU_input=="":
        return
    #load into matrix
    drain_Matrix = act_dict[gl_MASU_input]
    #set bit1, means matrix has loaded
    gl_masu_status = gl_masu_status | 0b0000_1000
    
    
    #global cycle counter
    if gl_latency_counter < 255:
        gl_latency_counter += 1
    else:
        gl_latency_counter = 1
        
    # PWM drive and then write back 
    drain_Matrix[0][0], drain_Matrix[0][1], drain_Matrix[0][2], gl_servo1_duty = \
                      PWM1_drive(drain_Matrix[0][0], drain_Matrix[0][1], drain_Matrix[0][2], gl_servo1_duty)
    
    drain_Matrix[1][0], drain_Matrix[1][1], drain_Matrix[1][2], gl_servo2_duty = \
                      PWM2_drive(drain_Matrix[1][0], drain_Matrix[1][1], drain_Matrix[1][2], gl_servo2_duty)
        
    #print("sequ,latency,angle,lastduty")
    #print(drain_Matrix[0][0],drain_Matrix[0][1], drain_Matrix[0][2], gl_servo1_duty)
    #print(gl_servo1_duty)
    #print(bin(gl_servos_PWM_status))
    #print(bin(gl_masu_status))
    
        
        
    if gl_servos_PWM_status==0:
        gl_masu_status = gl_masu_status & 0b0111_0111
        gl_MASU_input = ""
    
    return 

# definitions PWM1_drive
#############################################################################################
#                                                                                           #
#  PWM1_drive                                                                               #
#                                                                                           #
#############################################################################################
# para: sequ,latency,angle,lastduty       
def PWM1_drive(sequ,latency,angle,lastduty):
    global gl_PWM_d1
    global gl_servos_PWM_status
    
    #when enter this func set PWM1(bit15)
    gl_servos_PWM_status = gl_servos_PWM_status | 0b1000_0000_0000_0000
    
    # Construct PWM object, with Servo1 on GPIO Pin(16)
    pwm = PWM(Pin(2))
    
    # Set the PWM frequency @50Hz, T = 20ms
    pwm.freq(50)
    
    # recieve para
    duty = lastduty
        
    # recieve pare
    latency = latency
  
    #revieve para and convert destination degree to setduty(setduty:1638-8190 @ angle:0-180)
    setduty = round((angle / 90 + 0.5)*3276)
    
    # drain the sequence (this para transmit through function and eventurely the global var)
    if sequ>0:
        sequ -= 1
        
    # setup an approaching prosess
    # servo dead_zone=5us, so shall >5LSB @LSB=3.2768 bit/us
    # only gl_latency_counter%latency==0 then get into 
    if abs(duty - setduty) > 60 and gl_latency_counter%latency==0 and sequ==0: 
        duty += gl_PWM_d1
        if duty > setduty:
            #duty = 255
            gl_PWM_d1 = -5
        if duty < setduty:
            #duty = 0
            gl_PWM_d1 = 5
        pwm.duty_u16(duty)
        
    if abs(duty - setduty) <= 60:
        #when servo get to aim, clear its busy bit
        gl_servos_PWM_status = gl_servos_PWM_status & 0b0111_1111_1111_1111
       
    #pwm.deinit()
    return sequ,latency,angle,duty

def PWM2_drive(sequ,latency,angle,lastduty):
    global gl_PWM_d2
    global gl_servos_PWM_status
    
    #when enter this func set PWM1(bit14)
    gl_servos_PWM_status = gl_servos_PWM_status | 0b0100_0000_0000_0000
    
    # Construct PWM object, with Servo1 on GPIO Pin(16)
    pwm = PWM(Pin(3))
    
    # Set the PWM frequency @50Hz, T = 20ms
    pwm.freq(50)
    
    # recieve para
    duty = lastduty
        
    # recieve pare
    latency = latency
  
    #revieve para and convert destination degree to setduty(setduty:1638-8190 @ angle:0-180)
    setduty = round((angle / 90 + 0.5)*3276)
    
    # drain the sequence (this para transmit through function and eventurely the global var)
    if sequ>0:
        sequ -= 1
        
    # setup an approaching prosess
    # servo dead_zone=5us, so shall >5LSB @LSB=3.2768 bit/us
    # only gl_latency_counter%latency==0 then get into 
    if abs(duty - setduty) > 60 and gl_latency_counter%latency==0 and sequ==0:
        # PWM direction gl_PWM_dx is global, and exclusive by servos
        duty += gl_PWM_d2
        #print(duty)
        if duty > setduty:
            #duty = 255
            gl_PWM_d2 = -5
        if duty < setduty:
            #duty = 0
            gl_PWM_d2 = 5
        pwm.duty_u16(duty)
        
    if abs(duty - setduty) <= 60:
        #when servo get to aim, clear its busy bit
        gl_servos_PWM_status = gl_servos_PWM_status & 0b1011_1111_1111_1111
       
    #pwm.deinit()
    return sequ,latency,angle,duty    
        
def masu():
    
    read_instruction()
 
# below is the para transition for masu
###############################################################################
if gl_masu_status == 0:
    gl_MASU_input = "stand"
    gl_masu_status = gl_masu_status | 0b1000_0000
    
print("starting: Act1")    
print(bin(gl_masu_status))
print(bin(gl_servos_PWM_status))
print("gl_servo1_duty: ", gl_servo1_duty)
print("gl_servo2_duty: ", gl_servo2_duty)
print(gl_MASU_input)

# masu cycled in main
for i in range(8000):
    masu()
    
print("\nDone:")   
print(bin(gl_masu_status))
print(bin(gl_servos_PWM_status))
print("gl_servo1_duty: ", gl_servo1_duty)
print("gl_servo2_duty: ", gl_servo2_duty)
print(gl_MASU_input)
###############################################################################
if gl_masu_status == 0:
    gl_MASU_input = "still"
    gl_masu_status = gl_masu_status | 0b1000_0000
    
print("\nstarting: Act2")  
print(bin(gl_masu_status))
print(bin(gl_servos_PWM_status))
print(gl_MASU_input)

# masu cycled in main
for i in range(15000):
    masu()
    
print("\nDone:")      
print(bin(gl_masu_status))
print(bin(gl_servos_PWM_status))
print(gl_MASU_input)
###############################################################################
if gl_masu_status == 0:
    gl_MASU_input = "squat"
    gl_masu_status = gl_masu_status | 0b1000_0000
    
print("\nstarting: Act3")  
print(bin(gl_masu_status))
print(bin(gl_servos_PWM_status))
print(gl_MASU_input)

# masu cycled in main
for i in range(15000):
    masu()
    
print("\nDone:")      
print(bin(gl_masu_status))
print(bin(gl_servos_PWM_status))
print(gl_MASU_input)
###############################################################################
print("\ngl_servos_PWM_status: ", bin(gl_servos_PWM_status))

print("gl_servo1_duty: ", gl_servo1_duty)
print("gl_servo2_duty: ", gl_servo2_duty)
#print(bin(gl_servos_PWM_status))
print(bin(gl_masu_status))
print(gl_MASU_input)