import os
import logging

from .. import retcode

def add_arguments(subparser):
	parser = subparser.add_parser(
		'download',
		description='Download a file'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-f',
		'--file',
		dest='file',
		required=True,
		help='ID of file to download'
	)

	parser.add_argument(
		'--overwrite',
		default=False,
		action='store_true',
		help='Force an overwrite of the local file if it exists'
	)

	parser.add_argument('output', help='Path to destination file')

async def main(args):
	if os.path.exists(args.output):
		if not args.overwrite:
			logging.error('The file "{file:s}" already exists. To proceed anyway use the --overwrite flag.'.format(file=args.output))
			return retcode.WOULD_OVERWRITE_EXISTING
		elif not os.path.isfile(args.output):
			logging.error('"{file:s}" is not a file'.format(file=args.output))
			return retcode.NOT_A_FILE

	# file = await args.client.get(args.file)
	# TODO: {KL} Warn about mimetype mismatch

	await args.client.download_file(args.file, args.output)
