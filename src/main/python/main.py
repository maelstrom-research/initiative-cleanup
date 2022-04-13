import argparse
from cleanup.initiaitive import MlstrInitiativeCleanup

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('--user', '-u', required=False, help='User name')
  parser.add_argument('--password', '-p', required=False, help='User password')
  parser.add_argument('--mica', '-m', required=False, default='http://localhost:8082',
                      help='Mica server base url (default: http://localhost:8082)')
  args = parser.parse_args()

  MlstrInitiativeCleanup(args).process()
