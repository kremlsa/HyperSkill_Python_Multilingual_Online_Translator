import requests
import sys
from bs4 import BeautifulSoup

l7s = {1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish', 5: 'French', 6: 'Hebrew', 7: 'Japanese',
            8: 'Dutch', 9: 'Polish', 10: 'Portuguese', 11: 'Romanian', 12: 'Russian', 13: 'Turkish'}
headers = {'User-Agent': 'Mozilla/5.0'}
# Parse command line
args = sys.argv
l_from = str(args[1])
l_to = str(args[2])
text = str(args[3])
if l_from.capitalize() not in l7s.values():
    print(f"Sorry, the program doesn't support {l_from}")
    exit(0)
if l_to.capitalize() not in l7s.values() and l_to != 'all':
    print(f"Sorry, the program doesn't support {l_to}")
    exit(0)

# Make list for sending requests
l_to_list = [x for x in l7s.values() if x.lower() != l_from] if l_to == 'all' else [l_to]
# Write to file
with open(f'{text}.txt', 'a', encoding='utf-8') as file_:
    # Sending requests
    for lang_ in l_to_list:
        try:
            r = requests.get(f'https://context.reverso.net/translation/{l_from.lower()}-{lang_.lower()}/{text}', headers=headers)
            if r.status_code == 404:
                print(f'Sorry, unable to find {text}')
                exit(0)
            soup = BeautifulSoup(r.content, 'html.parser')
            print(lang_, 'Translations:')
            file_.write(f'{lang_} Translations:\n')
            result = []
            for elem in soup.find_all('a', {"class": 'translation'}):
                result.append(elem.text.strip())
            for word in result[1:2]:
                file_.write(word + '\n')
                print(word)
            print()
            file_.write('\n')
            print(lang_, 'Examples:')
            file_.write(f'{lang_} Examples:\n')
            result_from = soup.find_all('div', {"class": "src ltr"})
            result_to = soup.find_all('div', {"class": ["trg ltr", "trg rtl arabic", "trg rtl"]})
            result_from = [x.text.strip() for x in result_from]
            result_to = [x.text.strip() for x in result_to]
            sentences = []
            for elem in zip(result_from[:1], result_to[:1]):
                print(elem[0])
                file_.write(elem[0] + '\n')
                print(elem[1])
                file_.write(elem[1] + '\n')
                print()
                file_.write('\n')
        except ConnectionError:
            print('Something wrong with your internet connection')
