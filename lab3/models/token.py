import string

separators = ['[', ']', '{', '}', '(', ')', ';' , ',', ' ', ':', '\t', '\n']
operators = ['osszead', 'kivon', 'szoroz', 'oszt', 'modulusz', 'kisebb', 'kisebbvagyeegyenlo', 'egyenlo', 'nagyobbvagyegyenlo', 'nagyobb',
             'nemegyenlo', 'novel', 'csokken', 'kapja']
reservedWords = ['ha', 'kulonben', 'karakter', 'karakterlanc', 'amig', 'boolean',
                 'egesz', 'tomb', 'dupla', 'visszater', 'ismeteld', 'Kezd', 'Vegez',
                 'allj', 'valassz', 'eset', 'alapertelmezett', 'konstans' ]

all_items = separators + operators + reservedWords
codification = dict([(all_items[i], i + 3) for i in range(len(all_items))])
codification['identifier'] = 1
codification['constant'] = 2


alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.ascii_letters) + ['_']
