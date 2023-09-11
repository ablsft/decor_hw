import xml.etree.ElementTree as ET
import datetime


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            called_time = datetime.datetime.now()

            result = old_function(*args, **kwargs)
            
            with open(path, 'a', encoding='utf-8') as log_file:
                log_file.write(f'{called_time.strftime("%m/%d/%Y, %H:%M:%S")}\n')
                log_file.write(f'{old_function.__name__}\n')
                log_file.write(f'{", ".join(map(str, args))}')
                if args and kwargs:
                    log_file.write(', ')
                log_file.write(f'{", ".join(map(str, kwargs.values()))}')
                log_file.write(f'\n{str(result)}\n\n')
                
            return result
        return new_function
    return __logger

@logger('read_xml.log')
def read_xml(file_path, word_max_len=6, top_words_amt=10):
    parser = ET.XMLParser(encoding='utf-8')
    tree = ET.parse(file_path, parser)
    root = tree.getroot()
    items = root.findall('channel/item')

    words = []
    for item in items:
        raw = [word for word in item.find('description').text.split() if len(word) > word_max_len]
        words.extend(raw)
  
    unique_words = list(set(words))
    freq_word = [[word, words.count(word)] for word in unique_words]
    freq_word.sort(key=lambda x: x[1], reverse=True)
    top_words = [top_word[0] for top_word in freq_word]

    return top_words[:top_words_amt]

if __name__ == '__main__':
    logger(read_xml('newsafr.xml'))