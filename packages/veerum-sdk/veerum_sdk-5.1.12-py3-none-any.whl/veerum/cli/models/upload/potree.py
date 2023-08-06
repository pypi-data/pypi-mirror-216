import io
import os
import json
import struct

from collections import deque, namedtuple

from veerum.utils.helpers import File


OctreeNode = namedtuple('OctreeNode', [
	'key',
	'name',
	'depth',
	'children'
])

# TODO: {KL} This whole thing needs better error handling
def select_files(root):
	if os.path.isfile(root):
		if os.path.basename(root) != 'cloud.js':
			raise Exception('The base name is %s not cloud.js' % (os.path.basename(root)))
		root = os.path.dirname(root)
	elif os.path.isdir(root):
		pass
	else:
		raise Exception('Unrecognized path type %s' % root)

	path_cloud_js = os.path.join(root, 'cloud.js')
	if not (os.path.exists(path_cloud_js) and os.path.isfile(path_cloud_js)):
		raise Exception('cloud.js is missing or not a readable file')
	with open(path_cloud_js, 'r') as file:
		cloud_js = json.load(file)

	octree_dir = cloud_js.get('octreeDir', None)
	if octree_dir is None:
		raise Exception()
	octree_dir = os.path.join(root, octree_dir)

	hierarchy_size = cloud_js.get('hierarchyStepSize', None)
	if not isinstance(hierarchy_size, int):
		raise Exception()

	point_attributes = cloud_js.get('pointAttributes', None)
	if point_attributes is None:
		raise Exception()

	if isinstance(point_attributes, list):
		octant_extension = 'bin'
	elif point_attributes == 'LAS':
		octant_extension = 'las'
	elif point_attributes == 'LAZ':
		octant_extension = 'laz'
	else:
		raise Exception()

	yield File('cloud.js', path_cloud_js, 'application/javascript')

	files = {}
	for dirpath, dirnames, filenames in os.walk(octree_dir):
		for filename in filenames:
			if filename in files:
				raise Exception()

			src = os.path.join(dirpath, filename)
			dst = os.path.relpath(src, root)

			files[filename.lower()] = File(dst, src, 'application/octet-stream')

	hierarchy_queue = [OctreeNode('r.hrc', '', 0, {})]
	while hierarchy_queue:
		node = hierarchy_queue.pop(0)
		if not node.key in files:
			raise Exception()

		hierarchy = list(load_hierarchy(files[node.key].path))

		yield files.pop(node.key)

		index = 0
		octree_queue = [node]
		while octree_queue and index < len(hierarchy):
			node = octree_queue.pop(0)

			octant_file = 'r%s.%s' % (node.name, octant_extension)
			if not octant_file in files:
				raise Exception()

			# TODO: {KL} Calculate the size of each point record and validate file sizes
			yield files.pop(octant_file)

			for child_index in range(8):
				child_mask = 1 << child_index
				if hierarchy[index][0] & child_mask == 0:
					continue

				child_name = '%s%d' % (node.name, child_index)

				if len(child_name) % hierarchy_size == 0:
					child_node = OctreeNode(
						'r%s.hrc' % child_name,
						child_name,
						node.depth + 1,
						{}
					)
					hierarchy_queue.append(child_node)
				else:
					child_node = OctreeNode(
						None,
						child_name,
						node.depth + 1,
						{}
					)
					node.children[child_index] = child_node
					octree_queue.append(child_node)

			index += 1

def load_hierarchy(filename):
	with open(filename, 'rb') as file:
		yield from struct.iter_unpack('<BI', file.read())
