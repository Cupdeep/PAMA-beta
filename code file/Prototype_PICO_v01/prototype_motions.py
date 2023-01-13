from prototype_modules import setServoAngle

def Simple_M(AccX, duty):
    
    x = AccX
    
    angle = x / 360 +90
    
    print (angle)
    
    lastduty = duty
    
    latency = 500
    #print("Start PWM")
    #gl_PWM0_lastDuty = setServoAngle(angle, latency, gl_PWM0_lastDuty)
    setServoAngle(angle, latency, 5000)
    
    
    
    
    
    
    