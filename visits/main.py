from logging.config import fileConfig
from os.path import realpath, dirname

from visits.collection.museum import collect_from_wiki


def main():
    fileConfig(fname=f'{realpath(dirname(__file__))}/resources/logging.ini', disable_existing_loggers=False)
    wiki_page = 'List_of_most_visited_museums'
    collect_from_wiki(wiki_page)


if __name__ == '__main__':
    main()
