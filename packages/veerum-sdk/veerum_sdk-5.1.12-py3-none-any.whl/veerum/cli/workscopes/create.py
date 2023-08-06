def add_arguments(subparser):
    parser = subparser.add_parser(
        'create',
        description='Create a new workscope'
    )
    parser.set_defaults(command=main)

    parser.add_argument(
        '-o',
        '--organization',
        required=True,
        help='ID of the Organization this workscope should be attached to (Required)'
    )
    parser.add_argument(
        '-n',
        '--name',
        required=True,
        help='Name of the workscope (Required)'
    )

    parser.add_argument(
        '-p',
        '--parentId',
        default=None,
        help='Workscope\'s parentId (string)'
    )

    parser.add_argument(
        '-d',
        '--description',
        default=None,
        help='Description of the workscope'
    )
    parser.add_argument(
        '--lat',
        type=float,
        default=None,
        help='Latitude component of the workscope\'s position'
    )
    parser.add_argument(
        '--long',
        type=float,
        default=None,
        help='Longitude component of the workscope\'s position'
    )

    parser.add_argument(
        '-u',
        '--units',
        help='Workscope\'s units (string) Default \"m\"'
    )
    parser.add_argument(
        '-xl',
        '--xlabel',
        help='xLabel for workscope\'s cross section (string) Default \"Chainage\"'
    )
    parser.add_argument(
        '-yl',
        '--ylabel',
        help='yLabel for workscope\'s cross section (string)'
    )

    parser.add_argument(
        '--labelMax',
        help='Heatmap legend max label (string). Default \"High\"'
    )

    parser.add_argument(
        '--labelMin',
        help='Heatmap legend min label (string) Default \"Low\"'
    )

    parser.add_argument(
        '--labelLegend',
        help='Heatmap legend title (string) Default \"Tolerance\"'
    )

    parser.add_argument(
        '--heatmapMaxVal',
        help='Heatmap slider max value (number) Default 8'
    )
    parser.add_argument(
        '--heatmapUnits',
        help='Separate units for this workscope\'s heatmap legend'
    )
    parser.add_argument(
        '--path',
        default=None,
        help='Workscope\'s path'
    )
    parser.add_argument(
        '-dm',
        '--defaultModels',
        default=None,
        help="Turn on the model by default while entering the 3d/2d viewer. Enter a comma delimited list of model id's and/or lm= (latest model) surrounded by quotes."
    )
    parser.add_argument(
        '-si',
        '--showImages',
        default=None,
        help="When a user visits the workscope, labels, fills, bounding boxes will be turned off so that objects are not visible."
    )
    parser.add_argument(
        '-psm',
        '--pointSizeMode',
        default=None,
        help="A point-size mode [adaptive | fixed]"
    )


async def main(args):
    return await args.client.create(
        organization=args.organization,
        name=args.name,
        description=args.description,
        position=[args.long, args.lat] if args.lat and args.long else None,
        units=args.units,
        xLabel=args.xlabel,
        yLabel=args.ylabel,
        labelMax=args.labelMax,
        labelMin=args.labelMin,
        labelLegend=args.labelLegend,
        heatmapMaxVal=args.heatmapMaxVal,
        heatmapUnits=args.heatmapUnits,
        parentId=args.parentId,
        path=args.path,
        defaultModels=args.defaultModels,
        showImages=args.showImages,
        pointSizeMode=args.pointSizeMode
    )
