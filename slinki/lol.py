import matplotlib.pyplot as plt
from os import system
import os
import time

import matplotlib as mpl
mpl.rcParams.update({
    "text.usetex": False,
    "font.family": "STIXGeneral",
    "mathtext.fontset": "stix",
    "axes.unicode_minus": False,
})
system("rm [0-9][0-9][0-9][0-9].png")

class slinky(object):

    __N = 20
    __l1 = 1.0
    __k = 1.0
    __g = 1.0
    __m = 1.0
    __tornado = 1.0
    __slin = []
    __collapsed = []
    __topcolT = 0
    __bottomcolT = 0
    __yrange = []
    __comy0 = 0.0
    __hl = 5.0
    __hw = 0.05
    __scale = 1.0
    
    def __init__(self, _N, _l1, _k, _g, _m):
        self.__N = _N
        self.__l1 = _l1
        self.__k = _k
        self.__g = _g
        self.__m = _m
        self.__tornado = _k/(_m*_g)
        self.__bottomcolT = _N

        self.__slin.append(0.0)
        for i in range(1,self.__N):
            dy = float(self.__N - i)/float(self.__tornado)
            if dy > self.__l1:
                nt = self.__slin[-1] - dy
                self.__collapsed.append(False)
            else:
                nt = False
                self.__collapsed.append(self.__l1)
                if (i-1) < self.__bottomcolT:
                    self.__bottomcolT = (i-1)
            self.__slin.append(nt)
    
        self.__yrange = [self.gety(self.__N-1)*1.2,self.gety(self.__N-1)*-0.1]
        self.__comy0 = self.com()

    def gety(self,i):
        y = False
        if(i >= self.__topcolT) and (i <= self.__bottomcolT):
            y = self.__slin[i]
        elif(i < self.__topcolT):
            y = self.__slin[self.__topcolT]
            ctr = self.__topcolT
            while (ctr > i):
                ctr -= 1
                y += self.__collapsed[ctr]
        elif(i > self.__bottomcolT):
            y = self.__slin[self.__bottomcolT]
            ctr = self.__bottomcolT
            while (ctr < i):
                y -= self.__collapsed[ctr]
                ctr += 1
        return y
        
    def yarray(self):
        ya = []
        for i in range(self.__N):
            ya.append(self.gety(i))
        return ya

    def ten(self,i):
        ten = 0.0
        if(i != 0) and (self.__collapsed[i-1] == False):
            ten += self.__k*(self.gety(i-1) - self.gety(i))
        if(i != (self.__N - 1)) and (self.__collapsed[i] == False):
            ten += self.__k*(self.gety(i+1) - self.gety(i))
        return ten
    
    def accel(self,i):
        f = self.ten(i)
        a = 0.0
        if(self.__collapsed[i-1] == False) and ( (i == len(self.__collapsed)) or (self.__collapsed[i] == False) ):
            f -= self.__m*self.__g
            a = f/self.__m
        elif(i == self.__topcolT):
            f -= self.__m*self.__g*(self.__topcolT + 1)
            a = f/(self.__m*(self.__topcolT + 1))
        elif(i == self.__bottomcolT):
            f -= self.__m*self.__g*(self.__N - self.__bottomcolT)
            a = f/((self.__N - self.__bottomcolT)*self.__m)
        return a

    def adv(self, ylast, dt):
        ynext = []
        old = self.yarray()
        
        for i in range(self.__N):
            next = 2.0*self.gety(i) - ylast[i] + dt*dt*self.accel(i)
            ynext.append(next)
        
        for i in range(self.__N - 1):
            if( i >= self.__topcolT ) and ( i < self.__bottomcolT ):
                if((ynext[i] - ynext[i+1]) < self.__l1):
                
                    if(i+1 != self.__bottomcolT):
                        mmtBefore = 0.0
                        for j in range(self.__topcolT + 2):
                            mmtBefore += (ynext[j] - old[j])/dt
                        ynext[i+1] = mmtBefore*dt/(i+2) + old[i+1]
                    else:
                        mmtBefore = 0.0
                        for j in range(self.__N):
                            mmtBefore += (ynext[j] - old[j])/dt
                        ynext[i+1] = mmtBefore*dt/(self.__N) + old[i+1]
                
                    self.__collapsed[i] = (ynext[i] - ynext[i+1])
                    self.__topcolT = (i+1)
                    self.__slin[i] = False
                
                    
                else:
                    self.__slin[i] = ynext[i]
            elif(i == self.__bottomcolT):
                self.__slin[self.__bottomcolT] = ynext[self.__bottomcolT]
        
        return old

    def mmt(self, ylast,dt):
        tm = 0.0
        yc = self.yarray()
        for i in range(self.__N):
            tm += self.__m*(yc[i] - ylast[i])/dt
        return tm

    def com(self):
        sum = 0.0
        for i in range(self.__N):
            sum += self.__m*self.gety(i)
        return (sum/(self.__m*self.__N))

    def printSlinky(self, name, t):
        plt.figure(figsize=(32, 18), facecolor='#0a0a0a')
        ax = plt.gca()
        ax.set_facecolor('#0a0a0a')
        
        slinky_color = '#00d4ff'
        com_color = '#ff6b35'
        ref_color = '#ffd23f'
        grav_color = '#ff006e'
        ten_color = '#06ffa5'
        total_color = '#ff006e'
        
        ypos = []
        for i in range(self.__N):
            ypos.append(self.gety(i))
            if(i%1 == 0) and (i < self.__bottomcolT) and ( i >= self.__topcolT):
                self.drawForce(i, grav_color, ten_color, total_color)
        
        plt.plot([1.0]*len(ypos), ypos, 'o', color=slinky_color, markersize=20, 
                markeredgewidth=3, markeredgecolor='white', linewidth=0, label='Slinky Turns')
        
        plt.plot([1.0], self.com(), 's', color=com_color, markersize=30, 
                markeredgewidth=4, markeredgecolor='white', label='Center of Mass')
        
        ref_y = -1.0*self.__g*t*t/2.0 + self.__comy0
        plt.plot([1.0,2.0], [ref_y]*2, '-', color=ref_color, linewidth=6, label='Reference Particle')
        plt.plot([2.0], ref_y, '^', color=ref_color, markersize=35, 
                markeredgewidth=4, markeredgecolor='white')
        
        top_y_pos = self.__yrange[0] * 0.05
        if(self.__topcolT != (self.__bottomcolT)):
            plt.text(0.5, self.gety(self.__topcolT) -1, "Gravitational Force", 
                    fontsize=32, color=grav_color, weight='bold', 
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.7, edgecolor=grav_color, linewidth=3))
            plt.text(0.79, self.__yrange[1]*0.4 + self.gety(self.__topcolT)-1, "Tension Force", 
                    fontsize=32, color=ten_color, weight='bold',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.7, edgecolor=ten_color, linewidth=3))
            plt.text(1.25, self.gety(self.__topcolT)-1, "Total Force", 
                    fontsize=32, color=total_color, weight='bold',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.7, edgecolor=total_color, linewidth=3))
        
        plt.text(2.1, ref_y, "Reference Particle\n(free fall)", 
                fontsize=32, color=ref_color, weight='bold',
                bbox=dict(boxstyle='round,pad=0.8', facecolor='black', alpha=0.7, edgecolor=ref_color, linewidth=3))
        
        plt.title(f'Slinky Drop Simulation - t = {t:.3f} s', 
                 fontsize=48, color='white', weight='bold', pad=30)
        
        plt.xlabel('Position (arbitrary units)', fontsize=36, color='white', weight='bold')
        plt.ylabel('Height (arbitrary units)', fontsize=36, color='white', weight='bold')
        
        plt.ylim(self.__yrange)
        plt.xlim([0,3.0])
        ax.tick_params(axis='both', which='major', labelsize=28, colors='white', width=3, length=10)
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_linewidth(3)
        ax.spines['top'].set_linewidth(3)
        ax.spines['right'].set_linewidth(3)
        ax.spines['left'].set_linewidth(3)
        
        ax.grid(True, color='#333333', linestyle='--', linewidth=2, alpha=0.5)
        
        try:
            abs_path = os.path.abspath(name)
            plt.savefig(abs_path, dpi=150, facecolor='#0a0a0a', bbox_inches='tight', edgecolor='none')
        except Exception as e:
            print(f"Error saving {name}: {e}")
            try:
                abs_path = os.path.abspath(name)
                plt.savefig(abs_path, dpi=150, facecolor='#0a0a0a', edgecolor='none')
            except Exception as e2:
                print(f"Error saving {name} (second attempt): {e2}")
        finally:
            plt.close('all')
            time.sleep(0.01)
        
    def drawForce(self, i, grav_color, ten_color, total_color):
        plt.arrow(0.8, self.gety(i), 0, -1.0*self.__m*self.__g*self.__scale,
                 shape='full', lw=4, length_includes_head=True, 
                 head_width=self.__hw*2, head_length=self.__hl*2, 
                 color=grav_color, alpha=0.8)
        if(self.accel(i) != 0.0):
            plt.arrow(1.2, self.gety(i), 0, self.accel(i)*self.__m*self.__scale,
                     shape='full', lw=4, length_includes_head=True, 
                     head_width=self.__hw*2, head_length=self.__hl*2, 
                     color=total_color, alpha=0.8)
        if(self.ten(i) != 0.0):
            plt.arrow(0.9, self.gety(i), 0, self.ten(i)*self.__scale,
                     shape='full', lw=4, length_includes_head=True, 
                     head_width=self.__hw*2, head_length=self.__hl*2,
                     color=ten_color, alpha=0.8)
        

N = 20
l1 = 1
dt = 0.0001
endt = 10.0
imgs = 200
m = 1.0
k = 2.0
g = 1.0
t = dt
imgEvery = (endt/(dt*imgs))
ctr = 0
imgctr = 1


sl = slinky(N, l1,k,g,m)
last = sl.yarray()

time_data = []
bottom_y_data = []
top_y_data = []
bottom_vel_data = []
top_vel_data = []
bottom_accel_data = []
top_accel_data = []

prev_bottom_y = sl.gety(N - 1)
prev_top_y = sl.gety(0)

while t < endt :
    last = sl.adv(last,dt)
    
    current_bottom_y = sl.gety(N - 1)
    current_top_y = sl.gety(0)
    
    bottom_velocity = (current_bottom_y - prev_bottom_y) / dt
    top_velocity = (current_top_y - prev_top_y) / dt
    
    bottom_accel = sl.accel(N - 1)
    top_accel = sl.accel(0)
    
    time_data.append(t)
    bottom_y_data.append(current_bottom_y)
    top_y_data.append(current_top_y)
    bottom_vel_data.append(bottom_velocity)
    top_vel_data.append(top_velocity)
    bottom_accel_data.append(bottom_accel)
    top_accel_data.append(top_accel)
    
    prev_bottom_y = current_bottom_y
    prev_top_y = current_top_y
    
    if (ctr%imgEvery) == 0:
        print ("img at t = ", t)
        try:
            filename = f'{imgctr:04d}.png'
            sl.printSlinky(filename, t)
            imgctr += 1
        except Exception as e:
            print(f"Error creating image at t={t}: {e}")
            imgctr += 1
    ctr += 1
    t += dt

def plotTimeSeries(time_data, bottom_y_data, top_y_data):
    fig = plt.figure(figsize=(32, 18), facecolor='#0a0a0a')
    ax = plt.gca()
    ax.set_facecolor('#0a0a0a')
    
    bottom_color = '#ff6b35'
    top_color = '#00d4ff'
    
    ax.plot(time_data, bottom_y_data, '-', color=bottom_color, linewidth=4, label='Bottom End', alpha=0.9)
    ax.plot(time_data, top_y_data, '-', color=top_color, linewidth=4, label='Top End', alpha=0.9)
    ax.set_xlabel('Time (s)', fontsize=36, color='white', weight='bold')
    ax.set_ylabel('Position (arbitrary units)', fontsize=36, color='white', weight='bold')
    ax.set_title('Position vs Time', fontsize=48, color='white', weight='bold', pad=30)
    legend = ax.legend(fontsize=32, loc='best', facecolor='black', edgecolor='white', framealpha=0.8)
    plt.setp(legend.get_texts(), color='white')
    ax.tick_params(axis='both', which='major', labelsize=28, colors='white', width=3, length=10)
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    for spine in ax.spines.values():
        spine.set_linewidth(3)
    ax.grid(True, color='#333333', linestyle='--', linewidth=2, alpha=0.5)
    
    try:
        plt.savefig('slinky_position_vs_time.png', dpi=150, facecolor='#0a0a0a', bbox_inches='tight', edgecolor='none')
        print("Saved slinky_position_vs_time.png")
    except Exception as e:
        print(f"Error saving slinky_position_vs_time.png: {e}")
        try:
            plt.savefig('slinky_position_vs_time.png', dpi=150, facecolor='#0a0a0a', edgecolor='none')
            print("Saved slinky_position_vs_time.png (second attempt)")
        except Exception as e2:
            print(f"Error saving slinky_position_vs_time.png (second attempt): {e2}")
    finally:
        plt.close()

plotTimeSeries(time_data, bottom_y_data, top_y_data)

exit()
