import ROOT
import glob
import os
import matplotlib.pyplot as plt
import numpy as np

def plot_time_over_threshold_histograms(file_list):
    plt.figure(figsize=(10, 6))

    for file_path in file_list:
        root_file = ROOT.TFile(file_path)
        tree = root_file.Get("singlephotons/pmtaf_tree")
        
        time_over_threshold = []
        for event in tree:
            time_over_threshold.append(event.time_over_threshold_ns)

        time_over_threshold = np.array(time_over_threshold)
        file_name = os.path.basename(file_path).replace(".root", "")
        plt.hist(time_over_threshold, bins=100, density=True, alpha=0.6, label=file_name)
        root_file.Close()

    plt.xlabel("Time over threshold [ns]")
    plt.ylabel("Probability density")
    plt.title("Time over threshold distributions from multiple ROOT files")
    plt.legend()
    plt.grid(True)
    plt.show()


root_files_directory = "root_files"
root_files = glob.glob(os.path.join(root_files_directory, "*.root"))
plot_time_over_threshold_histograms(root_files)
