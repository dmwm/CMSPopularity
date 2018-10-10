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
  sumpb = 0
  with open(sys.argv[filnum], "r") as infile :
    for inline in infile :
      entries = inline.split(",")
      # print entries
      dsSize = entries[1]
      if len(dsSize) > 0 and len(entries[2]) > 0 :
        numUses = float(entries[2])
	if numUses > 0.0 and numUses < 1.0 :
	  numUses = 1.0
        szinpb = float(dsSize) / 1024.0 / 1024.0 / 1024.0 / 1024.0 / 1024.0
	if numUses > 0.0 :
	  numUses = int(numUses + 0.5)
        sumpb = sumpb + szinpb
        if numUses > (numBins - 2) :
          numUses = (numBins - 2)
	# factor = numUses
	# if factor <= 0.0:
	  # factor = 1.0
	# else :
	  # numUses = numUses + 0.9999
        binNum = histo.Fill(numUses, szinpb)
  return sumpb


ext = 'png' if len(sys.argv) == 4 else sys.argv[4]
title = 'Dataset usage' if len(sys.argv) == 5 else sys.argv[5]
print("Use '%s' title in plots" % title)
numBins = 17
scrutplot1 = ROOT.TH1F ("scrutiny1", title, numBins, -1.0, float(numBins - 1))
scrutplot2 = ROOT.TH1F ("scrutiny2", title, numBins, -1.0, float(numBins - 1))
scrutplot3 = ROOT.TH1F ("scrutiny3", title, numBins, -1.0, float(numBins - 1))
scrutplot1.SetStats(0)
scrutplot2.SetStats(0)
scrutplot3.SetStats(0)
sum1 = FillHisto(1, scrutplot1)
sum2 = FillHisto(2, scrutplot2)
sum3 = FillHisto(3, scrutplot3)
# for binNum in range(0, numBins ) :
  # print "bin ", binNum, ", plot 3", scrutplot3.GetBinContent(binNum), "| ",
c1 = ROOT.TCanvas()
c1.SetGrid()
scrutplot3.GetXaxis().SetTitle("Number of Accesses");
scrutplot3.GetYaxis().SetTitle("Aggregated Data Size [PB]");
scrutplot3.SetNdivisions(numBins, "X")
for binNum in range(0, numBins - 2) :
  binNumStr = str(binNum)
  scrutplot3.GetXaxis().SetBinLabel(binNum + 2, binNumStr);
scrutplot3.GetXaxis().SetBinLabel(1, "0-old");
scrutplot3.GetXaxis().SetBinLabel(numBins, ">14");
scrutplot1.SetFillColor(4)
scrutplot1.SetBarWidth(0.3)
scrutplot2.SetFillColor(8)
scrutplot2.SetBarOffset(0.3)
scrutplot2.SetBarWidth(0.3)
scrutplot3.SetFillColor(2)
scrutplot3.SetBarWidth(0.3)
scrutplot1.SetBarOffset(0.6)
scrutplot3.Draw("hist b")
scrutplot2.Draw("hist b same")
scrutplot1.Draw("hist b same")
legend = ROOT.TLegend(0.4, 0.6, 0.8, 0.9)
legend.SetHeader("Dataset Accesses over Period","C")
legstr3 = "Last 3 months -- sum=" + "%.3g PB" % sum3
legstr2 = "Last 6 months -- sum=" + "%.3g PB" % sum2
legstr1 = "Last 12 months -- sum=" + "%.3g PB" % sum1
legend.AddEntry(scrutplot3, legstr3, "f")
legend.AddEntry(scrutplot2, legstr2, "f")
legend.AddEntry(scrutplot1, legstr1, "f")
legend.Draw()
c1.Print("scrutlinear.%s" % ext)
c1.SetLogy()
scrutplot3.Draw("hist b")
scrutplot2.Draw("hist b same")
scrutplot1.Draw("hist b same")
legend.Draw()
c1.Print("scrutlog.%s" % ext)
