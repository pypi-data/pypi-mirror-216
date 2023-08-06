import logging

def add_arguments(subparser):
    parser = subparser.add_parser(
        'update',
        description='Update an existing work scopes'
    )
    parser.set_defaults(command=main)

    parser.add_argument(
        '-w',
        '--workscope',
        dest='workscope',
        required=True,
        help='ID of workscope to inspect'
    )
    parser.add_argument(
        '-n',
        '--name',
        default=None,
        help='Name of the workscope'
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
        '-xl',
        '--xlabel',
        default=None,
        help='xLabel for workscope\'s cross-section (string)'
    )
    parser.add_argument(
        '-yl',
        '--ylabel',
        default=None,
        help='yLabel for workscope\'s cross-section (string)'
    )
    parser.add_argument(
        '-p',
        '--parentId',
        default=None,
        help='parentId for workscope (string)'
    )
    parser.add_argument(
        '-o',
        '--organization',
        default=None,
        help='Organization ID for workscope (string)'
    )
    parser.add_argument(
        '--path',
        default=None,
        help='Workscope\'s path'
    )
    parser.add_argument(
        '-u',
        '--units',
        default=None,
        help='Units for workscope (string)'
    )
    parser.add_argument(
        '--labelMax',
        default=None,
        help='Heatmap legend max label (string). Default \"High\"'
    )
    parser.add_argument(
        '--labelMin',
        default=None,
        help='Heatmap legend min label (string) Default \"Low\"'
    )
    parser.add_argument(
        '--labelLegend',
        default=None,
        help='Heatmap legend title (string) Default \"Tolerance\"'
    )
    parser.add_argument(
        '--heatmapMaxVal',
        default=None,
        help='Heatmap slider max value (number) Default 8'
    )
    parser.add_argument(
        '--heatmapUnits',
        default=None,
        help='Units (string) to be rendered on the heatmap legend. Default m'
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
    # Double Check
  if args.organization:
    message = 'Are you sure want to change to organization {} (yes/no)?'.format(args.organization)
    answer = input(message).lower().strip()
    if len(answer) == 0 or answer[0] != 'y':
      logging.warning('User cancel the request')
      raise

  return await args.client.update(
      workscope=args.workscope,
      name=args.name,
      description=args.description,
      latitude=args.lat,
      longitude=args.long,
      xLabel=args.xlabel,
      yLabel=args.ylabel,
      units=args.units,
      labelMax=args.labelMax,
      labelMin=args.labelMin,
      labelLegend=args.labelLegend,
      heatmapMaxVal=args.heatmapMaxVal,
      heatmapUnits=args.heatmapUnits,
      parentId=args.parentId,
      organization=args.organization,
      path=args.path,
      defaultModels=args.defaultModels,
      showImages=args.showImages,
      pointSizeMode=args.pointSizeMode
    )
