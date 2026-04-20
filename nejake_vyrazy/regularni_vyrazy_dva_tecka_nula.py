import re

date_regex = r"\b\d{1,2}([./-])\d{1,2}\1\d{4}\b"
date_vzor = re.compile(date_regex)
texts = [
    "Datum 30.3.2026", # shoda
    "Datum 30/3/2026", # bez shody
    "Datum 30-3-2026", # bez shody
]

print("\n priklad - validace dat pomoci zpetneho odkazu")
for text in texts:
    match = date_vzor.search(text)
    if match:
        print(f" '{text}' = shoda. oddelovac: '{match.group(1)}'")
    else:
        print(f" '{text}' = bez shody")