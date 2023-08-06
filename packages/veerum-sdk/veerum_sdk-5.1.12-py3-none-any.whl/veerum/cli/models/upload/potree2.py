import os

from veerum.utils.helpers import File

def select_files(root):
	if os.path.isfile(root):
		if os.path.basename(root) != 'metadata.json':
			raise Exception('The base name is %s not metadata.json' % (os.path.basename(root)))
		root = os.path.dirname(root)
	elif os.path.isdir(root):
		pass
	else:
		raise Exception('Unrecognized path type %s' % root)

	path_metadata_json = os.path.join(root, 'metadata.json')
	yield File('metadata.json', path_metadata_json, 'application/json')

	path_hierarchy_bin = os.path.join(root, 'hierarchy.bin')
	yield File('hierarchy.bin', path_hierarchy_bin, 'application/octet-stream')

	path_octree_bin = os.path.join(root, 'octree.bin')
	yield File('octree.bin', path_octree_bin, 'application/octet-stream')
