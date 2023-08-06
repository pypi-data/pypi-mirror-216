from ..common import supports_sorting, supports_pagination


def add_arguments(subparser):
    parser = subparser.add_parser(
        'ls',
        description='Search for work scopes'
    )
    parser.set_defaults(command=main)

    parser.add_argument(
        '-n',
        '--name',
        default=None,
        help='Find workscopes with a matching name'
    )
    parser.add_argument(
        '-o',
        '--organization',
        default=None,
        help='Find workscopes for an organization'
    )

    parser.add_argument(
        '-t',
        '--tag',
        default=None,
        help='Find workscopes by tag'
    )
    parser.add_argument(
        '-r',
        '--recursive',
        default=False,
        action='store_true',
        help='Include subtags'
    )
    parser.add_argument(
        '-xl',
        '--xlabel',
        default=None,
        help='Find workscopes by xLabel (string)'
    )
    parser.add_argument(
        '-yl',
        '--ylabel',
        default=None,
        help='Find workscopes by yLabel (string)'
    )
    parser.add_argument(
        '-u',
        '--units',
        default=None,
        help='Find workscopes with matching units (string) Exact match only'
    )
    parser.add_argument(
        '-p',
        '--parentId',
        default=None,
        help='Find workscopes with matching parentId (string) Exact match only'
    )

    parser.add_argument(
        '--path',
        default=None,
        help='Find workscopes with matching path (string) Exact match only'
    )

    parser.add_argument(
        '--labelMax',
        default=None,
        help='Find workscopes by heatmap max label (string)'
    )
    parser.add_argument(
        '--labelMin',
        default=None,
        help='Find workscopes by heatmap min label (string)'
    )
    parser.add_argument(
        '--labelLegend',
        default=None,
        help='Find workscopes by heatmap legend label (string)'
    )
    parser.add_argument(
        '--heatmapMaxVal',
        default=None,
        help='Find workscopes by heatmap max slider value (number). Exact match only'
    )
    parser.add_argument(
        '--heatmapUnits',
        default=None,
        help='Find workscopes with matching heatmap units (string) Exact match only'
    )

    supports_sorting(parser, 'name')
    supports_pagination(parser)


async def main(args):
    return await args.client.find(
        name=args.name,
        organization=args.organization,
        xLabel=args.xlabel,
        yLabel=args.ylabel,
        units=args.units,
        tag=args.tag,
        recursive=args.recursive,
        sort=args.sort,
        order=args.order,
        offset=args.skip,
        limit=args.limit,
        labelMax=args.labelMax,
        labelMin=args.labelMin,
        labelLegend=args.labelLegend,
        heatmapMaxVal=args.heatmapMaxVal,
        parentId=args.parentId,
        path=args.path
    )
