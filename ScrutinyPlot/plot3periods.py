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
	infile = open(sys.argv[filnum], "r")
	for inline in infile:
		entries = inline.split(",")
		# print entries
		if len(entries[1]) > 0 and len(entries[4]) > 0 :
			szintb = float(entries[1]) / 1024.0 / 1024.0 / 1024.0 / 1024.0
			histo.Fill(float(entries[4]), szintb)
	infile.close()


scrutplot1 = ROOT.TH1F ("scrutiny1", "Dataset Usage for June 16 - December 9, 2017", 15, 0.0, 15.0)
scrutplot2 = ROOT.TH1F ("scrutiny2", "", 15, 0.0, 15.0)
scrutplot3 = ROOT.TH1F ("scrutiny3", "", 15, 0.0, 15.0)
scrutplot1.SetStats(0)
scrutplot2.SetStats(0)
scrutplot3.SetStats(0)
FillHisto(1, scrutplot1)
FillHisto(2, scrutplot2)
FillHisto(3, scrutplot3)
scrutplot1.GetXaxis().SetTitle("Number of Accesses");
scrutplot1.GetYaxis().SetTitle("Aggregated Data Size [TB]");
scrutplot1.SetNdivisions(15, "X")
c1 = ROOT.TCanvas()
gStyle.SetHistFillColor(49)
c1.SetGrid()
c1.SetLogy()
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
legend = ROOT.TLegend(0.5, 0.6, 0.9, 0.9)
legend.SetHeader("Dataset Accesses over Period","C")
legend.AddEntry(scrutplot1, "Full period", "f")
legend.AddEntry(scrutplot2, "Last 3 months", "f")
legend.AddEntry(scrutplot3, "Last 1 month", "f")
legend.Draw()
c1.Print ("scrut136.png")
