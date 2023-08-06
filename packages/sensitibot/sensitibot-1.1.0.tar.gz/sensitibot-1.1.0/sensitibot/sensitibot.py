import sys

from cleaner import cleaner
from github import github
from local import local
from reader import reader
from renderer import renderer
from sensitibot import parser


def main():

    args = parser.parse_args()

    files = {}
    name = ""

    if args.command == 'github':
        name = args.user
        try:
            files = github.process_github(
                args.user, args.repository, args.branch, args.token)
        except github.GitHubAPIException as exception:
            print(f'{exception}\n')
            sys.exit(1)  # exit with non-zero exit code

    if args.command == 'local':
        name = "local"
        files = local.process_local(args.path)

    if files == None:
        print("")
        sys.exit(1)  # exit with non-zero exit code

    result = reader.process_files(files, args.deep_search, args.wide_search)
    if result == None:
        sys.exit(1)  # exit with non-zero exit code

    try:
        renderer.show_result_as_text(result, name, args.deep_search)
    except OSError as exception:
        print(f'{exception}\n')

    if args.command == 'local':
        cleaner.process_cleaner(result)

    print("")
