import argparse
import sys


def main():
    parser = argparse.ArgumentParser(prog='example-package-zaw',
                                     description='okn related graphs plotting program.')
    parser.add_argument('--version', action='version', version='0.0.2'),
    parser.add_argument("-t", dest="plot_type", required=True, default=sys.stdin,
                        help="trial, summary, (staircase or progress), tidy or simpler", metavar="plot type")
    parser.add_argument("-d", dest="directory_input", required=True, default=sys.stdin,
                        help="directory folder to be processed", metavar="directory")
    parser.add_argument("-c", dest="config_dir", required=False, default=sys.stdin,
                        help="config or resource file", metavar="config location")
    parser.add_argument("-r", dest="referenced_csv", required=False, default=sys.stdin,
                        help="referenced csv file to be referenced", metavar="referenced csv")
    parser.add_argument("-o", dest="output", required=False, default=sys.stdin,
                        help="output folder or file directory", metavar="output")
    parser.add_argument("-p", dest="template", required=False, default=sys.stdin,
                        help="template file location or file name", metavar="template")
    parser.add_argument("-n", dest="decider_name", required=False, default=sys.stdin,
                        help="decider name for each sub folder", metavar="decider name")

    args = parser.parse_args()
    directory_input = str(args.directory_input)
    type_input = str(args.plot_type)
    config_file_location = str(args.config_dir)
    referenced_csv_dir = str(args.referenced_csv)
    output_dir = str(args.output)
    template_dir = str(args.template)
    decider_name = str(args.decider_name)

