import ROOT
import os
import matplotlib.pyplot as plt
import numpy as np

def plot_energy_histogram(root_file_path):
    # Open the ROOT file
    root_file = ROOT.TFile(root_file_path)
    tree = root_file.Get("singlephotons/pmtaf_tree")  # Access the tree

    # Extract energy values
    energy_values = []
    for event in tree:
        energy_values.append(event.energy)

    # Close the ROOT file
    root_file.Close()

    # Calculate statistics
    mean_energy = np.mean(energy_values)
    stddev_energy = np.std(energy_values)

    # Calculate the 3-sigma upper limit
    upper_limit = mean_energy + 3 * stddev_energy

    # Filter the data to include only values below the 3-sigma upper limit
    filtered_energy_values = [e for e in energy_values if e <= upper_limit]

    # Determine the range and binning for the filtered data
    min_energy = min(filtered_energy_values)
    max_energy = max(filtered_energy_values)
    bins = 150

    # Plot the histogram
    plt.figure(figsize=(10, 6))

    # Create the histogram and get bin edges (for the histogram's range)
    n, bin_edges, _ = plt.hist(
        filtered_energy_values, bins=bins, range=(min_energy, max_energy),
        color='blue', alpha=0.7, edgecolor=None
    )

    # Set y-axis to logarithmic scale
    plt.yscale('log')

    # Add labels and grid
    plt.xlabel("Energy")
    plt.ylabel("Count (Log scale)")
    plt.title("Energy Distribution (3-sigma Upper Limit)")

    # Add a legend with entries, mean, and stddev
    legend_text = f"Entries: {len(filtered_energy_values)}\nMean: {mean_energy:.5f}\nStd dev: {stddev_energy:.5f}"
    plt.legend([legend_text], loc='upper right', fontsize=10, frameon=False)

    # Set grid style
    plt.grid(visible=True, linestyle=':', linewidth=0.5, color='gray')

    # Tighten layout and save the figure
    plt.tight_layout()

    # Save the figure in the current directory
    current_directory = os.getcwd()
    plt.savefig(os.path.join(current_directory, "Energy_Distribution_3sig+log.png"), dpi=300)
    plt.show()  # Show the plot

# Path to the ROOT file
root_file_path = "pulses.root"
plot_energy_histogram(root_file_path)

