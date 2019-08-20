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
Code Written by: Qiu Chang Wu
"""
 
import pandas as pd
import numpy as np
from FlowCytometryTools import FCMeasurement as FC
import os
from itertools import combinations
from fcswrite import write_fcs

#Check if polint is inside a quadrilateral
def ray_tracing_method(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

#Data input must be in a pandas dataframe
def get_14channels(data, procode_metals):
    procodes = []

    channels = data.columns
    for metal in procode_metals:
        str_metal = str(metal)
        for i,name in enumerate(channels):
            if str_metal in name:
                procodes.append(i)
    procode_col = data.iloc[:,procodes]
    return procode_col

#Reading gate from XLS 
def process_gate_coords(coord_xls):
    coord_df = pd.read_excel(coord_xls)
    coord_df = coord_df.sort_values(by= 'Metal').reset_index()
    coord_df = coord_df.iloc[:,1:]

    #get names
    metal_num = np.array(coord_df['Metal'])
    tag_name = np.array(coord_df['Name'])
    gate_coord = coord_df.iloc[:,-1]

    #get readable coordinates
    gate_coord_readable = make_coord_list(gate_coord)
    
    return metal_num, tag_name, gate_coord_readable

#Turning gate from XLS string to tuple list
def make_coord_list(gate_coord):
    coord_ls = []
    for num_metal in range(gate_coord.shape[0]):
        coordinates = gate_coord[num_metal].split('} {')
        coord_ls.append([])
        for ikset,kset in enumerate(coordinates):
            if ikset == 0:
                kset = kset.split(', ')
                kset[0] = kset[0][1:]
                kset_tuple = (float(kset[0]), float(kset[1]))
                coord_ls[num_metal].append(kset_tuple)
            elif ikset == 3:
                kset = kset.split(', ')
                kset[1] = kset[1][:-2]
                kset_tuple = (float(kset[0]), float(kset[1]))
                coord_ls[num_metal].append(kset_tuple)
            else:
                kset = kset.split(', ')
                kset_tuple = (float(kset[0]), float(kset[1]))
                coord_ls[num_metal].append(kset_tuple)
    return coord_ls

#Gets three barcodes by first assigning positive or negative within a gate
#Then searching through for only three barcoded cells
def get_3barcodes(procode_data,all_data,gate_coord):
    barcode_df = pd.DataFrame(np.zeros(procode_data.shape),columns = [procode_data.columns])
    num_metals = procode_data.shape[1]
    for i in range(num_metals):
        NGFR = all_data.loc[:,'Sm149Di']
        epitote = procode_data.iloc[:,i]
        gate = gate_coord[i]

        pos_ind = [ray_tracing_method(point[0], point[1], gate) 
               for point in np.concatenate([epitote,NGFR]).reshape(2,epitote.shape[0]).T]
    
        ones_arr = np.zeros(epitote.shape)
        ones_arr[pos_ind] = 1
        
        barcode_df.iloc[:,i] = ones_arr

    barcode_df['num barcode'] = np.sum(barcode_df, axis = 1)
    
    #get three barcoded cells
    three_barcode_df = procode_data.iloc[np.array(barcode_df['num barcode'] == 3).T[0],:]
    three_barcode_all_data = all_data.iloc[np.array(barcode_df['num barcode'] == 3).T[0],:]
    #sort by similarity of barcodes
    barcode_df = barcode_df[np.array(barcode_df['num barcode'] == 3)].sort_values(by = list(barcode_df[:-1]))
    indices = barcode_df.index
    three_barcode_df = three_barcode_df.loc[indices,:]
    three_barcode_all_data = three_barcode_all_data.loc[indices,:]

    return three_barcode_df, three_barcode_all_data, barcode_df

#Determine what type of barcodes are available 
def get_unique_barcodes(three_barcode_df, barcode_df):
    unique_row = [0]
    barcode_df = barcode_df.iloc[:,:-1]
    checker = barcode_df.iloc[0,:]

    for row in range(barcode_df.shape[0]):
        if np.sum(barcode_df.iloc[row,:] == checker) == 14:
            continue
        else:
            unique_row.append(row)
            checker = barcode_df.iloc[row,:]
    
    unique_barcodes = barcode_df.iloc[unique_row,:]
    #get barcodes
    row_ind, col_ind = np.where(np.array(unique_barcodes)==1)

    barcode_ind = col_ind.reshape(len(unique_row),3)
    barcode_ls = []
    for barcode in barcode_ind:
        barcode_ls.append(tuple(barcode))
    
    return barcode_ind, barcode_ls,unique_row


#Determine which barcodes are missing based on list
def get_missing_barcodes(folderpath,barcode_ls,tag_name):
    num_metals = tag_name.shape[0]
    all_barcodes = list(combinations(np.arange(num_metals), 3))
    missing_barcodes = set(all_barcodes) - set(barcode_ls)

    missing_names = []
    for barcode in list(missing_barcodes):
        ind = list(barcode)
        missing_names.append(np.array(tag_name)[ind])

    missing_df = pd.DataFrame(np.array(missing_names))
    print('There are {} missing barcodes'.format(len(missing_names)))
    print('Saving missing barcodes in file "missing barcodes.csv"...')
    missing_df.to_csv(folderpath+'0_Missing Barcodes.csv')
    
    return missing_names

#Write individual barcodes into their own separate file
def write_debarcoded_files(path,three_barcode_df_all_data, unique_row, barcode_ind, tag_name):
    for ibarcode,barcode in enumerate(barcode_ind):
        if ibarcode == len(unique_row)-1:
            saving_df = three_barcode_df_all_data.iloc[unique_row[ibarcode]:,:]
        else:
            saving_df = three_barcode_df_all_data.iloc[unique_row[ibarcode]:unique_row[ibarcode+1],:]

        saving_name = '-'.join(np.array(tag_name)[barcode]) + '.fcs'
        write_fcs(path+saving_name,list(three_barcode_df_all_data.columns), saving_df )
    print('Successfully wrote out debarcoded data into FCS files')
        

def folder(name):
    currentpath = os.getcwd()
    folderpath = os.path.join(currentpath, "Debarcoded FCS", name)
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
        print('Created:', folderpath)
    return folderpath +'\\'

def write_barcode_distribution_file(barcode_ls,unique_row,three_barcode_df,names_missing,path,tag_name):
    #Get barcode sizes 
    barcode_sizes = []
    for i,j in enumerate(unique_row):
        if i<len(unique_row)-1:
            barcode_sizes.append(unique_row[i+1] - unique_row[i])
        else:
            barcode_sizes.append(three_barcode_df.shape[0]- unique_row[i])
    #Get density of barcodes
    barcodes = []
    for barcode in list(barcode_ls):
        ind = list(barcode)
        barcodes.append(np.array(tag_name)[ind])

    density_df = pd.DataFrame(barcodes)
    density_df['density'] = barcode_sizes/np.sum(barcode_sizes)
    tmp_df = pd.DataFrame(np.array(names_missing))
    tmp_df['density'] = np.zeros(np.array(names_missing).shape[0])

    density_df = pd.concat([density_df, tmp_df])



    density_df.to_csv(path+'1_procode_distribution.csv')
    print('Sucessfully wrote out procode distribution file')