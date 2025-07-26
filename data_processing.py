"""
Documentation

"""

import pandas as pd
import numpy as np

def open_raw_csv():
    df = pd.read_csv("./Raw Data Files/Raw Data.csv") 
    return df

def frames_to_seconds(seconds, frames, fps):
    """
    Converts frames to seconds.

    Args:
        frames (df): number of frames counted
        seconds (df): number of seconds counted
        fps (integer): frames per second of the recording camera

    Returns:
        time_stamp (df): time stamp recorded in seconds
    """

    time_stamp = frames / fps + seconds

    return time_stamp

def baseline_averages(df):
    """
    Calculates baseline handling time averages for all categories separately.

    Args: 
        df (dataframe): input data
    
    Returns:
       averages (dict): dictionary mapping each category to its baseline average
    """

    # get all states
    states = [state for state in df['Category'].unique() if pd.notna(state)]

    averages = {}
    for state in states:
        averages[state] = df[(df['Category'] == state) & (df['Trial Name'] == 'baseline')]['Involvement Time (T_i)'].mean()

    return averages

def P_t(initial_targets, total_blocks, total_picks=5):
    k_correct = [i for i in range(total_picks+1)]
    probabilities = {}

    for k in k_correct:
        total = 0

        T = initial_targets
        N = total_blocks - initial_targets
        total += T / (T + N)

        for m in range(1, total_picks):
            T -= k / total_picks
            N -= (total_picks - k) / total_picks
            total += T / (T + N)
        
        average_pt = total / 5.0
        probabilities[k/5] = average_pt
    
    return probabilities

def process_data(fps, initial_targets, total_blocks):
    """
    Adds the following coloumns to processed csv file:
        Accuracy (%): Percent accuracy 
        Cycle Start Time (s): Start time of the foraging cycle
        Found Target Time (s): Time when participants found the to-be-selected target 
        Release Target Time (s): Time when participants release the target
        Involvement Time (T_i, s): Time spent interacting with selected target block (also called handling time for baseline trials)
        ...

    Deletes all columns with frames and seconds from csv file.
    """

    df = open_raw_csv()
    non_baseline_mask = df['Trial Name'] != 'baseline'

    # adding columns: calculating time stamps
    df['Accuracy'] = df['Accuracy (/5)'] / 5 
    df['Cycle Start Time (s)'] = frames_to_seconds(df['Cycle Start (seconds)'], df['Cycle Start (frames)'], fps)
    df['Found Target Time (s)'] = frames_to_seconds(df['Found Target (seconds)'], df['Found Target (frames)'], fps)
    df['Release Target Time (s)'] = frames_to_seconds(df['Release Target (seconds)'], df['Release Target (frames)'], fps)

    # deleting uneccesary data
    del df['Accuracy (/5)']
    del df['Cycle Start (seconds)']
    del df['Cycle Start (frames)']
    del df['Found Target (seconds)']
    del df['Found Target (frames)']
    del df['Release Target (seconds)']
    del df['Release Target (frames)']

    # creating new baseline column
    df['Involvement Time (T_i)'] = abs(df['Release Target Time (s)'] - df['Found Target Time (s)'])
    categorical_averages = baseline_averages(df)
    df['Baseline Average (T_h)'] = df['Category'].map(categorical_averages)

    # addting columns: calculating foraging times
    df.loc[non_baseline_mask, 'Search Time (T_s)'] = df['Cycle Start Time (s)'] - df['Found Target Time (s)']
    df.loc[non_baseline_mask, 'Recognition Time (T_r)'] = df['Involvement Time (T_i)'] - df['Baseline Average (T_h)']

    # adding columns: calculating efficiency data
    df.loc[non_baseline_mask, 'Efficiency (E)'] = df['Accuracy'] / (df['Search Time (T_s)'] + abs(df['Recognition Time (T_r)']) + df['Baseline Average (T_h)'])
    df['Average Efficiency (E_avg)'] = df.groupby('Trial No.')['Efficiency (E)'].transform('mean')
    df["Adjusted Accuracy (A')"] = df['Accuracy'] - 0.5 * (1 - df['Accuracy'])
    df['Discrimination Efficiency (D)'] = df["Adjusted Accuracy (A')"] / abs(df['Recognition Time (T_r)'])
    df['Average Discrimination Efficiency (D_avg)'] = df.groupby('Trial No.')['Discrimination Efficiency (D)'].transform('mean')

    # adding columns: probability calculations
    sum_per_trial = df.groupby('Trial No.')['No. of Objects Encountered'].transform('sum')
    df['P(s)'] = np.where(sum_per_trial > 0, 5 / sum_per_trial, np.nan)

    Pt_dict = P_t(initial_targets, total_blocks)
    df['P(t)'] = df['Accuracy'].map(Pt_dict)

    df['P(~t|s)'] = 1 - df['Accuracy']
    df['P(t|s)'] = df['Accuracy']

    df['Alpha Rate'] = df['P(~t|s)'] * df['P(s)'] / (1 - df['P(t)'])
    df['Beta Rate'] = 1 - df['P(t|s)'] * df['P(s)'] / df['P(t)']

    # export to csv
    df.to_csv('./Processed Data Files/Processed Data (ordered by trial).csv', index=False, float_format='%.3f')
    df_sorted = df.sort_values(by=['Category', 'Trial No.'])
    df_sorted.to_csv('./Processed Data Files/Processed Data (ordered by category).csv', index=False, float_format='%.3f')