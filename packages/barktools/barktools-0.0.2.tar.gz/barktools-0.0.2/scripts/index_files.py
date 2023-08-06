# Script to rename multiple files in a directory to numerically indexed filenames
  
import os 
import sys
import argparse

from barktools.base_utils import find_nbr_of_files

# Parse arguments

def index_files(target_dir, extension, n_leading_zeros=6):
	i = 0 
	n_files = find_nbr_of_files(target_dir, extension)
	for filename in os.listdir(target_dir): 
		if filename.endswith(extension):
		    dst = str(i).zfill(n_leading_zeros) + '.' +  extension
		    src = os.path.join(target_dir, filename) 
		    dst = os.path.join(target_dir, dst)
		    os.rename(src, dst) 
		    i += 1
		    sys.stdout.write("\rProcessed {}/{} files.".format(i, n_files))
	print()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--directory', '-d', help='Directory in which to rename files')
	parser.add_argument('--leading_zeros', '-n', help='Number of leading zeros in filename', default=6)
	parser.add_argument('--extension', '-e', help='Extension of file')
	args = parser.parse_args()
	target_dir = args.directory
	n_leading_zeros = int(args.leading_zeros)
	extension = args.extension

	index_files(target_dir, extension, n_leading_zeros)

if __name__ == '__main__':
	main()