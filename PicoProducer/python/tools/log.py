# Author: Izaak Neutelings (May 2020)

tcol_dict = { 'black':  30,  'red':     31, 'green': 32,
              'yellow': 33,  'orange':  33, 'blue':  34,
              'purple': 35,  'magenta': 36, 'white': 37,
              'grey':   90,  'none':     0 }
bcol_dict = {k: (10+v if v else v) for k,v in tcol_dict.iteritems()}
def color(string,c='green',b=False,**kwargs):
  tcol_key   = kwargs.get('color',     c     )
  bcol_key   = kwargs.get('background','none')
  bold_code  = "\033[1m" if kwargs.get('bold',b) else ""
  tcol_code  = "\033[%dm"%tcol_dict[tcol_key] if tcol_key!='none' else ""
  bcol_code  = "\033[%dm"%bcol_dict[bcol_key] if bcol_key!='none' else ""
  stop_code  = "\033[0m"
  reset_code = stop_code if kwargs.get('reset',False) else ""
  return kwargs.get('pre',"") + reset_code + bcol_code + bold_code + tcol_code + string + stop_code
  

def warning(string,**kwargs):
  return color(kwargs.get('exclam',"Warning! ")+string, color="yellow", bold=True, pre=kwargs.get('pre',">>> "))
  

def error(string,**kwargs):
  return color(kwargs.get('exclam',"ERROR! ")+string, color="red", bold=True, pre=kwargs.get('pre',">>> "))
  

def green(string,**kwargs):
  return "\033[32m%s\033[0m"%string
  

def error(string,**kwargs):
  print ">>> \033[1m\033[91m%sERROR! %s\033[0m"%(kwargs.get('pre',""),string)
  

def warning(string,**kwargs):
  print ">>> \033[1m\033[93m%sWarning!\033[0m\033[93m %s\033[0m"%(kwargs.get('pre',""),string)
  

def bold(string):
  return "\033[1m%s\033[0m"%(string)
  

#_headeri = 0
def header(*strings):
  #global _headeri
  title  = ', '.join([str(s).lstrip('_') for s in strings if s])
  string = "\n" +\
           "   ###%s\n"    % ('#'*(len(title)+3)) +\
           "   #  %s  #\n" % (title) +\
           "   ###%s\n"    % ('#'*(len(title)+3))
  #_headeri += 1
  return string
  


class Logger(object):
  """Class to customly log program."""
  
  def __init__(self, name="LOG", verb=0, **kwargs):
    self.name      = name
    self.verbosity = verb
    self.pre       = kwargs.get('pre',">>> ")
    self._table    = None
    if  kwargs.get('showname',False):
      self.pre += self.name + ": "
  
  def getverb(self,*args):
    """Decide verbosity level based on maximum of own verbosity and given arguments."""
    verbs = [ self.verbosity ]
    for arg in args:
      if isinstance(arg,dict):
        verbosity = arg.get('verb',0) + arg.get('verbosity',0) + 0
      else:
        verbosity = int(bool(arg) or 0)
      verbs.append(verbosity)
    return max(verbs)
  
  def info(self,string,**kwargs):
    """Info"""
    print self.pre+string
  
  def color(self,*args,**kwargs):
    """Print color."""
    print self.pre+color(*args,**kwargs)
  
  def warning(self,string,trigger=True,**kwargs):
    """Print warning if triggered."""
    if trigger:
      exclam  = color(kwargs.get('exclam',"Warning! "),'yellow',b=True,pre=self.pre+kwargs.get('pre',""))
      message = color(string,'yellow',pre="")
      print exclam+message
  
  def title(self,*args,**kwargs):
    print header(*args,**kwargs)
  
  def header(self,*args,**kwargs):
    print header(*args,**kwargs)
  
  def error(self,string,trigger=True,**kwargs):
    """Print error if triggered without throwing an exception."""
    if trigger:
      exclam  = color(kwargs.get('exclam',"ERROR! "),'red',b=True,pre=self.pre+kwargs.get('pre',""))
      message = color(string,'red',pre="")
      print exclam+message
    return trigger
  
  def fatal(self,string,trigger=True,**kwargs):
    """Fatal error by throwing an exception."""
    return self.throw(Exception,string,trigger=trigger,**kwargs)
  
  def throw(self,error,string,trigger=True,**kwargs):
    """Fatal error by throwing a specified exception."""
    if trigger:
      string = color(string,'red',**kwargs)
      raise error(string)
    return trigger
  
  def insist(self,condition,string,error=AssertionError,**kwargs):
    """Assert condition throwing an exception."""
    return self.throw(error,string,trigger=(not condition),**kwargs)
  
  def verbose(self,string,verb=None,level=1,**kwargs):
    """Check verbosity and print if verbosity level is matched."""
    if verb==None:
      verb   = self.verbosity
    if verb>=level:
      pre = self.pre+kwargs.get('pre',"")
      print pre+string
      return True
    return False
  
  def verb(self,*args,**kwargs):
    return self.verbose(*args,**kwargs)
  
  #def table(self,format,**kwargs):
  #  """Initiate new table."""
  #  self._table = Table(format)
  #
  #def theader(self,*args):
  #  """Print header of table."""
  #  self._table.header(*args)
  #
  #def row(self,*args):
  #  """Print row of table."""
  #  self._table.row(*args)
  

