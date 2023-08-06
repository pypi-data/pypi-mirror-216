import os
# from utils import getSecret, runShellCommand

def install_VEERUM_CLI(config):
  print('-----------------------------------------------------')
  print('job: install_VEERUM_CLI for FME Server Dynamic Engine')
  print('-----------------------------------------------------')

  veerum_sdk_repo = 'veerum-sdk'
  branch = os.getenv('master')
  token_github = ''

  print('branch: ' + branch)

  os.system('docker exec -u 0 -it fmeserver_fmeserverenginedynamic_1 bash')
  
  if (veerum_sdk_repo in os.listdir('.')):
    print('removing existing veerum-cli...')
    deleteDir('./' + veerum_sdk_repo)

  os.system('apt update -y')
  os.system('apt install python3.7-dev -y')
  os.system('python3.7 -m pip install --upgrade pip')
  os.system('pip3 install --upgrade setuptools')
  os.system('apt install git -y')
  os.system('git clone --single-branch --branch ' + branch + ' https://' + token_github + '@github.com/Veerum/' + veerum_sdk_repo + '.git')
  os.system('cd ' + veerum_sdk_repo + '; make install')
  os.system('veerum --profile=development version')

  return(True)
