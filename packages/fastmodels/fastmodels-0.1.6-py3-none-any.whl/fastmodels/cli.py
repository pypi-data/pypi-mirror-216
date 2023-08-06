import argparse
from fastmodels.datavalidator.validator import validate_jsonl


def main():
    parser = argparse.ArgumentParser(description='Validate a JSONL file.')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create a parser for the "validate_data" command
    parser_validate = subparsers.add_parser('validate_data', help='Validate a JSONL file.')
    parser_validate.add_argument('-f', '--file', type=str, required=True,
                                 help='The path to the JSONL file to validate.')

    args = parser.parse_args()
    if args.command == 'validate_data':
        is_valid = validate_jsonl(args.file)
        if is_valid:
            print('The JSONL file is valid.')
            print('您的数据文件是有效的。')
        else:
            print('The JSONL file is invalid. Please make sure each line conforms to the format:')
            print('{"instruction": "<text>", "input": "<text>", "output":"<text>"}')
            print('您的数据文件存在问题。')


if __name__ == '__main__':
    main()
