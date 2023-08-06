import os

from veerum.utils.helpers import File

def select_files(root):
	if os.path.isfile(root):
		raise Exception('The path %s must be a folder containing CSV files' % (os.path.basename(root)))
	elif not os.path.isdir(root):
		raise Exception('Unrecognized path type %s' % root)

	for file in os.listdir(root):
		if file.endswith('.csv'):
			mime = 'text/csv'
		else:  # ignore all others
			continue
		fullpath = os.path.join(root, file)
		yield File(file, fullpath, mime, os.path.getsize(fullpath))
