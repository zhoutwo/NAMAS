import glob
import os
import sys

work_dir = sys.argv[1]
for n in glob.glob('%s*_eng' % work_dir):
    os.rename(n, '%s%s' % (work_dir, n[-len('NYT_eng'):-len('_eng')].upper()))
