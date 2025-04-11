import ROOT
import os

def get_histograms(directory):
    histograms = []
    
    def search(directory):
        for key in directory.GetListOfKeys():
            obj = key.ReadObj()
            if obj.InheritsFrom("TDirectoryFile"):
                search(obj)
            elif obj.InheritsFrom("TH1") or obj.InheritsFrom("TH2") or obj.InheritsFrom("TProfile"):
                histograms.append(obj)
    
    search(directory)
    return histograms

def save_histograms(histograms, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for hist in histograms:
        canvas = ROOT.TCanvas(f"canvas_{hist.GetName()}", f"Histogram {hist.GetName()}", 800, 600)
        hist.Draw("COLZ" if hist.InheritsFrom("TH2") else "")
        #canvas.SaveAs(f'{output_dir}/{hist.GetName()}.pdf')
        canvas.SaveAs(f'{output_dir}/{hist.GetName()}.png')
        #canvas.SaveAs(f'{output_dir}/{hist.GetName()}.C')
        canvas.Close()

def plot_all_histograms_from_root_file(root_file):
    root_file = ROOT.TFile.Open(root_file)
    histograms = get_histograms(root_file)

    if not histograms:
        print("V souboru nebyly nalezeny žádné histogramy.")
        return

    save_histograms(histograms, 'histogramy')

    num_histograms = len(histograms)
    ncols = int(num_histograms**0.5) + (num_histograms**0.5 % 1 > 0)
    nrows = (num_histograms + ncols - 1) // ncols

    canvas_all = ROOT.TCanvas("canvas_all", "Všechny histogramy", 1600, 900)
    canvas_all.Divide(ncols, nrows)
    
    for i, hist in enumerate(histograms):
        canvas_all.cd(i + 1)
        hist.Draw("COLZ" if hist.InheritsFrom("TH2") else "")
    
    #canvas_all.SaveAs("histogramy/all_histograms.pdf")
    canvas_all.SaveAs("histogramy/all_histograms.png")
    #canvas_all.SaveAs("histogramy/all_histograms.C")
    
    input("Stiskněte Enter pro ukončení...")

plot_all_histograms_from_root_file("pulses.root")
