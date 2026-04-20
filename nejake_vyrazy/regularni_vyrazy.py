import re

text = "Psaní je zvláštní činnost. Na první pohled se může zdát jednoduché"
regex_slova = r"\w+"
vsechna_slova = re.findall(regex_slova, text)
print(vsechna_slova)

regex_mezery = r"\x20+"
vsechny_mezery = re.findall(regex_mezery, text)
print(f"počet mezer: {len(vsechny_mezery)}")