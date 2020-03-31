#!/usr/bin/env python
import sys


team_number = int(sys.argv[1])   #
score_init = sys.argv[2]         #

time_content = '|'.join(['0'] * (team_number * team_number))
score_content = '|'.join([score_init] * team_number)
open('/tmp/score.txt','w').write(score_content)
open('/tmp/time.txt','w').write(time_content)
open('/tmp/result.txt','w').write('')
