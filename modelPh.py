# импортируем модули
import numpy as np
import math
import matplotlib.pyplot as plt

def func(U):
        toch = 1000
        e = 1.6 * 10**(-19)
        m = 9.1 * 10**(-31)
        v = 4.5 * 10**6 #м/с
        l = 0.19 #м
        R1 = 0.05 #м
        R2 = 0.11 #м
        d = R2 - R1
        a_koef = e*U/(m*math.log(R2/R1))
        pos = d/2 
        r = pos + R1 
        a = a_koef/r
        vy = 0
        t = 0
        dt = l/(v*toch)
        for q in range(0,toch):
            pos = max (pos - vy*dt -  a*dt**2/2, 0)
            vy = 0 if pos == 0 else vy + a*dt
            r = pos + R1
            a = a_koef/r
    
            t += dt
            if (t > (l/v)):
                break

        return pos == 0

class MyClass:
    U = 11.276479840278625
    U_ans = 11.276479840278625
    x_= []
    y_= []

    t_ = []
    Vy = []
    Ay = []
    toch = 1000
    e = 1.6 * 10**(-19)
    m = 9.1 * 10**(-31)
    v = 4.5 * 10**6 #м/с
    l = 0.19 #м
    R1 = 0.05 #м
    R2 = 0.11 #м
    d = R2 - R1
    t_ans =0
    v_ans = 0

    def __init__(self):
        U_ans = self.BinPoisk()
    def clean(self):
        self.x_= []
        self.y_= []

        self.t_ = []
        self.Vy = []
        self.Ay = []

    def DO(self):
        self.clean()
        a_koef = self.e*self.U/(self.m*math.log(self.R2/self.R1))
        pos = self.d/2 
        r = pos + self.R1 
        a = a_koef/r
        vy = 0
        t = 0
        dt = self.l/(self.v*self.toch)
        for q in range(0,self.toch):
            self.t_.append(t)
            self.Ay.append(a)
            self.Vy.append(vy)
    
            self.x_.append(self.v*t)
            self.y_.append(pos)

            if (pos == 0):
                break


            pos = max (pos - vy*dt -  a*dt**2/2, 0)
            vy = vy if pos == 0 else vy + a*dt
            r = pos + self.R1
            a = a if pos == 0 else a_koef/r
    
            t += dt
            self.t_ans = t
            if (t > (self.l/self.v)):
                break
        self.v_ans = math.sqrt(self.v**2 + vy**2)
        self.t_ans = t
        return pos == 0
    def GetGrap(self):
        plt.subplot (2, 2, 1)    
        plt.plot(self.x_, self.y_)
        plt.axis((0, self.l, 0, self.R2-self.R1))
        plt.title("у(x)")


        plt.subplot (2, 2, 2)    
        plt.plot(self.t_, self.Vy)
        plt.title("v_y(t)")

        plt.subplot (2, 2, 3)       
        plt.plot(self.t_, self.Ay)
        plt.title("a_y(t)")

        plt.subplot (2, 2, 4)  
        plt.plot(self.t_, self.y_)
        plt.title("y(t)")
        # показываем график
        plt.show()  
    

    
    
    def BinPoisk(self):
        left = 2
        right = 100
        while right - left > 0.00001:
            mid = (left+right)/2
            if func(mid):
                right = mid 
            else:
                left = mid 
        return right
