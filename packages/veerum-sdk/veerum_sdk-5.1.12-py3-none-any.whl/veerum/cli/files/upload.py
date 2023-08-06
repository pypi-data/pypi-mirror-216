import os
import logging
import mimetypes

from datetime import datetime

from .. import retcode

def add_arguments(subparser):
	parser = subparser.add_parser(
		'upload',
		description='Upload a file'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-w',
		'--workscope',
		required=True,
		help='ID of the workscope this file should be attached to'
	)
	parser.add_argument(
		'-d',
		'--date',
		required=True,
		type=datetime.fromisoformat,
		help='Date of the file (ISO8601 format)'
	)
	parser.add_argument(
		'-n',
		'--name',
		default=None,
		help='''
			Name of the file. If not present defaults to the last
			part of the path in the file argument.
		'''
	)
	parser.add_argument(
		'-D',
		'--description',
		default=None,
		help='Description of the file (Optional)'
	)
	parser.add_argument(
		'-m',
		'--mimetype',
		default=None,
		help=''
	)
	parser.add_argument('file', help='Path to a file to upload')

async def main(args):
	if not os.path.isfile(args.file):
		logging.error('"{file:s}" is not a file'.format(file=args.file))
		return retcode.NOT_A_FILE

	if args.name is None:
		args.name = os.path.basename(args.file).strip()
		if not args.name:
			args.name = 'Untitled'

	guessed_mimetype = mimetypes.guess_type(args.file)[0]
	if args.mimetype is None and guessed_mimetype is None:
		logging.error('Unable to guess the mimetype of the file. Please set it explicitly with the --mimetype flag.')
		return retcode.GENERAL_ERROR

	if args.mimetype is None:
		args.mimetype = guessed_mimetype
	elif not (args.mimetype == guessed_mimetype or guessed_mimetype is None):
		logging.warn(
			'Passed mimetype %s does not match the guessed mimetype %s',
			mimetype,
			guessed_mimetype
		)

	# TODO: {KL} If any of this fails rollback the upload

	file = await args.client.create(
		workscope=args.workscope,
		date=args.date,
		name=args.name,
		description=args.description
	)
	if not '_id' in file:
		return file

	await args.client.upload_file(
		file['_id'],
		filename=args.file,
		mimetype=args.mimetype
	)

	return await args.client.get(file['_id'])
