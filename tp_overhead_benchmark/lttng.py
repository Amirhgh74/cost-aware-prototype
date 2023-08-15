import os
import sys
from subprocess import call 

start = "lttng create my-user-space-session"
enable = "lttng enable-event --userspace --all"
run = "lttng start"

call(start, shell=True)
call(enable, shell=True)
call(run, shell=True)