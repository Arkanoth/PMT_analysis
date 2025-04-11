#include <TFile.h>
#include <TDirectory.h>
#include <TH1.h>
#include <TCanvas.h>
#include <iostream>

void save_histogram(TH1 *hist, const char *filename_base) {

    double xmin = hist->GetXaxis()->GetXmin();
    double xmax = hist->GetXaxis()->GetXmax();
    std::cout << "Úplný rozsah x-ové osy pro histogram " << hist->GetName() << ": " << xmin << " až " << xmax << std::endl;

    TCanvas *canvas = new TCanvas("canvas", "Histogram", 800, 600);
    hist->GetXaxis()->SetRangeUser(xmin, xmax);
    hist->Draw();

    std::string png_filename = std::string(filename_base) + ".png";
    std::string pdf_filename = std::string(filename_base) + ".pdf";
    std::string root_filename = std::string(filename_base) + ".C";

    canvas->SaveAs(png_filename.c_str());
    canvas->SaveAs(pdf_filename.c_str());
    canvas->SaveAs(root_filename.c_str());

    delete canvas;
}

void expand_x_axis() {
    TFile *file = TFile::Open("pulses.root");
    TDirectory *dir = (TDirectory*)file->Get("singlephotons");

    TH1 *hist0 = (TH1*)dir->Get("h_t0");
    TH1 *hist1 = (TH1*)dir->Get("h_t1");
    TH1 *hist_max = (TH1*)dir->Get("h_t_peak");

    save_histogram(hist0, "histogramy/h_t0");
    save_histogram(hist1, "histogramy/h_t1");
    save_histogram(hist_max, "histogramy/h_t_max");

    file->Close();
}

