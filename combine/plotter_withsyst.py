import ROOT,sys,optparse,os
import datetime
date = datetime.date.today().isoformat()
def if3(cond, iftrue, iffalse):
    return iftrue if cond else iffalse

fancyname={
    "jet1_p":"p(j^1)",
    "jet1_theta":"#theta(j^1)",
    "jet2_p":"p(j^2)",
    "jet2_theta":"#theta(j^2)",
    "lep_p":"p(l)",
    "lep_theta":"#theta(l)",
    "jet3_p":"p(j^3)",
    "jet3_theta":"#theta(j^3)",
    "jet4_p":"p(j^4)",
    "jet4_theta":"#theta(j^4)",        
    'singlebin': "N_{events}",
    'BDT_score': "BDT",
    "mbbar":"m_{b#barb}",
    "nbjets_R5_eff_p9" : "N_{bjets}",
    "njets_R5":"N_{jets}"}

nice_names={
    'had': "hadronic channel",
    'semihad': "semi-hadronic channel",
    'oneb':   "with N_{bjets} = 1  ",
    'zerob':  "with N_{bjets} = 0 ",
    'twob':   "with N_{bjets} > 1 ",
    'no_cut': "",
  }  

def drawSLatex(xpos,ypos,text,size):
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAlign(12)
    latex.SetTextSize(size)
    latex.SetTextFont(42)
    latex.DrawLatex(xpos,ypos,text)

def stackPlot(fname,vname,lumi,channel,ecm,useLog,showInt,nostack,sel):
    if ecm == "365":
        lumi_txt=f'{lumi/1e6:.1f}'
    else:     lumi_txt=f'{lumi/1e3:.1f}'
    Canv = ROOT.TCanvas(f'Canv_{channel}_{ecm}',"",600,600)
    Canv.Range(0,0,1,1);   Canv.SetFillColor(0);   Canv.SetBorderMode(0);   Canv.SetBorderSize(2);
    Canv.SetTickx(1);   Canv.SetTicky(1);   Canv.SetLeftMargin(0.16);   Canv.SetRightMargin(0.08);
    Canv.SetBottomMargin(0.13);   Canv.SetFrameFillStyle(0);   Canv.SetFrameBorderMode(0);
    pf=""    
    #legend = ROOT.TLegend(0.5 if showInt else 0.635,0.67,0.8 if showInt else  0.875,0.85);
    legend = ROOT.TLegend(0.65,0.63,0.9,0.78);
    legend.SetNColumns(1);legend.SetFillColor(0);legend.SetFillStyle(0); legend.SetShadowColor(0);   legend.SetLineColor(0);
    legend.SetTextFont(42);        legend.SetBorderSize(0);   legend.SetTextSize(0.035);
    hs=ROOT.THStack(f'hs_{channel}_{ecm}',""); 
    f_in=ROOT.TFile.Open(fname)
    h_sig=f_in.Get('x_sig');
    h_bkg=f_in.Get('x_bkg_%s'%channel);
    h_bkg1=f_in.Get(f'x_bkg1_{channel}') 
            
    h_bkg.SetDirectory(0);    h_sig.SetDirectory(0); h_bkg1.SetDirectory(0);
    if nostack:
        pf+="_nostack"
        h_sig.SetLineColor(ROOT.kAzure+1); 
        h_bkg.SetLineColor(ROOT.kOrange+1);
        h_bkg1.SetLineColor(ROOT.kRed);
    else:        
        h_sig.SetFillColor(ROOT.kAzure+1);  h_sig.SetLineColor(ROOT.kBlack)
        h_bkg.SetFillColor(ROOT.kOrange+1); h_bkg.SetLineColor(ROOT.kBlack)
        h_bkg1.SetFillColor(ROOT.kRed);    h_bkg1.SetLineColor(ROOT.kBlack)
            
    f_in.Close();

    if "BDT" not in vname:
        hs.Add(h_bkg1);
        hs.Add(h_sig);
        hs.Add(h_bkg);
    else:
        hs.Add(h_bkg);
        hs.Add(h_bkg1);
        hs.Add(h_sig);
            


    legend.AddEntry(h_sig,  'WbWb'+ (f"({h_sig.Integral():.2e})"  if showInt else ''),"F" if not nostack else 'l');
    legend.AddEntry(h_bkg,  'WW ' + (f"({h_bkg.Integral():.2e})"  if showInt else ''),"F" if not nostack else 'l');
    legend.AddEntry(h_bkg1, 'WWZ '+ (f"({h_bkg1.Integral():.2e})" if showInt else ''),"F" if not nostack else 'l');
    
    hs.Draw("HIST" if not nostack else 'nostackhist');
    hs.GetXaxis().SetTitle(xtitle)
    hs.GetYaxis().SetTitle("Events");
    hs.GetYaxis().SetLabelSize(0.04);    hs.GetYaxis().SetTitleSize(0.045);    hs.GetYaxis().SetTitleOffset(1.22);
    hs.GetXaxis().SetTitleSize(0.045);    hs.GetXaxis().SetTitleOffset(1.0); hs.GetXaxis().SetLabelSize(0.04);
    hs.GetYaxis().SetMaxDigits(3);
    hs.GetXaxis().SetTitleFont(42);        hs.GetYaxis().SetTitleFont(42);    
    t2a = drawSLatex(0.2,0.85,"#bf{FCC-ee} #it{Simulation (Delphes)}",0.04);
    t4a = drawSLatex(0.2,0.8,nice_names[channel]+" "+nice_names[sel],0.035);

    if ecm == "365":
        t3a = drawSLatex(0.64,0.915,"%s ab^{#minus1} (%s GeV)"%(lumi_txt,ecm),0.035);
    else:    
        t3a = drawSLatex(0.64,0.915,"%s fb^{#minus1} (%s GeV)"%(lumi_txt,ecm),0.035);


    morey=1.0
    hs.SetMinimum(1);
    if useLog:
        Canv.SetLogy();
        pf+='_log'
        morey=500
        if "single" in vname:
            morey=5000
        if ecm == "365":
            hs.SetMinimum(65);
        
    else:
        hs.SetMinimum(0.05);
        hs.GetYaxis().SetTitleOffset(1.25);
        morey=1.25 
        
    hs.SetMaximum(morey*hs.GetHistogram().GetMaximum()) 
    legend.Draw("same");
    
    Canv.Update();
    plotsdir=f"/eos/user/a/anmehta/www/FCC_top/{date}_paper"
    if not os.path.isdir(plotsdir):        os.system("mkdir %s"%plotsdir);  os.system('cp ~/public/index.php %s/'%plotsdir)

    Canv.Print(f"{plotsdir}/{vname}_{channel}_{ecm}{pf}.pdf")
    Canv.Print(f"{plotsdir}/{vname}_{channel}_{ecm}{pf}.png")
    return True

def getHist(isSig,proc,vname,h_name,xsec_sig,channel,ecm,lumi):
    sf=1.0;sumW=1.0;xsec=1.0;
    f_in=ROOT.TFile.Open(f'/eos/cms/store/cmst3/group/top/FCC_tt_threshold/output_condor_20241121_1142/WbWb/outputs/histmaker/{channel}/{proc}.root')
    print("looking for ",vname, "in \t",f_in.GetName())
    h_in=f_in.Get(vname).Clone(h_name);
    xsec=f_in.Get('crossSection').GetVal();
    sumW=f_in.Get('sumOfWeights').GetVal()
    if isSig:
        xsec=xsec_sig;
    N_tot=f_in.Get('eventsProcessed').GetVal()
    print('input ylds',h_in.Integral())
    sf=xsec*lumi/N_tot #sumW
    print("for process \t", proc,'\t',vname,'\t xsec is \t',xsec,'\t n_tot\t',N_tot,"\t lumi\t",lumi,"\t sf \t",sf)
    h_in.Scale(sf);    h_in.SetDirectory(0);    f_in.Close();
    #print('integral after scaling',h_in.Integral())
    return h_in

def cards(mkplots,lumi,xsec_sig,channel,sel,bWP,ecm,logy,vname,xtitle,showInt,nostack):
    h_sig=getHist(True,f'sig_vs_wwz/wzp6_ee_WbWb_ecm{ecm}',vname,"x_sig",xsec_sig,channel,ecm,lumi)
    vname_btagUp=vname.replace('p9','p91')
    vname_btagDown=vname.replace('p9','p89')

    print('checking these histograms', vname,vname_btagUp,vname_btagDown)

    h_sig_psUp=getHist(True,f'sig_vs_wwz/wzp6_ee_WbWb_PSup_ecm{ecm}',vname,"x_sig_psUp",xsec_sig,channel,ecm,lumi)
    h_sig_psDown=getHist(True,f'sig_vs_wwz/wzp6_ee_WbWb_PSdown_ecm{ecm}',vname,"x_sig_psDown",xsec_sig,channel,ecm,lumi)
    h_sig_btagUp=getHist(True,f'sig_vs_wwz_btagup/wzp6_ee_WbWb_ecm{ecm}',vname_btagUp,"x_sig_btagUp",xsec_sig,channel,ecm,lumi)
    h_sig_btagDown=getHist(True,f'sig_vs_wwz_btagdown/wzp6_ee_WbWb_ecm{ecm}',vname_btagDown,"x_sig_btagDown",xsec_sig,channel,ecm,lumi)

    h_sig_topmassUp=getHist(True,f'sig_vs_wwz/wzp6_ee_WbWb_mtop173p5_ecm{ecm}',vname,"x_sig_topmassUp",xsec_sig,channel,ecm,lumi)
    h_sig_topmassDown=getHist(True,f'sig_vs_wwz/wzp6_ee_WbWb_mtop171p5_ecm{ecm}',vname,"x_sig_topmassDown",xsec_sig,channel,ecm,lumi)
    

    #print('sig',h_sig.Integral())
    h_obs  = h_sig.Clone("x_data_obs")
    h_bkg  = getHist(False,f'sig_vs_wwz/p8_ee_WW_ecm{ecm}',vname,"x_bkg_%s"%channel,1.0,channel,ecm,lumi)
    
    #h_bkg_psUp      = getHist(False,f'sig_vs_wwz/p8_ee_WW_PSup_ecm{ecm}',vname,"x_bkg_%s_psUp"%channel,1.0,channel,ecm,lumi)
    #h_bkg_psDown    = getHist(False,f'sig_vs_wwz/p8_ee_WW_PSdown_ecm{ecm}',vname,"x_bkg_%s_psDown"%channel,1.0,channel,ecm,lumi)

    h_bkg_btagUp     = getHist(False,f'sig_vs_wwz_btagup/p8_ee_WW_ecm{ecm}',vname_btagUp,"x_bkg_%s_btagUp"%channel,1.0,channel,ecm,lumi)
    h_bkg_btagDown   = getHist(False,f'sig_vs_wwz_btagdown/p8_ee_WW_ecm{ecm}',vname_btagDown,"x_bkg_%s_btagDown"%channel,1.0,channel,ecm,lumi)
    h_obs.Add(h_bkg);
    

    h_bkg1           = getHist(False,f'sig_vs_wwz/wzp6_ee_WWZ_Zbb_ecm{ecm}',vname,f"x_bkg1_{channel}",1.0,channel,ecm,lumi)
    h_bkg1_btagUp    = getHist(False,f'sig_vs_wwz_btagup/wzp6_ee_WWZ_Zbb_ecm{ecm}',vname_btagUp,f"x_bkg1_{channel}_btagUp",1.0,channel,ecm,lumi)
    h_bkg1_btagDown  = getHist(False,f'sig_vs_wwz_btagdown/wzp6_ee_WWZ_Zbb_ecm{ecm}',vname_btagDown,f"x_bkg1_{channel}_btagDown",1.0,channel,ecm,lumi)
    h_obs.Add(h_bkg1)


    fout_name=f"rootfiles/{channel}_{sel}_{vname}_beffp{bWP}_{ecm}.root"
    f_out=ROOT.TFile(fout_name,"RECREATE");
    f_out.cd();
    #h_bkg_psUp.Write(); h_bkg_psDown.Write();
    h_sig_psUp.Write(); h_sig_psDown.Write();
    h_sig_topmassUp.Write(); h_sig_topmassDown.Write();
    h_bkg_btagUp.Write(); h_bkg_btagDown.Write();
    h_sig_btagUp.Write(); h_sig_btagDown.Write();
    h_bkg1.Write();h_bkg1_btagUp.Write();h_bkg1_btagDown.Write();
    
    h_sig.Write();    h_bkg.Write();
    h_obs.Write();    f_out.Close();
    if mkplots:
        stackPlot(fout_name,vname,lumi,channel,ecm,logy,showInt,nostack,sel)


if __name__ == '__main__':
    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)

    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('-c',  '--ch',       dest='channel',   type='string',         default='semihad',    	help='had/semihad')
    parser.add_option('-s',  '--sel',      dest='sel' ,      type='string',         default='no_cut',       	help='no_cut/effp9_twob/effp9_oneb/effp9_zerob')
    parser.add_option('-e',  '--ecm',      dest='ecm' ,      type='string',         default='345',        	help='ecm 340/345/365 (allthree backgrounds are simulated for these energy pts')
    parser.add_option('-w',  '--bwp',      dest='btagWP',    type='string',         default='9',      	        help='btagWP:nom(9)/up(91)/dn(89)')
    parser.add_option('-v',  '--vname',    dest='vname',     type='string',         default='njets_R5',         help='plot this variable')
    parser.add_option('-l',  '--lum',      dest='lum' ,      type=float,            default=41.0,         	help='lumi in fb')
    parser.add_option('-p',  '--plots',    dest='mkplots',   action='store_true',   default=False,        	help='make plots too')
    parser.add_option('-i',  '--sInt',     dest='showInt' ,  action='store_true',   default=False,        	help='show integral in legends')
    parser.add_option('--logy',            dest='logy' ,     action='store_true',   default=False,        	help='use log scale for y-axis')
    parser.add_option('--nostack',         dest='nostack' ,  action='store_true',   default=False,        	help='draw non-stacked plots with transparent fill style')

    (opts, args) = parser.parse_args()
    
    if opts.ecm == "365":
        lumi=2650*1000
    else:
        lumi=opts.lum*1000

    
    br_semihad=0.438
    br_had=0.457
    xsec_tt=0.1 if opts.ecm =="340" else 0.5
    xsec_sig=xsec_tt #*(br_semihad if "semihad" in opts.channel else br_had)
    hname=opts.sel+"_"+opts.vname
    if "no_cut" not in opts.sel:
        hname="effp"+opts.btagWP+"_"+opts.sel+"_"+opts.vname

    #print(opts.vname,hname)
    
    xtitle= fancyname[opts.vname] #"N_{bjets}" if "nbjets" in opts.vname else "N_{jets}"

    cards(opts.mkplots,lumi,xsec_sig,opts.channel,opts.sel,opts.btagWP,opts.ecm,opts.logy,hname,xtitle,opts.showInt,opts.nostack)



