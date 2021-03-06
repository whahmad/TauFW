# Author: Izaak Neutelings (April 2020)
import os, re
from TauFW.PicoProducer.tools.utils import execute
from TauFW.PicoProducer.batch.BatchSystem import BatchSystem


class HTCondor(BatchSystem):
  # https://research.cs.wisc.edu/htcondor/manual/quickstart.html
  # https://twiki.cern.ch/twiki/bin/view/ABPComputing/LxbatchHTCondor
  
  def __init__(self,verb=False):
    super(HTCondor,self).__init__(verb=verb)
    # http://pages.cs.wisc.edu/~adesmet/status.html
    self.statusdict = { 'q': ['1'], 'r': ['2','3'], 'f': ['4','5','6'], 'c': ['5'] }
    self.jobidrexp  = re.compile("submitted to cluster (\d+).")
  
  def submit(self,script,**kwargs):
    """Submit a script with some optional parameters."""
    #jobname   = kwargs.get('name',  'job'           )
    #queue     = kwargs.get('queue', 'microcentury'  )
    appcmds   = kwargs.get('app',   [ ]            )
    options   = kwargs.get('opt',   None           )
    queue     = kwargs.get('queue', None           )
    name      = kwargs.get('name',  None           )
    dry       = kwargs.get('dry',   False          )
    verbosity = kwargs.get('verb',  self.verbosity )
    failflags = ["no jobs queued"]
    jobids    = [ ]
    subcmd    = "condor_submit"
    if not isinstance(appcmds,list):
      appcmds = [appcmds]
    if name:
      subcmd += " -batch-name %s"%(name)
    if options:
      subcmd += " "+options
    for appcmd in appcmds:
      subcmd += " -append %s"%(appcmd)
    subcmd += " "+script
    if queue:
      subcmd += " -queue %s"%(queue)
    out = self.execute(subcmd,dry=dry,verb=verbosity)
    fail = False
    for line in out.split(os.linesep):
      if any(f in line for f in failflags):
        fail = True
      matches = self.jobidrexp.findall(line)
      for match in matches:
        jobids.append(int(match))
    if fail:
      print ">>> Warning! Submission failed!"
      print out
    jobid = jobids[0] if len(jobids)==1 else jobids if len(jobids)>1 else 0
    return jobid
  
  def queue(self,job,**kwargs):
    """Get queue status."""
    qcmd  = "condor_q"
    return self.execute(qcmd)
  
  def status(self,job,**kwargs):
    """Check status of queued or running jobs."""
    jobid   = str(job.jobid)
    if job.taskid>=0:
      jobid+= '.%s'%job.taskid
    quecmd  = "condor_q -wide %s"%(jobid)
    return self.execute(quecmd)
  
  def jobs(self,jobids=[],**kwargs):
    """Get job status, return JobList object."""
    if not isinstance(jobids,list):
      jobids  = [jobids]
    verbosity = kwargs.get('verb', self.verbosity )
    quecmd    = "condor_q"
    for jobid in jobids:
      quecmd += " "+str(jobid)
    quecmd   += " -format '%s ' Owner -format '%s ' ClusterId -format '%s ' ProcId -format '%s ' JobStatus -format '%s\n' Args" # user jobid taskid status args
    rows      = self.execute(quecmd,verb=verbosity)
    return self.parsejobs(rows)
  
