#include <TFile.h>
#include <TH1.h>
#include <TCanvas.h>
#include <TLegend.h>

void remove_legend_from_waveform() {
    TFile *file = TFile::Open("pulses.root");
    TH1 *hist = (TH1*)file->Get("singlephotons/wfm_Stack");

    TCanvas *canvas = new TCanvas("canvas", "Histogram", 800, 600);

    TLegend *legend = new TLegend(0.1, 0.7, 0.3, 0.9);
    legend->AddEntry(hist, "Waveform", "l");
    legend->Draw();

    hist->Draw("same");

    std::string filename = "histogramy/wfm_stack_noleg.png";
    canvas->SaveAs(filename.c_str());

    delete legend;
    delete canvas;
    file->Close();
}

