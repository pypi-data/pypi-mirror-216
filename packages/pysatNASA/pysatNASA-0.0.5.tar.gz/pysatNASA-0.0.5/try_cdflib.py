import time

import pysat

num_tests = 10

inst = pysat.Instrument('timed', 'saber',
                        use_header=True)

t0 = time.time()
for date in inst.files.files.index[:num_tests]:
    inst.load(date=date)

t1 = time.time()

print('{:} tests, {:} s / test'.format(num_tests, (t1-t0)/num_tests))
