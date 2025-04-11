import ROOT
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm  #progress bar

def get_waveform_thickness(waveform, time, threshold):
    mean_value = np.mean(waveform)
    threshold_value = mean_value * threshold
    
    indices_above_threshold = np.where(waveform >= threshold_value)[0]
    
    if len(indices_above_threshold) == 0:
        return 0
    
    start_index = indices_above_threshold[0]
    end_index = indices_above_threshold[-1]
    
    thickness = time[end_index] - time[start_index]
    return thickness

def main():
    file_path = 'sp.root'
    directory_name = 'singlephotons'
    tree_name = 'pmtaf_pulses'
    waveform_branch = 'x'
    time_branch = 't'
    threshold = 0.5
    
    root_file = ROOT.TFile(file_path)
    directory = root_file.Get(directory_name)
    tree = directory.Get(tree_name)
    
    n_entries = tree.GetEntries()
    waveform_thicknesses = []
    
    #tqdm progress bar
    for entry in tqdm(tree, total=n_entries, desc="Processing waveforms"):
        waveform = np.array(getattr(entry, waveform_branch))
        time = np.array(getattr(entry, time_branch))
        
        thickness = get_waveform_thickness(waveform, time, threshold)
        waveform_thicknesses.append(thickness)
    
    root_file.Close()
    

    plt.figure()
    plt.hist(waveform_thicknesses, bins=100, edgecolor='black')
    plt.xlabel('Wfm thickness [t]')
    plt.ylabel('Count')
    plt.title('Wfm thicknesses (50% of mean)')
    plt.show()

    np.savetxt('waveform_thicknesses.txt', waveform_thicknesses)

if __name__ == "__main__":
    main()

