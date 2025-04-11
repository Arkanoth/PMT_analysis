import ROOT
import glob
import os
import matplotlib.pyplot as plt
import numpy as np

def plot_normalized_time_over_threshold_histograms(file_list, x_max=None):
    plt.figure(figsize=(16, 9))

    # Define a list of visually distinct colors
    colors = [
        '#FF6347',  # Tomato Red
        '#4682B4',  # Steel Blue
        '#32CD32',  # Lime Green
        '#FFD700',  # Gold
        '#8A2BE2',  # Blue Violet
        '#FF7F50',  # Coral
        '#6A5ACD',  # Slate Blue
        '#FF1493',  # Deep Pink
        '#20B2AA',  # Light Sea Green
        '#FF4500',  # Orange Red
        '#1E90FF',  # Dodger Blue
        '#FFB6C1',  # Light Pink
        '#8FBC8F',  # Dark Sea Green
        '#FF8C00',  # Dark Orange
        '#DDA0DD',  # Plum
    ]

    for i, file_path in enumerate(file_list):
        root_file = ROOT.TFile(file_path)
        tree = root_file.Get("singlephotons/pmtaf_tree")
        
        time_over_threshold = []
        for event in tree:
            time_over_threshold.append(event.time_over_threshold_ns)

        time_over_threshold = np.array(time_over_threshold)
        file_name = os.path.basename(file_path).replace(".root", "")
        
        # Create histogram
        hist, bins = np.histogram(time_over_threshold, bins=150, density=False)
        
        # Normalize histogram to have the same surface area (integral = 1)
        bin_width = np.diff(bins)
        area = np.sum(hist * bin_width)
        normalized_hist = hist / area
        
        # Plot normalized histogram with the color only
        plt.bar(bins[:-1], normalized_hist, width=bin_width, 
                alpha=0.6, color=colors[i % len(colors)], 
                label=file_name, align='edge')  # No edgecolor here

        # Overlay the histogram with a step outline to highlight the entire histogram
        plt.hist(bins[:-1], bins=bins, weights=normalized_hist, histtype='step', 
                 color='black', linewidth=0.5, linestyle='solid')  # Thinner outline for the entire histogram

        root_file.Close()

    plt.xlabel("Time over threshold [ns]")
    plt.ylabel("Normalized Probability")
    plt.title("Normalized Time over Threshold Data")

    # Place the legend in the top right corner without a title
    plt.legend(loc='upper right', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.xlim(right=x_max) if x_max is not None else None

    # Save the figure in the specified directory
    output_directory = "PMT_plot"
    os.makedirs(output_directory, exist_ok=True)  # Create directory if it doesn't exist
    plt.savefig(os.path.join(output_directory, "PMTs_time_over_threshold.png"), dpi=300)
    plt.savefig(os.path.join(output_directory, "PMTs_time_over_threshold.pdf"))
    plt.close()

# Directory containing the ROOT files
root_files_directory = "root_data"
root_files = glob.glob(os.path.join(root_files_directory, "*.root"))
plot_normalized_time_over_threshold_histograms(root_files, x_max=100)

