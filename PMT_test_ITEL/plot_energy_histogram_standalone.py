import ROOT
import glob
import os
import matplotlib.pyplot as plt
import numpy as np

def plot_single_pmt_energy_histogram(file_path, output_dir="PMT_plot", num_bins=100):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Open the ROOT file
    root_file = ROOT.TFile(file_path)
    tree = root_file.Get("singlephotons/pmtaf_tree")

    energy_values = []
    if tree and tree.GetEntries() > 0:
        for event in tree:
            if hasattr(event, 'energy'):
                energy_values.append(event.energy)

    # Proceed only if energy values were collected
    if energy_values:
        energy_values = np.array(energy_values)
        file_name = os.path.basename(file_path).replace(".root", "")
        
        # Calculate mean and standard deviation
        mean_energy = np.mean(energy_values)
        std_dev_energy = np.std(energy_values)
        
        # Calculate the 5-sigma range
        x_min = mean_energy - 10 * std_dev_energy
        x_max = mean_energy + 10 * std_dev_energy

        # Plot the histogram of energy values for this PMT tube
        plt.figure(figsize=(16, 9))

        # Set density to False to use event counts instead of probability density
        # Add mean and std deviation to the label in the legend
        label = f"{file_name}\nMean: {mean_energy:.2f}\nStd Dev: {std_dev_energy:.2f}"
        plt.hist(energy_values, bins=num_bins, density=False, alpha=1, label=label)

        # Set plot labels, title, and grid
        plt.xlabel("Energy (10σ)")
        plt.ylabel("Event Counts")
        plt.title(f"Energy Distribution Histogram for {file_name}")
        plt.legend(title="PMT", loc='upper right', fontsize=10, frameon=True, bbox_to_anchor=(1, 1))
        plt.grid(True)

        # Set the y-axis to a logarithmic scale (base 10)
        plt.yscale('log')

        # Set the x-axis limits to the 5-sigma range
        plt.xlim(left=x_min, right=x_max)

        # Save each histogram as PNG and PDF with unique filenames in the output directory
        output_png = os.path.join(output_dir, f"plot_energy_histogram_{file_name}.png")
        output_pdf = os.path.join(output_dir, f"plot_energy_histogram_{file_name}.pdf")
        plt.savefig(output_png, dpi=300)
        plt.savefig(output_pdf)
        plt.close()  # Close the figure after saving to avoid memory issues

    root_file.Close()

# Directory containing the ROOT files
root_files_directory = "root_data"  # Update this to your directory
root_files = glob.glob(os.path.join(root_files_directory, "*.root"))

# Plot and save energy histogram for each ROOT file individually
for root_file in root_files:
    plot_single_pmt_energy_histogram(root_file, num_bins=100)  # Adjust num_bins as needed

