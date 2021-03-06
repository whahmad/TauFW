#! /usr/bin/env python
# Author: Izaak Neutelings (May 2020)
# Description: Simple create mutau events
from ROOT import TFile, TTree, TH1D
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class ModuleMuTauSimple(Module):
  
  def __init__(self,fname):
    self.outfile  = TFile(fname,'RECREATE')
    self.tree     = TTree('tree','tree')
    self.cutflow  = TH1D('cutflow', 'cutflow',25,0,25)
    self.cut_none = 0
    self.cut_muon = 1
    self.cut_tau  = 2
    self.cut_pair = 3
    self.cutflow.GetXaxis().SetBinLabel(1+self.cut_none, "no cut" )
    self.cutflow.GetXaxis().SetBinLabel(1+self.cut_muon, "muon"   )
    self.cutflow.GetXaxis().SetBinLabel(1+self.cut_tau,  "tau"    )
    self.cutflow.GetXaxis().SetBinLabel(1+self.cut_pair, "pair"   )
  
  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    """Create branches in output tree."""
    self.pt_1  = np.zeros(1,dtype='f')
    self.eta_1 = np.zeros(1,dtype='f')
    self.iso_1 = np.zeros(1,dtype='f')
    self.pt_2  = np.zeros(1,dtype='f')
    self.eta_2 = np.zeros(1,dtype='f')
    self.iso_2 = np.zeros(1,dtype='f')
    self.m_vis = np.zeros(1,dtype='f')
    self.tree.Branch('pt_1',  self.pt_1,  'pt_1/F')
    self.tree.Branch('eta_1', self.eta_1, 'eta_1/F')
    self.tree.Branch('iso_1', self.iso_1, 'iso_1/F')
    self.tree.Branch('pt_2',  self.pt_2,  'pt_2/F')
    self.tree.Branch('eta_2', self.eta_2, 'eta_2/F')
    self.tree.Branch('iso_2', self.iso_2, 'iso_2/F')
    self.tree.Branch('m_vis', self.m_vis, 'm_vis/F')
  
  def endJob(self):
    self.outfile.Write()
    self.outfile.Close()
  
  def analyze(self, event):
    """Process event, return True (pass, go to next module) or False (fail, go to next event)."""
    self.cutflow.Fill(self.cut_none)
    
    # SELECT MUON
    muons = [ ]
    for muon in Collection(event,'Muon'):
      if muon.pt<20: continue
      if abs(muon.eta)>2.4: continue
      if abs(muon.dz)>0.2: continue
      if abs(muon.dxy)>0.045: continue
      if not muon.mediumId: continue
      if muon.pfRelIso04_all>0.50: continue
      muons.append(muon)
    if len(muons)<1: return False
    muon = max(muons,key=lambda p: p.pt)
    self.cutflow.Fill(self.cut_muon)
    
    # SELECT TAU
    taus = [ ]
    for tau in Collection(event,'Tau'):
      if tau.pt<20: continue
      if abs(tau.eta)>2.4: continue
      if abs(tau.dz)>0.2: continue
      taus.append(tau)
    if len(taus)<1: return False
    tau = max(taus,key=lambda p: p.pt)
    self.cutflow.Fill(self.cut_tau)
    
    # PAIR
    if muon.DeltaR(tau)<0.4: return False
    self.cutflow.Fill(self.cut_pair)
    
    # SAVE VARIABLES
    self.pt_1[0]  = muon.pt
    self.eta_1[0] = muon.eta
    self.iso_1[0] = muon.pfRelIso04_all
    self.pt_2[0]  = tau.pt
    self.eta_2[0] = tau.eta
    self.iso_2[0] = tau.rawIso
    self.m_vis[0] = (muon.p4()+tau.p4()).M()
    self.tree.Fill()
    
    return True
