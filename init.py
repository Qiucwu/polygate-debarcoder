""" 
Polygate debarcoder
For debarcoding cyTOF data with 3 tag barcodes
Input:
    1. Polygonal gate coordinates for each individual channel of interest
    2. cyTOF data in a single FCS file
    3. Name of folder
Output:
    1. Debarcoded files in said named folder

Last Edited: 08/20/2019
Author: Qiu Chang Wu
Author Email: q_wu@g.harvard.edu

"""

# Run polygate functions
import polygate_debarcoder as pb
import sys
import os

#!/usr/bin/env python3
#$ chmod +x init.py

sys.path.append(os.getcwd())
fcs_path = os.getcwd()+"\\fcs_files\\"
coordinate_path = os.getcwd()+"\\coordinates\\"

#list the procode metals used for CYTOF
procode_metals = [141,142,143,153,
            156,158,159,163,165,169,
            170,171,174,175]

gate_file = coordinate_path+ input('Gate Coordinate Filename:')
FCS_file = fcs_path+ input('FCS Filename:')
foldername = input('Output foldername:')

#Get Data
data = pb.FC(ID = 'test data', datafile = FCS_file).data
data_14 = pb.get_14channels(data, procode_metals)

channel_names = data.columns

#make folder
cpath = pb.folder(foldername)

# Get gate coordinates
metal_num, tag_name, gate_coord_readable = pb.process_gate_coords(gate_file)

# Get three barcoded date
cytof_3data , cytof_3data_all_data, barcode_df = pb.get_3barcodes(data_14,data, gate_coord_readable)

#Get unique barcodes
barcode_ind, barcode_ls,unique_row = pb.get_unique_barcodes(cytof_3data, barcode_df)

#Get missing barcodes
names_missing = pb.get_missing_barcodes(cpath, barcode_ls, tag_name)

#Get barcode distribution
pb.write_barcode_distribution_file(barcode_ls, unique_row, cytof_3data,names_missing,cpath,tag_name)

#Write debarcoded_files
pb.write_debarcoded_files(cpath, cytof_3data_all_data, unique_row,barcode_ind,tag_name)