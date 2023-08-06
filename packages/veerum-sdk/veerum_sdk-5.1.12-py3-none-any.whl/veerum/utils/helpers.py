from collections import namedtuple

File = namedtuple('File', [
	'key', 'path', 'mimetype', 'size'
], defaults=(None,))
