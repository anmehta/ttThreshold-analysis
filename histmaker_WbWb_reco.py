# list of processes (mandatory)
import os, sys
from treemaker_WbWb_reco import all_processes, available_ecm

def if3(cond, iftrue, iffalse):
    return iftrue if cond else iffalse

#hadronic = False

channel = 'CHANNELHERE' #'had' if hadronic else 'semihad'
ecm = 'ECMHERE'
#useflav=useflavHERE
#usebtagged=usebtaggedHERE

#pf="%s"%if3(usebtagged,'withbtaggedJet',if3(useflav,'withflav','noflav'))
#pf=pf+"WPpt8"

#pf="noflav"
pf="noBDT"

#if not ecm in available_ecm:
#    raise ValueError("ecm value not in available_ecm")


            
processList={key: value for key, value in all_processes.items() if ecm in available_ecm and ecm in key} #str('p8_ee_WW_ecm'+ecm) in key else str('wzp6_ee_WbWb_ecm'+ecm) in key)}  #avoid looking for semihad samples in had category

print("these are the procs",processList)

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
#prodTag = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Define the input dir (optional)

basedir="/eos/cms/store/cmst3/group/top/FCC_tt_threshold/output_condor_20241101_1121"

#inputDir="{}/WbWb/{}/{}/".format(basedir,channel,pf)##with BDT
inputDir="{}/WbWb/{}/".format(basedir,channel)

# Optional: output directory, default is local running directory
outputDir = "{}/WbWb/outputs/histmaker/{}/{}/".format(basedir,channel,pf)
print('this is outdir',outputDir)

# optional: ncpus, default is 4, -1 uses all cores available
nCPUS = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = False
intLumi = 36000 #5000000  # 5 /ab


# define some binning for various histograms
bins = {
    "phi": (100, -6.3, 6.3),
    "theta": (100, 0, 3.2),
    "p": (100, 0, 200),
    "tagger": (20, 0, 1),
    "tagged": (2, -0.5, 1.5),
    "nleps" : (5,-0.5,4.5),
    'singlebin' : (1,-0.5,0.5),
    "nbjets" : (7,-0.5,6.5),
    "njets" : (11,-0.5,10.5),
    "atleastonebjet" : (10,0.5,10.5),
    "dij": {
        "d_12": (100, 0, 100000),
        "d_23": (100, 0, 10000),
        "d_34": (100, 0, 5000),
        "d_45": (100, 0, 5000),
        "d_56": (100, 0, 5000),
    }
}


# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):



    results = []
    df = df.Define("weight", "1.0")
    weightsum     = df.Sum("weight")

    column_names  = df.GetColumnNames()
    print(column_names) 
    #df_BDT         = df.Filter("BDT_score > 0.5")
    #df_zerobVL     = df.Filter("nbjets_R5_WPp5  == 0")
    #df_onebVL      = df.Filter("nbjets_R5_WPp5  > 0")
    #df_zerobL      = df.Filter("nbjets_R5_WPp8  == 0")
    #df_onebL       = df.Filter("nbjets_R5_WPp8  > 0")
    #df_zerobM      = df.Filter("nbjets_R5_WPp85 == 0")
    #df_onebM       = df.Filter("nbjets_R5_WPp85 > 0")
    #df_zerobT      = df.Filter("nbjets_R5_WPp9  == 0")
    #df_onebT       = df.Filter("nbjets_R5_WPp9  > 0")

    df_effp9_zerob   = df.Filter("nbjets_R5_eff_p9 == 0");
    df_effp9_oneb    = df.Filter("nbjets_R5_eff_p9 == 1 ");
    df_effp9_twob    = df.Filter("nbjets_R5_eff_p9 > 1 ");
    
    df_effp91_zerob   = df.Filter("nbjets_R5_eff_p91 == 0");
    df_effp91_oneb    = df.Filter("nbjets_R5_eff_p91 == 1");
    df_effp91_twob    = df.Filter("nbjets_R5_eff_p91 > 1");
    
    df_effp89_zerob   = df.Filter("nbjets_R5_eff_p89 == 0");
    df_effp89_oneb    = df.Filter("nbjets_R5_eff_p89 == 1");
    df_effp89_twob    = df.Filter("nbjets_R5_eff_p89 > 1");
    
    ##amdf_BDT_zerobL  = df_zerobL.Filter("BDT_score > 0.5")
    ##amdf_BDT_onebL   = df_onebL.Filter("BDT_score > 0.5")
    ##amdf_BDT_zerobT  = df_zerobT.Filter("BDT_score > 0.5")
    ##amdf_BDT_onebT   = df_onebT.Filter("BDT_score > 0.5")

    
    for var in column_names:
        var = str(var)
        if "is" in var : continue
        if var.endswith("_phi"): binning = bins["phi"];
        elif 'nbjets' in var :  binning = bins["nbjets"]
        #elif 'R5_true' in var :  binning = bins["nbjets"]
        elif 'njets' in var :  binning = bins["njets"]
        elif "tagged" in var: binning = bins["tagged"] 
        elif var == 'ntau_h':            binning = bins["nleps"]
        elif var.endswith("_theta"): binning = bins["theta"]; 
        elif var.endswith("_p"): binning = bins["p"]; 
        #elif var.endswith("_isB") or var.endswith("_isG") or var.endswith("_isQ") or var.endswith("_isS") or var.endswith("_isC"): binning = bins["tagger"]; 
        #elif var in ['d_12', 'd_23', 'd_34', 'd_45', 'd_56']: binning = bins["dij"][var]; 
        elif 'BDT_score' in var: binning = bins["tagger"]; 
        else: 
            print('Default binning for variable {}'.format(var))
            binning = (100, -1, 100)

        results.append(df.Histo1D(("no_cut_"+var, "", *binning), var))
        results.append(df_effp9_zerob.Histo1D(('effp9_zerob_'     +var, "", *binning), var))
        results.append(df_effp9_oneb.Histo1D(('effp9_oneb_'       +var, "", *binning), var))
        results.append(df_effp91_zerob.Histo1D(('effp91_zerob_'   +var, "", *binning), var))
        results.append(df_effp91_oneb.Histo1D(('effp91_oneb_'     +var, "", *binning), var))
        results.append(df_effp89_zerob.Histo1D(('effp89_zerob_'   +var, "", *binning), var))
        results.append(df_effp89_oneb.Histo1D(('effp89_oneb_'     +var, "", *binning), var))
        results.append(df_effp89_twob.Histo1D(('effp89_twob_'     +var, "", *binning), var))
        results.append(df_effp9_twob.Histo1D(('effp9_twob_'       +var, "", *binning), var))
        results.append(df_effp91_twob.Histo1D(('effp91_twob_'     +var, "", *binning), var))
#        results.append(df_BDT_zerobL.Histo1D(('BDT_cut_zerobtagl_'+var, "", *binning), var))
#        results.append(df_BDT_onebL.Histo1D(('BDT_cut_onebtagl_'+var, "", *binning), var))
#        results.append(df_BDT_zerobT.Histo1D(('BDT_cut_zerobtagt_'+var, "", *binning), var))
#        results.append(df_BDT_onebT.Histo1D(('BDT_cut_onebtagt_'+var, "", *binning), var))



    return results, weightsum
