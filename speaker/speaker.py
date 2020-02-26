#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:35:47 2020

@author: tim
"""

import numpy as np
import matplotlib.pyplot as plt

def parallel(rlist):
    one_over = 0.0
    for r in rlist:
        one_over = one_over + 1.0/r
    return 1.0/one_over    

def Z(R0, L0, C, L1, R1, w):
    return R0 + 1j*w*L0 + parallel([1/(1j*w*C),1j*w*L1,R1])

def magphaseplot(x,y,title, xlabel="Frequency (Hz)", phase=True):
    # Plotting routine
    # https://stackoverflow.com/questions/9103166/multiple-axis-in-matplotlib-with-different-scales/27965971
    
    fig, host = plt.subplots(nrows=1, ncols=1)
    host.set_xlabel(xlabel)
    host.set_ylabel("Magnitude")
    host.set_title(title)
    color1 = plt.cm.hsv(0.7)
    color2 = plt.cm.hsv(0.1)
    
    p1, = host.semilogx(x, np.abs(y), color = color1, label='Magnitude')
     


    if phase:
        par1 = host.twinx()
        par1.set_ylim(-90,270)
        p2, = par1.semilogx(x, np.angle(y) * 180 / np.pi, color = color2, label='Phase')   
        lns = [p1, p2]

        
        par1.set_ylabel("Phase (degrees)")
        par1.yaxis.label.set_color(p2.get_color())
    else:
        lns = [p1]

    host.legend(handles=lns, loc='best')
    host.yaxis.label.set_color(p1.get_color())
    plt.savefig(title+'.png', dpi=300, bbox_inches='tight')
   

def phasor(base,vector,plt,color='black',label=''):
    plt.arrow(np.real(base), np.imag(base), np.real(vector), np.imag(vector), edgecolor=color, label=label)

if __name__ == "__main__":
    #https://sound-au.com/tsp.htm
    R0 = 6.2
    L0 = 1.5e-3
    C = 700e-06
    L1 = 50e-3
    R1 = 44
    
    Rs = 10
    
    wlist = np.logspace(1,5,num=500)
    
    zlist = []
    for w in wlist:
        zlist.append(Z(R0, L0, C, L1, R1, w))
    
    zlist = np.array(zlist)
    VL = zlist / (Rs + zlist) 
    IL = VL / zlist  
    PL = IL*VL #VL**2 / np.abs(zlist)
    ref_power = np.max(PL)
    PLdB = 10 * np.log10(PL/ref_power)  
    flist = wlist / 2 / np.pi
    
    magphaseplot(flist, zlist, 'Impedance')
    magphaseplot(flist, VL, 'Voltage')
    magphaseplot(flist, IL, 'Current')
    magphaseplot(flist, PL, 'Normalised power', phase = False)
   

    plt.figure()
    plt.semilogx(flist, PLdB)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Normalised power (dB)')    

    w = 440 * 2 * np.pi
    ZT = Z(R0, L0, C, L1, R1, w)
    ZL0 = 1j*w*L0
    ZC = 1/(1j*w*C)
    ZL1 = 1j*w*L1
    Vamp = 1
    Vsource = Rs / (ZT + Rs)
    Vspeaker = ZT / (ZT + Rs)
    IT = Vspeaker / ZT
    VR0 = IT * R0
    VL0 = IT * ZL0
    VC = Vspeaker - VR0 - VL0
    IC = VC / ZC
    IR1 = VC / R1
    IL1 = VC / ZL1
    Icheck = IC+IR1+IL1

    names = ["ZT","Vamp","Vsrc","Vspkr","VC","VR0","VL0","IT","IR1","IC","IL1","Icheck"]
    values = [ZT,Vamp,Vsource,Vspeaker,VC,VR0,VL0,IT,IR1,IC,IL1,Icheck]
    units = ["Ω","V","V","V","V","V","V","A","A","A","A","A"]
    print("param \t mag    unit \t phase(deg)\n")
    for name, value , unit in zip(names,values, units):
        print("%s \t %1.4f %s \t %4.1f"%(name, np.abs(value), unit, np.angle(value)*180/np.pi))

    plt.figure()
    plt.ylim([-0.2,0.5])
    plt.xlim([-0.2,0.5])
    phasor(0,Vspeaker,plt,color='red',label='VT')
    phasor(0,VC,plt)
    phasor(VC,VR0,plt)
    phasor(VC + VR0, VL0,plt)
    plt.title('voltages')
    plt.xlabel('Real (V)')
    plt.ylabel('Imag (V)')
    plt.savefig('voltage phasor.png',dpi=300,bbox='tight')
    
    plt.figure()
    plt.ylim([-31,31])
    plt.xlim([-2,60])
    phasor(0,IT*1e3,plt,color='blue',label='IT')
    phasor(0,IL1*1e3,plt)
    phasor(IL1*1e3,IR1*1e3,plt)
    phasor(1e3*(IL1+IR1),IC*1e3,plt)
    plt.title('currents')
    plt.xlabel('Real (mA)')
    plt.ylabel('Imag (mA)')
    plt.savefig('current phasor.png',dpi=300,bbox='tight')
    
    
