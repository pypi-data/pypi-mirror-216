from collections import namedtuple

File = namedtuple('File', [
	'key', 'path', 'mimetype'
], defaults=(None,))
