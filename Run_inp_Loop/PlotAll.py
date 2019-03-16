import matplotlib.pyplot as plt
import numpy as np


Data = []
for j in range(1,6):

    for i in range(50):
        try:
            A = np.loadtxt('Results/Cluster_' +str(j)+ '_' + str(i)+'.csv',delimiter=',',skiprows=1)
            if True:#(70<A[106,1]<85) and (190<A[40,1]<220):    
                plt.plot(A[:,0],A[:,1], color='grey')
                print('Cluster_' +str(j)+ '_' + str(i)+ '----' )
        except:
            #print("An exception occurred")
            R=1

            
A = np.loadtxt('Results/Cluster_2_32.csv',delimiter=',',skiprows=1)
plt.plot(A[:,0],A[:,1], label='Prony: [[0.51,0.0001] [0.19,0.001] [0.01,0.01]]', color='b')
            
Large_ball_95A = np.loadtxt('Large_ball_95A_Track.csv',delimiter=',',skiprows=1)
plt.plot(Large_ball_95A[:,0],Large_ball_95A[:,1], 'r--', label='Large_ball_C95A: Filmed')

plt.legend()
plt.grid()
plt.xlabel('time [s]')
plt.ylabel('Height [mm]')
plt.title('Ball dropping on Trekollan C95A')

plt.show()


