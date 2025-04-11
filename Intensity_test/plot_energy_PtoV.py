import ROOT
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

def plot_energy_histogram(root_file_path):
    root_file = ROOT.TFile(root_file_path)
    tree = root_file.Get("singlephotons/pmtaf_tree")
    energy_values = [event.energy for event in tree]

    energy_values_filtered_for_search = [e for e in energy_values if e >= 0.1]
    mean_energy = np.mean(energy_values_filtered_for_search)
    stddev_energy = np.std(energy_values_filtered_for_search)
    upper_limit = mean_energy + 3 * stddev_energy

    filtered_energy_values_for_histogram = [e for e in energy_values if e <= upper_limit]
    
    expelled_data_pedestal = [e for e in energy_values if e < 0.1]
    expelled_data_3sigma = [e for e in energy_values if e > upper_limit]
    expelled_data = expelled_data_pedestal + expelled_data_3sigma

    if len(filtered_energy_values_for_histogram) == 0:
        print("No valid energy values after filtering")
        return

    mean_energy = np.mean(filtered_energy_values_for_histogram)
    stddev_energy = np.std(filtered_energy_values_for_histogram)

    min_energy = min(filtered_energy_values_for_histogram)
    max_energy = max(filtered_energy_values_for_histogram)
    bins = 300

    plt.figure(figsize=(10, 6))
    counts, bin_edges, _ = plt.hist(
        filtered_energy_values_for_histogram, bins=bins, range=(min_energy, max_energy),
        color='blue', alpha=0.7, edgecolor=None)

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    valley_start_index = np.argmax(bin_centers >= 0.1)
    valley_end_index = np.argmax(bin_centers >= 0.5)

    valley_counts = counts[valley_start_index:valley_end_index]
    valley_bin_centers = bin_centers[valley_start_index:valley_end_index]

    valley_min_index = np.argmin(valley_counts)
    valley_min_energy = valley_bin_centers[valley_min_index]


    a_manual = 9000
    b_manual = -7000
    c_manual = 0

    # Plot manual fit
    x_fit = np.linspace(0.1, 0.5, 100)
    y_manual_fit = quadratic(x_fit, a_manual, b_manual, c_manual)
    plt.plot(x_fit, y_manual_fit, color='orange', linestyle='-', label=f'Manual Fit: {a_manual:.2f}x² + {b_manual:.2f}x + {c_manual:.2f}')

    # Automatic curve_fit using valley region
    c_initial = valley_min_energy
    popt, _ = curve_fit(quadratic, valley_bin_centers, valley_counts, p0=[1, 1, c_initial])
    y_fit = quadratic(x_fit, *popt)
    plt.plot(x_fit, y_fit, color='red', linestyle='--', label=f'Auto Fit: {popt[0]:.2f}x² + {popt[1]:.2f}x + {popt[2]:.2f}')

    peak_start_index = np.argmax(bin_centers >= valley_min_energy)
    peak_counts = counts[peak_start_index:]
    peak_bin_centers = bin_centers[peak_start_index:]
    peak_index = np.argmax(peak_counts)
    peak_value = peak_counts[peak_index]
    peak_energy = peak_bin_centers[peak_index]
    peak_to_valley_ratio = peak_value / valley_counts[valley_min_index] if valley_counts[valley_min_index] > 0 else np.nan

    plt.yscale('log')
    plt.xlabel("Energy")
    plt.ylabel("Count (Log scale)")
    plt.title("Energy Distribution with Manual & Auto Quadratic Fits")
    plt.grid(visible=True, linestyle=':', linewidth=0.5, color='gray')
    plt.tight_layout()

    legend_text = (f"Entries: {len(filtered_energy_values_for_histogram)}\n"
                   f"Mean: {mean_energy:.5f}\n"
                   f"Std dev: {stddev_energy:.5f}\n"
                   f"Peak: {peak_energy:.5f} ({peak_value:.0f})\n"
                   f"Valley: {valley_min_energy:.5f} ({valley_counts[valley_min_index]:.0f})\n"
                   f"P/V Ratio: {peak_to_valley_ratio:.2f}")
    plt.legend([legend_text], loc='upper right', fontsize=10, frameon=False)

    plt.scatter(peak_energy, peak_value, color='red', label="Peak", zorder=3)
    plt.scatter(valley_min_energy, valley_counts[valley_min_index], color='green', label="Valley", zorder=3)
    plt.axhline(y=peak_value, color='red', linestyle='--', linewidth=1.5, label="Peak Level")
    plt.axhline(y=valley_counts[valley_min_index], color='green', linestyle='--', linewidth=1.5, label="Valley Level")

    plt.savefig("Energy_Distribution_Fit.png", dpi=300)
    plt.show()

    print(f"\nPeak-to-Valley Ratio: {peak_to_valley_ratio:.2f}")
    print(f"Auto-Fitted quadratic function: f(x) = {popt[0]:.5f}x² + {popt[1]:.5f}x + {popt[2]:.5f}")
    print(f"Manual Fit: f(x) = {a_manual:.5f}x² + {b_manual:.5f}x + {c_manual:.5f}")

# Path to the ROOT file
root_file_path = "pulses.root"
plot_energy_histogram(root_file_path)
