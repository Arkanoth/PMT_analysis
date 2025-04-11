import ROOT

# Open the .root file
file = ROOT.TFile("pulses.root")
if file and not file.IsZombie():
    file.ls()  # List contents of the file

    # Navigate into the 'singlephotons' directory
    dir = file.Get("singlephotons")
    if dir:
        dir.ls()  # List contents of the directory

        # Example of accessing an object, e.g., a TTree named "myTree"
        tree = dir.Get("myTree")
        if tree:
            tree.Print()  # Print the structure of the tree
            tree.Show(0)  # Show the contents of the first entry
        else:
            print("TTree 'myTree' not found in the directory.")
    else:
        print("Directory 'singlephotons' not found.")
else:
    print("Failed to open file 'pulses.root'.")

