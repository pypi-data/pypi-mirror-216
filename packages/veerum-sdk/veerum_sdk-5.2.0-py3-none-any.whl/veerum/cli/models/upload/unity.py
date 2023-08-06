import os
import json

from veerum.utils.helpers import File

# TODO: {KL} This whole thing needs better error handling
def select_files(root):
	if os.path.isfile(root):
		if os.path.basename(root) != 'bounds.json':
			raise Exception('The base name is %s not bounds.json' % (os.path.basename(root)))
		root = os.path.dirname(root)
	elif os.path.isdir(root):
		pass
	else:
		raise Exception('Unrecognized path type %s' % root)

	path_bounds_json = os.path.join(root, 'bounds.json')
	if not (os.path.exists(path_bounds_json) and os.path.isfile(path_bounds_json)):
		raise Exception('bounds.json is missing or not a readable file')
	with open(path_bounds_json, 'r') as file:
		bounds_json = json.load(file)

	voxel_chunks = bounds_json.get('voxelChunks', None)
	if voxel_chunks is None:
		raise Exception()
	if not isinstance(voxel_chunks, list):
		raise Exception()

	yield File('bounds.json', path_bounds_json, 'application/javascript')

	yield from voxel_files('CAD', root, 'application/octet-stream')

	for voxel_chunk in voxel_chunks:
		voxel_name = voxel_chunk.get('voxelName', None)
		if voxel_name is None:
			raise Exception()

		yield from voxel_files(voxel_name, root, 'application/octet-stream')

def voxel_files(name, path, mimetype):
	voxel_path = os.path.join(path, name)
	yield File(name, voxel_path, 'application/octet-stream')

	manifest = '{name:s}.manifest'.format(name=name)
	manifest_path = os.path.join(path, manifest)

	yield File(manifest, manifest_path, 'application/octet-stream')
