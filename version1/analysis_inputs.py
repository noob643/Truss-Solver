#! python3
# analysis_inputs.py this script takes inputs from text file
# and converts them to inpts for analysis
import logging
from decimal import Decimal
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -  %(levelname)s- %(message)s')
logging.disable(logging.CRITICAL)
logging.debug('Start of program')

# Open text file name fea.input.txt, must be saved in Path.cwd()
input_file = open('fea_input.txt','r')
input_file_lines = input_file.readlines()

# GET NODES DATA and ELEMENTS DATA
# DICTIONARY STRUCTURE: nodes_data = {NODE: [X COOR,
#                                            Y COOR], ...}
nodes_data={}

# DICTIONARY STRUCTURE: elements_data = {ELEMENT: [START NODE,
#                                                 END NODE,
#                                                 MATERIAL OVERRIDE,
#                                                 STRENGTH OVERRIDE,
#                                                 YOUNGS OVERRIDE,
#                                                 DENSITY OVERRIDE,
#                                                 SECTION OVERRIDE], ...}
elements_data={}

# DICTIONARY: supports_data =[NODE, DEFINITION]
supports_data ={}

# LOADCASES ARE STORED AS A NESTED DICTIONARY:
# DICTIONARY STRUCTURE: loadcases={loadcase_number: 
#                                                   {NODE1: [SUPX, SUPY],
#                                                    NODE2: [SUPX, SUPY], ...},
#                                  loadcase_number: { :[...]}}
loadcases={}

# Read through imported file and extract data
counter=0 
for input_file_line in input_file_lines:
    for keyword in input_file_line.split(","):

# Get cooridnates for nodes from lines that start with keyword "NODES"
        if keyword == "NODES":
            for count,node in enumerate(input_file_line.split(",")):
                if count!=0:
                    nodes_data.setdefault(node.split()[0],[node.split()[1], node.split()[2]])
            logging.debug(nodes_data)

# Get connectivity for elements
        if keyword == 'ELEMENTS':
            for count,element in enumerate(input_file_line.split(",")):
                if count!=0:
                    elements_data.setdefault(element.split()[0],[element.split()[1], element.split()[2], '', '', '', '', ''])

# Update elements_data dictionary based on material overrides
        if keyword == 'ELEMENT_MAT':
            mat_override_elems = input_file_line.split(",")[1].split()
            for i in mat_override_elems:
# If no special overrides are specified, then only update material
# name and break loop
                try:
                    override_prop = input_file_line.split(",")[3].split()[0]
                except:
                    elements_data[i][2] = input_file_line.split(",")[2].split()[0]
                    continue
                elements_data[i][2] = input_file_line.split(",")[2].split()[0]
                if override_prop == "STRENGTH":
                    elements_data[i][3] = input_file_line.split(",")[3].split()[1]
                if override_prop == "YOUNGS":
                    elements_data[i][4] = input_file_line.split(",")[3].split()[1]
                if override_prop == "DENSITY":
                    elements_data[i][5] = input_file_line.split(",")[3].split()[1]

# Update elements_data dictionary based on section overrides
        if keyword == 'ELEMENT_SEC':
            sec_override_elems = input_file_line.split(",")[1].split()
            for i in sec_override_elems:
                elements_data[i][6] = input_file_line.split(",")[2].split()
            logging.debug(elements_data)


        if keyword == 'SUPPORT':
            support_nodes = input_file_line.split(",")[1].split()
            for i in support_nodes:
                supports_data.setdefault(i, input_file_line.split(",")[2][1:-1])
            logging.debug(supports_data)
            
        if keyword =='LOADCASE':
            loadcase_number = input_file_line.split()[1][:-1]
            for i in input_file_line.split(",")[2:]:
                support_node=i.split()[0]
                loadcases.setdefault(loadcase_number, {})
                loadcases[loadcase_number].setdefault(support_node,i.split()[1:3])
            #support_node = input_file_line.split(",")[3].split()[0]
            logging.debug(loadcases['1'])
