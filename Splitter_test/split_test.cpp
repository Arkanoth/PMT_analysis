void split_test()
{
    TFile *f = TFile::Open("waveforms.root");

    int n_měření = 32;
    int i = 1;

    double x[n_měření], y[n_měření], ex[n_měření], ey[n_měření];

    TF1 *gaus = new TF1("gaus_f", "gaus", 0, 1);
    TH1D *h;

    for (; i <= n_měření; i++)
    {
        h = (TH1D*)f->Get(("out" + to_string(i) + "/h_Q").c_str());
        h->Fit(gaus, "QN");

        x[i-1] = i;            
        y[i-1] = gaus->GetParameter(1);
        ex[i-1] = 0;
        ey[i-1] = gaus->GetParError(1);
    }
    TGraphErrors *err = new TGraphErrors(n_měření, x, y, ex, ey);
    err->Draw();
}
