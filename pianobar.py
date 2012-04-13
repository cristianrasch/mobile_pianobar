import re
import subprocess
import tempfile
import time

class Wrapper(object):
  _available_cmds = ('+', '-', 'n', 'p', '(', ')', 'help')
  _void_cmds = ('p', '(', ')')
  
  def __init__(self):
    self.starts_with_a_cap_letter_regex = re.compile(r'\A[A-Z]')
    self.sanitize_regex = re.compile(r'[\s|"]\w')
    self.buffer = tempfile.TemporaryFile('r+', prefix='pianobar', suffix='.log')
    self.pos = 0
    self.proc = subprocess.Popen('pianobar', stdin=subprocess.PIPE, stdout=self.buffer)
    time.sleep(10)
    
  def run(self):
    return self._read_from_pianobar()
  
  def execute(self, command):
    if True: #command in self._available_cmds or command.isdigit():
      cmd = command+'\n' if command.isdigit() else command
      self.proc.stdin.write(cmd)
      
      if self._isvoid(command):
        res = ['Cmd executed: %s' % command]
      else:
        time.sleep(3)
        res = self._read_from_pianobar()
    else:
      res = ['Command not found. Available commands:', str(self.available_cmds)]
    
    return res
    
  def _sanitize(self, string):
    if re.match(self.starts_with_a_cap_letter_regex, string):
      return string.strip()
    else:
      match = re.search(self.sanitize_regex, string)
      if match: return string[match.start():].strip()
  
  def _read_from_pianobar(self):
    self.buffer.seek(self.pos)
    lines = self.buffer.readlines()
    self.pos = self.buffer.tell()
    sanitized_lines = map(self._sanitize, lines)
    return filter(lambda x: x, sanitized_lines)
    
  def _isvoid(self, cmd):
    return cmd in self._void_cmds
  
  def __del__(self):
    self.proc.stdin.write('q')
    # self.proc.wait()
    self.buffer.close()

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
