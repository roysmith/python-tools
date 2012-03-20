import re
from pprint import pprint
from os.path import basename

def unfold(raw_log_line):
    """Take a raw syslog line and unfold all the multiple levels of
    newline-escaping that have been inflicted on it by various things.
    Things that got python-repr()-ized, have '\n' sequences in them.
    Syslog itself looks like it uses #012.

    """
    lines = raw_log_line \
            .replace('#012', '\n') \
            .replace('\\n', '\n') \
            .splitlines()
    return lines


# Example of a line containing a stack frame:
# File "/home/songza/deploy/current/scrobble/scrobble_mill.py", line 115, in listen'
frame_pattern = re.compile(r'^ *File "(?P<path>[^"]+)", line (?P<line>\d+), in (?P<function>\w+)')

def extract_stack(lines):
    """Parse a python stack trace out of a sequence of lines.

    Lines would most commonly be the list returned by unfold(), but
    could be from some other source.

    Returns a (header, stack) tuple.  The header is just the first
    line (which often contains information useful to a human).  The
    stack is a list of (path, function) tuples, where path is the
    pathname of the python source file and function is the name of the
    function in the stack frame.  For example, a stack might be:

    [('/usr/lib/pymodules/python2.6/django/core/handlers/base.py', 'get_response'),
     ('/home/songza/deploy/rel-2012-03-19/djsite/djfront/views.py', 'song_info'),
     ('/home/songza/deploy/rel-2012-03-19/djsite/djfront/api.py', 'get_song'),
     ('/home/songza/deploy/rel-2012-03-19/djsite/djfront/api.py', 'api')]

    """
    header = lines[0]
    stack = []
    for line in lines:
        m = frame_pattern.match(line)
        if not m:
            continue
        frame = (m.group('path'), m.group('function'))
        stack.append(frame)
    return (header, stack)
