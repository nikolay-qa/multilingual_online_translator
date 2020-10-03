import requests
from bs4 import BeautifulSoup
import sys


class UnsupportedInputLanguage(Exception):
    pass


class UnsupportedOutputLanguage(Exception):
    pass


class NoInternetError(Exception):
    pass


class UnableToFindWord(Exception):
    pass


supported_languages = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish',
                       'portuguese', 'romanian', 'russian', 'turkish', 'all']

language_db = {1: "Arabic",
               2: "German",
               3: "English",
               4: "Spanish",
               5: "French",
               6: "Hebrew",
               7: "Japanese",
               8: "Dutch",
               9: "Polish",
               10: "Portuguese",
               11: "Romanian",
               12: "Russian",
               13: "Turkish"}


def input_data():
    lang_input = int(input("""Hello, you're welcome to the translator. Translator supports:
1. Arabic
2. German
3. English
4. Spanish
5. French
6. Hebrew
7. Japanese
8. Dutch
9. Polish
10. Portuguese
11. Romanian3
12. Russian
13. Turkish
Type the number of your language:\n > """))
    lang_output = int(
        input("Type the number of a language you want to translate to or '0' to translate to all languages:\n > "))
    word = input('Type the word you want to translate:\n > ')
    return lang_input, lang_output, word


def translate(inp_lang, output_lang, word_to_translate, translation_db):
    translation, examples_src, examples_translated = [], [], []
    headers = {
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
    try:
        response = requests.get(
            f"https://context.reverso.net/translation/{inp_lang.lower()}-{output_lang.lower()}/{word_to_translate}",
            headers=headers)
        if response.status_code == 404:
            raise UnableToFindWord(f"Sorry, unable to find {word_to_translate}")
        src = response.content
        soup = BeautifulSoup(src, 'lxml')
        links = soup.find_all('a')
        for link in links:
            if link.attrs.get("class") and 'translation' in link.attrs['class']:
                translation.append(link.text.strip())
        ex = soup.find_all('div')
        for line in ex:
            if line.attrs.get('class') and 'src' in line.attrs['class'] and 'ltr' in line.attrs['class']:
                examples_src.append(line.text.strip())
            if line.attrs.get('class') and 'trg' in line.attrs['class'] and 'ltr' in line.attrs['class']:
                examples_translated.append(line.text.strip())
        translation_db[output_lang] = (translation[1:2], examples_src[:1], examples_translated[:1])
    except UnableToFindWord:
        print(f"Sorry, unable to find {word_to_translate}")


def process_translations_data(inp_lang_index, output_lang_index, word_to_translate, db):
    translation_db = {}
    inp_lang = db.get(inp_lang_index, inp_lang_index)
    output_lang = db.get(output_lang_index, output_lang_index)
    if output_lang_index == 0 or output_lang_index == "all":
        for key, value in db.items():
            if value.lower() == inp_lang_index:
                continue
            translate(inp_lang, value, word_to_translate, translation_db)
    else:
        translate(inp_lang, output_lang, word_to_translate, translation_db)
    with open(f'{word_to_translate}.txt', 'w') as file:
        for language in translation_db:
            language_description = f'{language} Translations:'
            print(language_description)
            file.write(language_description)
            for j in range(len(translation_db[language][0])):
                file.write(translation_db[language][0][j])
                print(translation_db[language][0][j])
            print()
            file.write(f'{language} Examples:')
            print(f'{language} Examples:')
            for k in range(len(translation_db[language][2])):
                file.write(translation_db[language][1][k] + ':')
                print(translation_db[language][1][k], ':')
                file.write(translation_db[language][2][k])
                print(translation_db[language][2][k])
                print()


if __name__ == '__main__':
    try:
        if sys.argv[1].lower() not in supported_languages:
            raise UnsupportedInputLanguage(f"Sorry, the program doesn't support {sys.argv[1]}")
        elif sys.argv[2].lower() not in supported_languages:
            raise UnsupportedOutputLanguage(f"Sorry, the program doesn't support {sys.argv[2]}")
        else:
            url = 'http://clients3.google.com/generate_204'
            res = requests.get(url, timeout=5)
            if res.status_code != 204:
                raise NoInternetError("Something wrong with your internet connection")
        if len(sys.argv) == 4:
            process_translations_data(sys.argv[1], sys.argv[2], sys.argv[3], language_db)
        else:
            user_date = input_data()
            process_translations_data(*user_date, language_db)
    except UnsupportedInputLanguage:
        print(f"Sorry, the program doesn't support {sys.argv[1]}")
    except UnsupportedOutputLanguage:
        print(f"Sorry, the program doesn't support {sys.argv[2]}")
    except NoInternetError:
        print("Something wrong with your internet connection")
