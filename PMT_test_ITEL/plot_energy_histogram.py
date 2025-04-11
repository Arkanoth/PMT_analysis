import ROOT
import glob
import os
import matplotlib.pyplot as plt
import numpy as np

def plot_energy_histograms(file_list, num_bins=150):
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

    legend_labels = []
    global_min = float('inf')
    global_max = float('-inf')
    pmt_energy_stats = []

    # Load data and calculate 5-sigma limits
    for file_path in file_list:
        root_file = ROOT.TFile(file_path)
        tree = root_file.Get("singlephotons/pmtaf_tree")
        energy_values = []
        
        if tree and tree.GetEntries() > 0:
            for event in tree:
                if hasattr(event, 'energy'):
                    energy_values.append(event.energy)
            
            if energy_values:
                energy_values = np.array(energy_values)
                mean_energy = np.mean(energy_values)
                std_dev_energy = np.std(energy_values)
                x_min = mean_energy - 5 * std_dev_energy
                x_max = mean_energy + 5 * std_dev_energy

                global_min = min(global_min, x_min)
                global_max = max(global_max, x_max)
                
                file_name = os.path.basename(file_path).replace(".root", "")
                pmt_energy_stats.append((energy_values, file_name, mean_energy, std_dev_energy))

        root_file.Close()

    # Set bin edges based on global min/max and bin width
    bins = np.linspace(global_min, global_max, num_bins)
    bin_width = bins[1] - bins[0]

    # Plot each histogram
    for i, (energy_values, file_name, mean_energy, std_dev_energy) in enumerate(pmt_energy_stats):
        counts, _ = np.histogram(energy_values, bins=bins)

        # Bar plot for the histogram (no normalization)
        plt.bar(bins[:-1], counts, width=bin_width, alpha=0.6, 
                color=colors[i % len(colors)], label=file_name, align='edge')

        # Outline for histogram bins
        plt.step(bins[:-1], counts, where='post', color='black', linewidth=0.5)

        legend_labels.append(f"{file_name}\nMean: {mean_energy:.2f}, Std Dev: {std_dev_energy:.2f}")

    # Set plot labels, title, and scale
    plt.xlabel("Energy")
    plt.ylabel("Events")
    plt.title("Energy Distribution Histogram")
    plt.yscale("log")
    plt.grid(True)

    # Add legend to the plot
    plt.legend(title="PMTs", loc='upper right', bbox_to_anchor=(1, 1))

    # Save the plot
    output_directory = "PMT_plot"
    os.makedirs(output_directory, exist_ok=True)
    plt.savefig(os.path.join(output_directory, "PMTs_energy_histogram.png"), dpi=300)
    plt.savefig(os.path.join(output_directory, "PMTs_energy_histogram.pdf"))
    plt.close()

# Directory containing the ROOT files
root_files_directory = "root_data"
root_files = glob.glob(os.path.join(root_files_directory, "*.root"))

# Generate the plot
plot_energy_histograms(root_files, num_bins=100)

