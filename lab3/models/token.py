import string

separators = ['[', ']', '{', '}', '(', ')', ';', ',', ' ', ':', '\t', '\n']
operators = ['osszead', 'kivon', 'szoroz', 'oszt', 'modulusz', 'kisebb', 'kisebbvagyeegyenlo', 'egyenlo',
             'nagyobbvagyegyenlo', 'nagyobb',
             'nemegyenlo', 'novel', 'csokken', 'kapja']
reservedWords = ['ha', 'kulonben', 'karakter', 'karakterlanc', 'amig', 'boolean',
                 'egesz', 'tomb', 'dupla', 'visszater', 'ismeteld', 'Kezd', 'Vegez',
                 'allj', 'valassz', 'eset', 'alapertelmezett', 'konstans']

all_items = separators + operators + reservedWords
codification = dict([(all_items[i], i + 2) for i in range(len(all_items))])
codification['constant'] = 0
codification['identifier'] = 1

alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.ascii_letters) + ['_']
