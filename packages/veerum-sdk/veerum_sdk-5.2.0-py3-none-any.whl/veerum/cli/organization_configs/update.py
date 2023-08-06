def add_arguments(subparser):
	parser = subparser.add_parser(
		'update',
		description='Specify an organization config'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-o',
		'--organization',
		required=True,
		help='ID of organization to modify'
	)
	parser.add_argument(
		'-rlu',
		'--rateLimitUsers',
		default=None,
		help='To change the number of available API requests to list users per organization'
	)
	parser.add_argument(
		'-rla',
		'--rateLimitAnnotations',
		default=None,
		help='To change the number of available API requests to list annotations per organization'
	)
	parser.add_argument(
		'-rlf',
		'--rateLimitFiles',
		default=None,
		help='To change the number of available API requests to list files per organization'
	)
	parser.add_argument(
		'-rlm',
		'--rateLimitModels',
		default=None,
		help='To change the number of available API requests to list models per organization'
	)
	parser.add_argument(
		'-rlw',
		'--rateLimitWorkscopes',
		default=None,
		help='To change the number of available API requests to list workscopes per organization'
	)
	parser.add_argument(
		'-rlos',
		'--rateLimitObjectsSearch',
		default=None,
		help='To change the number of available API requests to search objects per organization'
	)
	parser.add_argument(
		'-rloss',
		'--rateLimitObjectsSpatialSearch',
		default=None,
		help='To change the number of available API requests to spatial search objects per organization'
	)

async def main(args):
	# TODO: {KL} sanitize the slug
	return await args.client.update(
		args.organization,
		rateLimitUsers=args.rateLimitUsers,
		rateLimitAnnotations=args.rateLimitAnnotations,
		rateLimitFiles=args.rateLimitFiles,
		rateLimitModels=args.rateLimitModels,
		rateLimitWorkscopes=args.rateLimitWorkscopes,
		rateLimitObjectsSearch=args.rateLimitObjectsSearch,
		rateLimitObjectsSpatialSearch=args.rateLimitObjectsSpatialSearch
	)
