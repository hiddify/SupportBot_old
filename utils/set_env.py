# utils/set_env

import argparse, os

# Define command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--dev', action='store_true', help='Development mode')
args = parser.parse_args()

# Set environment variables based on command-line argument
os.environ['APP_ENVIRONMENT'] = 'development' if args.dev else 'production'
