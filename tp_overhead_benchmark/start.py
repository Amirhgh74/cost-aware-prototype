import os
import sys
from subprocess import call 

build_tp = "gcc -c -I. empty-tp.c"
build_code = "gcc -c proto.c"
link = "gcc -o benchmark proto.o empty-tp.o -llttng-ust -ldl"
run = "./benchmark"

call(build_tp, shell=True)
call(build_code, shell=True)
call(link, shell=True)
call(run, shell=True)