# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
ODBBeamReader.py
Code to determine the location and value of the maximum
SF, SM(1&2) and a combination of these two in an output database
containing several timesteps.
Usage: abaqus python odbMaxMises.py -odb odbName -elset elsetName
       
Requirements:
1. -odb   : Name of the output database.
2. -elset : Name of the assembly level element set.
            Search will be done only for element belonging
            to this set. If this parameter is not provided,
            search will be performed over the entire model.
3. -help  : Print usage
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from sys import argv,exit
import math 
import argparse
import numpy as np
#from prettytable.prettytable import *
import sys
import os
import pickle
import subprocess
import timeit
#import matplotlib.pyplot as plt
from odbAccess import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class SmartFormatter(argparse.HelpFormatter):

        def _split_lines(self, text, width):
            # this is the RawTextHelpFormatter._split_lines
            if text.startswith('R|'):
                return text[2:].splitlines()  
            return argparse.HelpFormatter._split_lines(self, text, width)       
            
def main():


     

    def colorText(plaintext, color):
        if color == 'r':
            return('\x1b[0;31;40m' + plaintext  + '\x1b[0m')
        elif color == 'g':
            return('\x1b[0;32;40m' + plaintext  + '\x1b[0m')
        elif color == 'y':
            return('\x1b[0;33;40m' + plaintext  + '\x1b[0m')
        elif color == 'b':
            return('\x1b[0;34;40m' + plaintext  + '\x1b[0m')

    def processBar(procent):
        returnString = ' |'
        marks = int(procent)
        for i in range(marks):
            returnString+=str('#')
        for i in range(100-marks):
            returnString+=str('-')
        returnString+=str('| ')
        returnString+=str(procent)
        returnString+=str(' %')
        
        return returnString
        
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

        # A read command
        read_parser = subparsers.add_parser('read', help='Excel2Pandas')
        read_parser.add_argument("file", action='store', help='Excel file')
        read_parser.add_argument("-step", action='store', help='Step (Stepnumber ar all)')
        read_parser.add_argument('-frames', default= 'all', action='store', help='Frame (Framenumber or all)')
        read_parser.add_argument('-field', action='store', help='Values (Eg. S, SM, SF, U)')
        read_parser.add_argument('-fieldvalue', action='store', help='invariants (Eg. SM1, SM2, SF1, U2)')
        read_parser.add_argument('-set', action='store', help='Set (Setname)')
        read_parser.add_argument('-o', action='store', help='Output db name')
        read_parser.set_defaults(command='read')

        # A find command
        find_parser = subparsers.add_parser('find', help='Find info')
        find_parser.add_argument("file", action='store', help='ABAQUS odb file (e.g. Results.odb')
        find_parser.add_argument('-t', default='all', action='store', help='Object to search, allowed: nodesets, elsets, steps, fields')
        find_parser.add_argument('-c', default='all', action='store', help='Column to search')
        find_parser.add_argument('-s', default='None', action='store', help='ODB step')
        find_parser.set_defaults(command='find')

        # A print command    
        print_parser = subparsers.add_parser('print', help='Print info')
        print_parser.add_argument("file", action='store', help='Data file containing Pandas objects')
        print_parser.add_argument('-r', action='store', help='Type of report (Rx,x=1...2)')
        print_parser.add_argument('-n', action='store', help='Name (name,all,T3,ret)')
        print_parser.add_argument('-p', action='store', help='Period (week, month, year)')
        print_parser.set_defaults(command='print')
        
        # An export command
        export_parser = subparsers.add_parser('export', help='Export to other formats')
        export_parser.add_argument("file", action='store', help='Data file containing Pandas objects')
        export_parser.add_argument('-i', action='store', help='Individual')
        export_parser.add_argument('-f', action='store', help='Output format (taskjuggler)')
        export_parser.add_argument('-p', action='store', help='Only export project if it is in the argument database')
        export_parser.set_defaults(command='export')
        
        # A batch command
        batch_parser = subparsers.add_parser('batch', help='Batch processing')
        batch_parser.add_argument("file", action='store', help='Data file containing commands')
        batch_parser.set_defaults(command='batch')
        
        args = parser.parse_args()


        #
        # ==========================
        # 
        #  F I N D
        #
        # ========================== 
        #
        
        if args.command == 'find':
            odb = openOdb(args.file, readOnly = True)
            assembly = odb.rootAssembly
            odb.close()
            if args.t == 'nodesets':
                t_nodesets = PrettyTable([colorText('Nodesets','g')])
                for j in assembly.nodeSets.values():
                    t_nodesets.add_row([j.name])
                print(t_nodesets)
            elif args.t == 'elsets':
                t_elsets = PrettyTable([colorText('ElementSets','g')])
                for j in assembly.elementSets.values():
                    t_elsets.add_row([j.name])
                print(t_elsets)
            elif args.t == 'steps':
                t_steps = PrettyTable([colorText('StepNr','g'),colorText('StepName','g'),colorText('StepProcedure','g')])
                for j in odb.steps.values():
                    t_steps.add_row([j.number, j.name, j.procedure])
                print(t_steps)
            elif args.t == 'fields':
                try:
                    myField=args.s
                    t_fields = PrettyTable([colorText('FieldOutput','g'),colorText('Components','g'),colorText('Invariants','g')])
                    for j in odb.steps[myField].frames[-1].fieldOutputs.values():
                        t_fields.add_row([j.name, j.componentLabels, j.validInvariants])
                    print(t_fields)
                except:
                        print(colorText('You have to define a step!\nUse the -s flag','y'))
                        
            else:
                print(colorText('You have to specify what to search for!\nUse the -t flag ','y'))

        #
        # ==========================
        # 
        #  R E A D
        #
        # ========================== 
        #

        if args.command == 'read':
            odb = openOdb(args.file, readOnly = True)
            assembly = odb.rootAssembly

            try:
                elemset = assembly.elementSets[args.set]  
            except KeyError:
                print('No elementset..')
        
                #print(odb.steps['Step-1'].frames[-1].fieldOutputs['S'].componentLabels[0])
                #print(odb.steps['Step-1'].frames[-1].fieldOutputs['S'].values[0].data[0])
                        
            maxoverframes = []       
            numberOfFrames = len(odb.steps[args.step].frames)
            
            separableFieldValues = ['SF1', 'SF2', 'SF3', 'SM1', 'SM2', 'SM3', 'UT1', 'UT2', 'UT3', 'UR1', 'UR2', 'UR3' ]
            
            if args.fieldvalue in separableFieldValues:
                field = ''.join([i for i in args.fieldvalue if i.isalpha()])
                dataposition = ''.join([i for i in args.fieldvalue if not i.isalpha()])
                separableFieldvalue = True
            elif args.fieldvalue == 'mises' or 'Mises' or 'MISES':
                field = 'S'
                separableFieldvalue = False
                
            start_time = timeit.default_timer()
                
            region=odb.rootAssembly.elementSets[args.set]
            specifiedFieldValue = args.fieldvalue
            frames = odb.steps[args.step].frames
        
            print('Total number of frames: %d' %(len(frames)))
            
            for frameIndex,frame in enumerate(frames):
                #if frameIndex > 20:
                #    break
                maxlist1 = np.array([])
                maxlist2 = np.array([])
                
                #print '{0}\r'.format(processBar(100*frameIndex/numberOfFrames)), 
                elements = frame.fieldOutputs[field].getSubset(region=region).values

                for element in elements:
                    if separableFieldvalue:
                        maxlist1 = np.append(maxlist1, element.data[int(dataposition)-1])
                        maxlist2 = np.append(maxlist2, element.data[int(dataposition)])
                    
                    elif args.fieldvalue == 'mises':
                        maxlist1.append(element.mises)
            
                #maxoverframes.append(float(max(maxlist)))
                #maxoverframes = np.append(maxoverframes, float(max(maxlist.min(), maxlist.max(), key=abs)))
                maxoverframes.append([float(frame.frameValue), float(max(maxlist1.min(), maxlist1.max(), key=abs)), float(max(maxlist2.min(), maxlist2.max(), key=abs))])
            print(' ')
            print(max(maxoverframes))
            print('Time: %f' %(timeit.default_timer() - start_time))

            #maxoverframes = np.array([3,4,5,7,3,2,4])
            pickle.dump(maxoverframes, open( args.o, "wb" ))
        
            #os.system('cd C:/Users/SEAXJOH/Desktop/gitRepos/ABAQUS_tools/ODB_Reader/ODB_Reader/ \n start /wait python pythonplot.py')
            #subprocess.Popen('python pythonPlot.py')
            #p = subprocess.Popen('python pythonplot.py',cwd=r'C:/Users/SEAXJOH/Desktop/gitRepos/ABAQUS_tools/ODB_Reader/ODB_Reader/', shell=True)#,stdin=subprocess.PIPE, stdout=sys.stdout, shell=True)
        
           

        


if __name__ == "__main__":
    main()
