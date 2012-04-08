import subprocess
import re

class Wrapper(object):
  available_cmds = ('+', '-', 'n', 'p', '(', ')', 'help')
  void_cmds = ('p', '(', ')')
  
  def __init__(self):
    self.proc = subprocess.Popen('pianobar', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    self.regex = re.compile(r'\A\w')
  
  def sanitize(self, string):
    if re.match(self.regex, string):
      return string
    else:
      idx = string.find('|>')
      if idx == -1:
        idx = string.find('(i)')
      return string[idx:]
  
  def read_from_pianobar(self, how_many = 1):
    lines = [self.proc.stdout.readline().strip() for i in range(how_many)]
    return map(self.sanitize, lines)
  
  def run(self):
    return self.read_from_pianobar(6)
  
  def isvoid(self, cmd):
    return cmd in self.void_cmds
  
  def execute(self, command):
    if command in self.available_cmds:
      if command == 'help':
        cmd, read = '?', 23
      else:
        cmd = command
        read = 0 if self.isvoid(cmd) else 1
      
      self.proc.stdin.write(cmd)
      
      if read:
        res = self.read_from_pianobar(read)
      else:
        res = ['Cmd executed: %s' % cmd]
    else:
      res = ['Command not found. Available commands:', str(self.available_cmds)]
    
    return res

  def __del__(self):
    self.proc.stdin.write('q')
    self.proc.wait()

#	+    love song
#	-    ban song
#	a    add music to station
#	c    create new station
#	d    delete station
#	e    explain why this song is played
#	g    add genre station
#	h    song history
#	i    print information about song/station
#	j    add shared station
#	m    move song to different station
#	n    next song
#	p    pause/continue
#	q    quit
#	r    rename station
#	s    change station
#	t    tired (ban song for 1 month)
#	u    upcoming songs
#	x    select quickmix stations
#	b    bookmark song/artist
#	(    decrease volume
#	)    increase volume
#	=    delete seeds/feedback
