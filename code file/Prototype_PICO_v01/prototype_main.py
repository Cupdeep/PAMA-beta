import machine, _thread
from prototype_modules import *


Tmp = 0

def say_hello():
    print('Hello Pico!\n')

def read_iic_sensor():
    print('reading Gypo:')
    
    #lock.acquire()
    read_gypo()
    #lock.release()
    #display_oled()
    return 

def setup_pipe():
    global_pipe()
    
def display():
    print('\noled displaying:\n')
    #lock.acquire()
    oled_display()
    #lock.release()

#here comes the integrated function module:
def data_pipe_update():
    lock.acquire()
    read_iic_sensor()
    lock.release()

setup_pipe()

say_hello()

lock = _thread.allocate_lock()

#_thread.start_new_thread(say_hello, ())

#_thread.start_new_thread(display, ())
_thread.start_new_thread(data_pipe_update, ())
#data_pipe_update()

#say_hello()

#display()
#_thread.start_new_thread(display, ())

