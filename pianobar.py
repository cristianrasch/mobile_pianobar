import subprocess

class Wrapper(object):
  available_cmds = ('+', '-', 'e', 'i', 'n', 'p', 't', '(', ')')
  void_cmds = ('p', '(', ')')
  
  def __init__(self):
    self.proc = subprocess.Popen('pianobar', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  
  def run(self):  
    for i in range(6):
      line = self.proc.stdout.readline()
    return line.strip()
  
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
        res = [self.proc.stdout.readline().strip() for i in range(read)]
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
