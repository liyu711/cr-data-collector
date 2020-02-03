import pandas as pd

import os


from utils.dataset_tools import calculate_frame_offset, fix_cam_drop_frames



def update_img_names(file, startid, data_root_old, dates, seq, data_root_new):
    skips = startid
    path_old = os.path.join(data_root_old, dates, seq)
    # Read in the old csv file
    df_original = pd.read_csv(file)
    df_filenames = pd.read_csv(file, usecols= ['filename'])
    df_filenames = df_filenames.drop_duplicates(keep='first', inplace= False)
    # Create a new csv file for output
    df_result = pd.DataFrame(columns= df_original.columns)
    # Extract old names
    filenames_old = df_original.filename
    # Create new names
    filenames_new = fix_cam_drop_frames(path_old, filenames_old)
    # Create a mapping between old and new names
    new_and_old_map = dict(zip(filenames_new,filenames_old))
    # Extract certain rows with the new name
    for name in df_filenames['filename']:
        if (skips > 0):
            skips -= 1;
            continue
        extracted_value = df_original.loc[df_original['filename'] == new_and_old_map.get(name)]
        for index, row in extracted_value.iterrows():
            df_result = df_result.append({'filename': str('%010d' % (int(name[:-4]) - startid)) + '.jpg', 'file_size': row['file_size'], 'region_count': row['region_count'],
                                          'file_attributes': row['file_attributes'],
                              'region_id':row['region_id'], 'region_shape_attributes': row['region_shape_attributes'],
                              'region_attributes': row['region_attributes']}, ignore_index= True)
    df_result = df_result.drop_duplicates(keep= 'last', inplace= False)
    # Put extracted rows into the result csv
    path_new = os.path.join(data_root_new, dates, seq)
    new_file_name = 'image_labels.csv'
    export_csv = df_result.to_csv(os.path.join(path_new, new_file_name), index= False)

def update_radar_names(file, startid, dates, seq, data_root_new):
    new_file_name = 'ramap_labels.csv'
    skips = startid
    df_original = pd.read_csv(file)
    df_result = pd.DataFrame(columns=df_original.columns)
    df_filenames = pd.read_csv(file, usecols= ['filename'])
    df_filenames = df_filenames.drop_duplicates(keep='first', inplace= False)
    first_name = int(df_filenames['filename'][0][19:-4])
    skips = skips - first_name

    for name in df_filenames['filename']:
        if skips > 0:
            skips -= 1
            continue
        extracted_value = df_original.loc[df_original['filename'] == name]
        for index, row in extracted_value.iterrows():
            df_result = df_result.append({'filename': dates + '' + seq + '_' + str('%06d' % (int(name[19:-4]) - startid)) + '.jpg', 'file_size': row['file_size'],
                                          'file_attributes': row['file_attributes'], 'region_count':row['region_count'],
                                          'region_id': row['region_id'], 'region_shape_attributes': row['region_shape_attributes'],
                                          'region_attributes': row['region_attributes']}, ignore_index= True)

    path_new = os.path.join(data_root_new, dates, seq)
    csv_output = df_result.to_csv(os.path.join(path_new, new_file_name), index= False)

# data_root_old = '/mnt/nas_crdataset'
data_root_old = '/mnt/disk1/UWCR'
dates = '2019_04_09'
seq = '2019_04_09_bms1000'
data_root_new = '/mnt/disk1/UWCR_new'
# '/mnt/nas_crdataset2'
start_id_cam = 2
start_id_radar = 2
file_name_cam = 'image_labels.csv'
file_name_rad = 'ramap_labels.csv'

file = os.path.join(data_root_old, dates, seq, file_name_cam)
    #'/mnt/disk1/UWCR/2019_04_09/2019_04_09_bms1000/image_labels.csv'
file_radar = os.path.join(data_root_old, dates, seq, file_name_rad)
    # os.path.join(data_root_old, dates, seq, file_name_rad)
# file_radar = '/mnt/disk1/UWCR/2019_04_09/2019_04_09_bms1000/ramap_labels.csv'
update_img_names(file, start_id_cam, data_root_old, dates, seq, data_root_new)
update_radar_names(file_radar, 3, dates, seq, data_root_new)
