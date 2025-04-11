f = open("cfg_split32.toml", mode="w")
i = 1           #EDITOVAT
while i <= 32:
    j = str(i)

    print("[osclec_converter.out%i]" %i, file=f)
    print("invert_polarity = true", file=f)
    print("threshold = 0", file=f)
    print("rawdata_directory = \"out%i\"" %i, file=f)

    print("", file=f)

    print("[pulse_analysis.out%i]" %i, file=f)
    print("bins_ampl = 30", file=f)
    print("bins_Q = 80", file=f)
    print("bins_Qnoise = 40", file=f)
    print("cut_fraction = 0.2", file=f)
    print("threshold = 0.004", file=f)
    print("max_ampl = 0.2", file=f)

    print("", file=f)
    print("###########", file=f)
    print("", file=f)
    i = i + 1

f.close()
