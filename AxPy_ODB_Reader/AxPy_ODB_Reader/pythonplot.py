import pickle
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import os
import sys
import time
from sys import argv,exit
import math
import argparse

import pdb

class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        # this is the RawTextHelpFormatter._split_lines
        if text.startswith('R|'):
            return text[2:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)

def main():
    """Console script for pyfp"""
    #
    # Parse command line arguments with argparse
    #
    parser = argparse.ArgumentParser(formatter_class = SmartFormatter,
                                     description = 'Generate some reports from SAP output',
                                     usage = '%(prog)s [options]',
                                     epilog = "Example: (to be updated!!) run pdtime.py print -r R1 -n T3 -p year  sap2015.db")

    subparsers = parser.add_subparsers(help='Commands')

    # A plot command
    read_parser = subparsers.add_parser('plot', help='Plot')
    read_parser.add_argument("file", action='store', help='database file')
    read_parser.add_argument("-title", action='store', help='database file')
    read_parser.add_argument("-xtext", action='store', help='database file')
    read_parser.add_argument("-ytext", action='store', help='database file')
    read_parser.set_defaults(command='plot')


    args = parser.parse_args()


    #
    # ==========================
    #
    #  P L O T
    #
    # ==========================
    #

    if args.command == 'plot':
        

        #abqlauncher = 'C:/SIMULIA/Commands/abaqus.bat'
        #print(sys.version_info)
        #print(os.path.dirname(np.__file__))
        #time.sleep(2)
        #p = subprocess.Popen( [abqlauncher, 'python', 'ODB_Reader.py', 'read',  'ExampleODB.odb'], shell=True)
        #trash = p.communicate()
        
        plotData = np.array(pickle.load( open(args.file, "rb" ) ))
        #xData=np.linspace(0,float(args.xmaxdata),len(plotData))

        Datalen = len(plotData)

        #plotDataMax = max(plotData)
        #maximum_indices = np.where(plotData==plotDataMax)

        #plotDataMin = min(plotData)
        #minimum_indices = np.where(plotData==plotDataMin)


        print('MAX: %f' %(np.amax(plotData)))
        print('MIN: %f' %(np.amin(plotData)))



        #os.remove('dump.db')
        
        #print(plotData)
        #print(type(plotData))

        plt.figure(1)
        plt.plot(plotData[:,0],plotData[:,1],'b',label='ODB outputdata_SM1')
        plt.plot(plotData[:,0],plotData[:,2],'r',label='ODB outputdata_SM2')

        #plt.plot(int(maximum_indices[0]), plotDataMax, 'o', color='Red', markersize=5)
        #plt.plot(int(minimum_indices[0]), plotDataMin, 'o', color='Red', markersize=5)
        legend = plt.legend(loc='upper right', shadow=False)
        plt.xlabel(args.xtext)
        plt.ylabel(args.ytext)
        plt.title(args.title)
        plt.grid(True)
        #plt.xlim(0,max(xData))
        #plt.xlim(0,float(args.xmax))
        #plt.ylim(5,35)
        plt.draw()
        plt.savefig(args.file.replace('.db','') + '.PNG', dpi=300, bbox_inches='tight')
        #plt.show()

#==================================================================
# S T A R T
#
if __name__ == "__main__":
    main()
