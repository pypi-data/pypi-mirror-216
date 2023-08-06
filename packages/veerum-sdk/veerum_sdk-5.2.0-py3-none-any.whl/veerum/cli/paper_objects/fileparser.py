import os
from veerum.utils.helpers import File

def select_files(root, format):
	if os.path.isfile(root):
		raise Exception('The path %s must be a folder containing %s files' % (os.path.basename(root), format))
	elif not os.path.isdir(root):
		raise Exception('Unrecognized path type %s' % root)

	for file in os.listdir(root):
		if (format == 'csv') & (file.endswith('.csv')):
			mime = 'text/csv'
		elif (format == 'json') & (file.endswith('.json')):
			mime = 'application/json'
		else:  # ignore all others
			continue
		fullpath = os.path.join(root, file)
		yield File(file, fullpath, mime, os.path.getsize(fullpath))