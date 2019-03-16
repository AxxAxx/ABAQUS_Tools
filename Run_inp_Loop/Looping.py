from sys import argv,exit
from odbAccess import openOdb
import math 
import numpy as np
import os
import subprocess
import sys
import shutil
import random

def ChangeLines(InFile, lines, newtext):
    with open(InFile, 'r') as file:
        data=file.readlines()
    for i, j in enumerate(lines):
        data[j]=('%.2f, %.2f, %.2E\n' % (newtext[i],newtext[i], 1.00E-4*(10**i)))
    with open(InFile, 'w') as file:
        file.writelines(data)
name = 'BallDrop'
Prony = [[0.51, 0.26, 0.02]]

for Loop in range(100):
    A = []
    PronyRand = [1,1,1]
    
    a=random.randrange(0, 100)/100.0
    b=random.randrange(0, 100)/100.0
    c=random.randrange(0, 100)/100.0
    PronyRand = [a,b,c]    
    #while sum(PronyRand)>=1 or (0.4>PronyRand[0] or PronyRand[0]>0.6) or (0.2>PronyRand[1] or PronyRand[1]>0.4) or (0.02>PronyRand[2] or PronyRand[2]>0.2):
    while sum(PronyRand)>=0.8 or PronyRand[2]>PronyRand[1] or PronyRand[1]>PronyRand[0]:
        a=random.randrange(0, 100)/100.0
        b=random.randrange(0, 100)/100.0
        c=random.randrange(0, 100)/100.0
        PronyRand = [a,b,c]
        
    ChangeLines('BallDrop.inp', range(2062-1, 2064-1), PronyRand)
    #shutil.copy('BallDrop.inp', str(Loop)+'.inp')
    
    #HERE ONE IS FOR LOCAL AND ONE FOR ABB CLUSTER!!!
    strCommandLine = '/pgm/abaqus2018/CAE/2018/linux_a64/code/bin/./ABQLauncher interactive job=' + name + '.inp cpus=4 double=both ask_delete=OFF' 
    #strCommandLine = 'abaqus.bat interactive job=' + name + '.inp cpus=4 double=both ask_delete=OFF' 

    #FNULL = open(os.devnull, 'w')
    subprocess.call(strCommandLine, shell=True)#, stdout=FNULL, stderr=subprocess.STDOUT)

    odb = openOdb(name+'.odb', readOnly = True)
    assembly = odb.rootAssembly

    #for j in assembly.nodeSets.values():
    #    print(j.name)

    for frame in odb.steps['Step-1'].frames:
        displacement = frame.fieldOutputs['UT']
        OutputNode = odb.rootAssembly.nodeSets['RP']
        NodeDisp = displacement.getSubset(region=OutputNode)

        for v in NodeDisp.values:        
            A.append(str(frame.frameValue) + ',' + str(v.data[1]))
            
    with open('Cluster_4_'+str(Loop) + '.csv', 'w') as out_file:
        for i in A:
            out_file.write(i+'\n')
    
    with open('Prony_Cluster_4.csv', 'a+') as out_file:
        out_file.write(str(Loop) + str(PronyRand) + '\n')
        
