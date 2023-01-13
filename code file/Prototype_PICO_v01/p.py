import machine, _thread, utime
from prototype_modules import *


#here is global variables
gl_Tmp, gl_AccX, gl_AccY, gl_AccZ, gl_GypoX, gl_GypoY, gl_GypoZ = 25, 0, 0, 0, 0, 0, 0

gl_PWM0_lastDuty = 5000

#Tmp = 0
def source_data():
    pass

def say_hello():
    print('Hello Pico!\n')

def setup_pipe():
    #lock.acquire()
    global_pipe()
    #lock.release()
    
def read_iic_sensor():
    
    global gl_Tmp, gl_AccX, gl_AccY, gl_AccZ, gl_GypoX, gl_GypoY, gl_GypoZ
    
    #print('reading Gypo:')
    #lock.acquire()
    gl_Tmp, gl_AccX, gl_AccY, gl_AccZ, gl_GypoX, gl_GypoY, gl_GypoZ = read_gypo()
    #lock.release()
    
    
def display():
    global gl_Tmp, gl_AccX
    m0 = str(gl_Tmp)
    m1 = str(gl_AccX)
    m2 = str(gl_AccY)
    m3 = str(gl_AccZ)
    m4 = str(gl_GypoX)
    m5 = str(gl_GypoY)
    m6 = str(gl_GypoZ)
    
    #print('\noled displaying:\n')
    #lock.acquire()
    oled_display(m0, m1, m2, m3, m4, m5, m6)
    #lock.release()
    
def data_output():
    global gl_Tmp, gl_AccX
    
    print("Data Outputting...")
    for i in range(100):
        
        print("\n\t", gl_Tmp, "\t" ,gl_AccX)
        utime.sleep(0.2)
        
def MAU():
    global gl_PWM0_lastDuty
    #angle = 90
    latency = 200
    
    for i in range (100):
        #print("Start PWM")
        #gl_PWM0_lastDuty = setServoAngle(angle, latency, gl_PWM0_lastDuty)
        x = gl_AccX
        angle = x / 360 +90
        print("angle=",angle)
        gl_PWM0_lastDuty = PWM_drive(angle, latency, gl_PWM0_lastDuty)
        sleep(0.5)
        
#here comes the integrated function module:
def data_pipe_update():
    #lock.acquire()
    for i in range(500):
        read_iic_sensor()
        display()
    
    #lock.release()
        
        
        
def funcs_on_thread():
    global gl_AccX
    #data_output()
    MAU()
    #setServo_0_Angle(angle, latency, gl_AccX)
   
# the main frame comes here:
def main():

    lock = _thread.allocate_lock()

    setup_pipe()

    #print(prototype_modules.gl_Tmp)
    #say_hello()

    _thread.start_new_thread(funcs_on_thread, ())
    #data_output()
    #_thread.start_new_thread(say_hello, ())
    #funcs_on_thread()
    #setServoAngle(0, 500, 5000)

    #_thread.start_new_thread(display, ())
    #_thread.start_new_thread(data_pipe_update, ())
    data_pipe_update()

    #say_hello()
    #talk_to_Pico()
    #data_output()
    #_thread.start_new_thread(display, ())

if __name__ =="__main__":
    main()