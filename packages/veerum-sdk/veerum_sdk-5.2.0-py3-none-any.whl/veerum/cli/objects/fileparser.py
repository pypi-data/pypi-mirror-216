import os
import pathlib
import mimetypes

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

def select_pano_files(root):
	if os.path.isfile(root):
		raise Exception('The path %s must be a folder containing Pano files' % (os.path.basename(root)))
	elif not os.path.isdir(root):
		raise Exception('Unrecognized path type %s' % root)
	for path, subdirs, files in os.walk(root):
		for name in files:
			fullpath = os.path.join(path, name)
			mime = mimetypes.guess_type(fullpath)[0]
			# todo implement in later versions
			#if (mime != 'image/jpeg'):
				# ignore non jpeg files
				#continue
			yield File(name, fullpath, mime, os.path.getsize(fullpath))

def validate_files(files):
	for file in files:
		if not os.path.exists(file.path):
			raise Exception()
		if not os.path.isfile(file.path):
			raise Exception()

		syspath = pathlib.Path(file.key)
		nixpath = pathlib.PurePosixPath(syspath)

		# This is here to fix a windows to unix path conversion issue
		file = file._replace(key=str(nixpath))

		yield file

def select_file(metadataPath, format):
	if not os.path.isfile(metadataPath):
		raise Exception('The path for metadata %s must be a file' % metadataPath)

	if (format == 'csv') & (metadataPath.endswith('.csv')):
		mime = 'text/csv'
	elif (format == 'json') & (metadataPath.endswith('.json')):
		mime = 'application/json'
	else:
		raise Exception('The path for metadata %s must be in %s format' % (metadataPath, format))
	return File(os.path.basename(metadataPath), metadataPath, mime, os.path.getsize(metadataPath))

def validate_file(file):
	if not os.path.exists(file.path):
		raise Exception()
	if not os.path.isfile(file.path):
		raise Exception()

	syspath = pathlib.Path(file.key)
	nixpath = pathlib.PurePosixPath(syspath)

	# This is here to fix a windows to unix path conversion issue
	file = file._replace(key=str(nixpath))

	return file

def as_posix_path(path_str):
	return pathlib.PureWindowsPath(path_str).as_posix()