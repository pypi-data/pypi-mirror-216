import os

from veerum.utils.helpers import File

def select_files(root):

	extensions = [
		'.json',
		'.b3dm',
		'.gltf',
		'.glb'
	]

	if os.path.isfile(root):
		if not os.path.basename(root).endswith('.json'):
			raise Exception('The base name %s does is not a json file' % (os.path.basename(root)))
		root = os.path.dirname(root)
	elif os.path.isdir(root):
		pass
	else:
		raise Exception('Unrecognized path type %s' % root)

	root_json = ''
	for filename in os.listdir(root):
		if filename.endswith('.json'):
			if root_json != '':
				raise Exception('Only one json file is allowed at the root of: %s' % (os.path.basename(root)))
			root_json = filename

	if root_json != '':
		yield File(root_json, os.path.join(root, root_json), 'application/json')
	else:
		raise Exception('A single json file is required at the root: %s for 3d-tiles' % (os.path.basename(root)))

	for file_root, _, filenames in os.walk(root):
		for filename in filenames:
			if(filename != root_json or file_root != root):
				split_file = os.path.splitext(filename)
				if split_file[1].lower() in extensions:
					if split_file[1] == '.json':
						content_type = 'application/json'
					else:
						content_type = 'application/octet-stream'
					full_path = os.path.join(file_root, filename)
					rel_path = os.path.relpath(full_path, root)
					yield File(rel_path, full_path, content_type)
