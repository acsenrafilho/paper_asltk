import argparse

from rich import print

parser = argparse.ArgumentParser(
    description='Run experiments from the paper_asltk package.'
)
subparsers = parser.add_subparsers(dest='command', required=True)

# Placeholder for exp_spatial_filters
parser_spatial = subparsers.add_parser(
    'spatial_filters', help='Run the spatial filters experiment'
)
# Add arguments for spatial_filters as needed
# parser_spatial.add_argument('--example', type=str, help='Example argument')

# Placeholder for exp_other_experiment
parser_other = subparsers.add_parser(
    'other_experiment', help='Run another experiment'
)
# Add arguments for other_experiment as needed

args = parser.parse_args()

if args.command == 'spatial_filters':
    # TODO: Import and call the spatial filters experiment
    print('Running spatial filters experiment (not yet implemented).')
elif args.command == 'other_experiment':
    # TODO: Import and call the other experiment
    print('Running other experiment (not yet implemented).')
else:
    parser.print_help()
