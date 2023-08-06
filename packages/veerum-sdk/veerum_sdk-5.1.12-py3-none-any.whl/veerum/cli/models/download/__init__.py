def add_arguments(subparser):
	parser = subparser.add_parser(
		'download',
		description='Download a file',
	)

	parser.add_argument(
		'-m',
		'--model',
		dest='model',
		required=True,
		help='ID of model to download'
	)

	parser.add_argument(
		'--overwrite',
		default=False,
		action='store_true',
		help='Force an overwrite of the local model if it exists'
	)

	parser.add_argument('output', help='Path to destination model')
