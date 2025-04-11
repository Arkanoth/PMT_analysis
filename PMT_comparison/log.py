import ROOT
import os

def remove_legend_from_heatmap(hist, canvas):
    """Remove legend only from the specific heatmap."""
    if hist.GetName() == "wfm_Stack":
        # Check for legends in the canvas and remove them
        for obj in canvas.GetListOfPrimitives():
            if isinstance(obj, ROOT.TLegend):
                obj.Delete()  # Remove the legend

def process_heatmap(root_file_path, output_dir, histogram_name):
    # Open the ROOT file
    root_file = ROOT.TFile.Open(root_file_path)
    if not root_file or not root_file.IsOpen():
        print(f"Error: Cannot open file {root_file_path}.")
        return
    
    # Get the specific histogram
    hist = root_file.Get(histogram_name)
    if not hist:
        print(f"Error: Histogram {histogram_name} not found.")
        root_file.Close()
        return

    # Create a canvas for drawing the histogram
    canvas = ROOT.TCanvas(f"canvas_{hist.GetName()}", f"Histogram {hist.GetName()}", 800, 600)
    
    # Draw the histogram
    if hist.InheritsFrom("TH2"):
        hist.Draw("COLZ")
        canvas.SetLogy()  # Set y-axis to logarithmic scale if it's a heatmap
    else:
        hist.Draw("")

    # Remove the legend if this is the specific heatmap
    remove_legend_from_heatmap(hist, canvas)
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save the histogram in various formats
    canvas.SaveAs(f'{output_dir}/{hist.GetName()}.pdf')
    canvas.SaveAs(f'{output_dir}/{hist.GetName()}.png')
    canvas.SaveAs(f'{output_dir}/{hist.GetName()}.C')

    # Close the canvas and ROOT file
    canvas.Close()
    root_file.Close()

# Specify the ROOT file path, output directory, and histogram name
process_heatmap("pulses.root", "histogramy", "wfm_Stack")

