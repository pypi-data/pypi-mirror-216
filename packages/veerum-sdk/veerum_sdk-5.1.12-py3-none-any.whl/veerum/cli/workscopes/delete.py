def add_arguments(subparser):
    parser = subparser.add_parser(
		'delete',
		description='Soft delete of workscope and it\'s references in other instances'
	)

    parser.set_defaults(command=main)

    parser.add_argument(
		'-w',
		'--workscope',
		help='ID of workscope to delete'
	)

async def main(args):
    # print('deleting...')
    result = await args.client.delete(args.workscope)
    res_message = 'success'
    hash = ''
    try:
        hash = result['data']['attributes']['hash']
    except KeyError:
        print(result['message'])
        return ('failed')
    else:
        yes = set(['yes', 'y'])
        no = set(['no', 'n'])

        while True:
            try:
                answer = input("Deleting will remove references from all related Objects, Models, Users to the workscope. \nAre you sure? (yes, no) or (y, n)\n")
                choice = answer.lower()
                if (choice not in yes.union(no)):
                    raise ValueError
            except ValueError:
                
                print("Sorry, your input is incorrect.")
                continue
            else:
                if choice in no:
                    res_message = 'cancelled'
                elif choice in yes:
                    print('Deleting...')
                    result = await args.client.delete(args.workscope, hash)
                    references = ''
                    try:
                        references = result['data']['attributes']['references']
                        print('Deleted references:')
                        for i in range(len(references)):
                            modelType = ''
                            modelId = ''
                            for k in references[i]:
                                if k == 'modelType':
                                    modelType = references[i][k]
                                if k == 'modelId':
                                    modelId = references[i][k]
                            print(modelType + ': ' + modelId)
                    except KeyError:
                        print(result['message'])
                        return ('failed')
                break
    return(res_message)