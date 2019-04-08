import collections
import re
from argparse import ArgumentParser, FileType

#распарсиваю значения из коммандной строки
def argument_parser():
    parser = ArgumentParser()

    parser.add_argument("path", type=FileType('r'),
                        help="path to file")

    parser.add_argument("-o", "--output_order", choices=['word_len', 'abc', 'frequency'],
                        dest="output_order", default=False,
                        help="sort order: word_len by symbol number, abc by alphabet, frequency by frequency of occurrence")

    parser.add_argument("-t", "--top",
                        type=int, dest="top", default=False,
                        help="number od words")

    parser.add_argument("-f", "--filter", dest="filter", default=False,
                        help="filter by word")

    return parser.parse_args()

#По-строчно считываю значения из файла
def stream_lines(text_file):
    # file = open(text_file)
    while True:
        line = text_file.readline()
        if not line:
            text_file.close()
            break
        yield line

# удаляю знаки препинания и записываю отдельные слова из строки в словарь
def word_compaer(line):
    world_list = []

    line = re.sub(r'[^\w\s\n].?[\n\t ]', ' ', line)
    line = re.sub(r'[ \n\t][^\w\s\n]', ' ', line)
    line = re.sub(r'^\s+|\n|\r|\s+$', '', line).split(' ')
    world_list.extend(line)
    return world_list

if __name__ == "__main__":
        cmd_args = argument_parser()

        #ключи сортировки
        sort_dict = {'word_len': lambda a: (len(a[0]), a[0]), 'abc': lambda a: a[0], 'frequency': lambda a: a[1]}
        #сюда будут записываться слова из списка
        words = []

        #генерирую список со словами
        for j in stream_lines(cmd_args.path):
            words.extend(word_compaer(j))

        #группирую слова по частоте использования
        words = collections.Counter(words)

        if cmd_args.output_order:
            if cmd_args.output_order == 'abc':
                final_list = sorted(words.items(), key=sort_dict.get(cmd_args.output_order))
            else:
                final_list = sorted(words.items(), key=sort_dict.get(cmd_args.output_order), reverse=True)
            words = {word[0]: word[1] for word in final_list}

        #удаляю слова, которые повторяются реже 2-х раз
        words = list(filter(lambda word_frequency: word_frequency[1] > 1, words.items()))

        if cmd_args.top == False:
            cmd_args.top = len(words)

        if cmd_args.filter:
            words = list(filter(lambda word_frequency: re.search(f'^{cmd_args.filter}', word_frequency), words.keys()))

        for word in words[:min(cmd_args.top, len(words))]:
            print(word[0], end='\n')

