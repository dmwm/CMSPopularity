# Takes three file names, for full period, half of period, and fraction of period

import ROOT
import sys
from DataFormats.FWLite import Events, Handle
from ROOT import gStyle

# Make VarParsing object
# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#VarParsing_Example
# from FWCore.ParameterSet.VarParsing import VarParsing
# options = VarParsing ('python')
# options.parseArguments()

def FillHisto(filnum, histo):
  with open(sys.argv[filnum], "r") as infile :
    for inline in infile :
      entries = inline.split(",")
      # print entries
      dsSize = entries[2]
      if len(dsSize) > 0 and len(entries[1]) > 0 :
        numUses = int(entries[1])
        szinpb = float(dsSize) / 1024.0 / 1024.0 / 1024.0 / 1024.0 / 1024.0
        if numUses > (numBins - 2) :
          numUses = (numBins - 2)
	# factor = numUses
	# if factor <= 0.0:
	  # factor = 1.0
	# else :
	  # numUses = numUses + 0.9999
        binNum = histo.Fill(numUses, szinpb)


numBins = 17
scrutplot1 = ROOT.TH1F ("scrutiny1", "Dataset Usage for June 16 - December 9, 2017", numBins, -1.0, float(numBins - 1))
scrutplot2 = ROOT.TH1F ("scrutiny2", "", numBins, -1.0, float(numBins - 1))
scrutplot3 = ROOT.TH1F ("scrutiny3", "", numBins, -1.0, float(numBins - 1))
scrutplot1.SetStats(0)
scrutplot2.SetStats(0)
scrutplot3.SetStats(0)
FillHisto(1, scrutplot1)
FillHisto(2, scrutplot2)
FillHisto(3, scrutplot3)
# for binNum in range(0, numBins ) :
  # print "bin ", binNum, ", plot 3", scrutplot3.GetBinContent(binNum), "| ",
scrutplot1.GetXaxis().SetTitle("Number of Accesses");
scrutplot1.GetYaxis().SetTitle("Aggregated Data Size [PB]");
scrutplot1.SetNdivisions(numBins, "X")
for binNum in range(0, numBins - 2) :
  binNumStr = str(binNum)
  scrutplot1.GetXaxis().SetBinLabel(binNum + 2, binNumStr);
scrutplot1.GetXaxis().SetBinLabel(1, "0-old");
scrutplot1.GetXaxis().SetBinLabel(numBins, ">14");
c1 = ROOT.TCanvas()
gStyle.SetHistFillColor(49)
c1.SetGrid()
scrutplot1.SetFillStyle(3001)
scrutplot1.SetFillColor(49)
scrutplot1.SetBarWidth(0.3)
scrutplot1.Draw("hist b")
scrutplot2.SetFillColor(55)
scrutplot2.SetBarOffset(0.3)
scrutplot2.SetBarWidth(0.3)
scrutplot2.Draw("hist b same")
scrutplot3.SetFillColor(65)
scrutplot3.SetBarWidth(0.3)
scrutplot3.SetBarOffset(0.6)
scrutplot3.Draw("hist b same")
legend = ROOT.TLegend(0.4, 0.6, 0.7, 0.9)
legend.SetHeader("Dataset Accesses over Period","C")
legend.AddEntry(scrutplot1, "Full period", "f")
legend.AddEntry(scrutplot2, "Last 3 months", "f")
legend.AddEntry(scrutplot3, "Last 1 month", "f")
legend.Draw()
c1.Print ("scrutlinear.png")
c1.SetLogy()
scrutplot1.Draw("hist b")
scrutplot2.Draw("hist b same")
scrutplot3.Draw("hist b same")
legend.Draw()
c1.Print ("scrutlog.png")
