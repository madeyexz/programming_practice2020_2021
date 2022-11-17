import time
import os

print("You ARE observing some moving objects and you are curious about its Time Dialation and Length Contraction.")

c = 299792458 # speed of light in m/s

def time_dilation(speed):
    # assuming ∆t' = 1(s)
    if speed != c:
        return float(1/(1-speed**2/c**2)**(1/2))
        
def length_contraction(speed):
    # assuming ∆l = 1(m)
    return float((1-(speed**2)/(c**2))**(1/2))
        
while True:
    v = float(input("Please enter the relative speed of the moving object (or \'-1\' to quit.): "))

    if v == -1:
        break
    try:
        t = time_dilation(v)
        l = length_contraction(v)
    except TypeError:
        print('Nothing can exceed speed of light')
        os.system('figlet -f starwars "You bullshit lier!!!"')
        break
    print('1 sec to the object will be {:.20f} sec(s) to you'.format(t))
    print('1 meter to the object will be {:.20f} meter(s) to you'.format(l))

    if l < 1:
        print("Your time travelling faster than the object")
    elif l == 1:
        print('The object is relatively stationary to you')
    else:
        os.system('figlet -f starwars "You bullshit lier!!!"')