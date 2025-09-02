import itertools
import random
import string
from datetime import datetime

leet_dict = {
    'a': ['@', '4'],
    'b': ['8'],
    'e': ['3'],
    'g': ['9'],
    'i': ['1', '!'],
    'l': ['1', '|'],
    'o': ['0'],
    's': ['$', '5'],
    't': ['7'],
    'z': ['2']
}

common_prefixes = ['my', 'the', 'super', 'ultra', '0x', 'root', 'king', 'admin']
common_suffixes = ['123', '007', '2023', '2024', '2025', '321', '69', '420', '!', '@', '#', '666', '777']
symbols = ['!', '@', '#', '$', '%', '^', '&', '*']

def all_case_combos(word):
    return map(''.join, itertools.product(*[(c.lower(), c.upper()) for c in word]))

def insert_symbols(word):
    results = set()
    for i in range(len(word)):
        for s in symbols:
            results.add(word[:i] + s + word[i:])
    return results

def leetify(word, deep=False):
    variations = set([word])
    queue = [word]
    for _ in range(3 if deep else 2):  # deeper leet level = more variations
        new_queue = []
        for w in queue:
            for i, c in enumerate(w):
                if c.lower() in leet_dict:
                    for replacement in leet_dict[c.lower()]:
                        new_word = w[:i] + replacement + w[i+1:]
                        if new_word not in variations:
                            new_queue.append(new_word)
                            variations.add(new_word)
        queue = new_queue
    return variations

def generate_passwords(base_word):
    base_word = base_word.strip()
    all_variants = set()

    # Case combos
    all_variants.update(all_case_combos(base_word))

    # Leetified
    all_variants.update(leetify(base_word, deep=True))

    # Reversed
    all_variants.add(base_word[::-1])

    # Duplicated
    all_variants.add(base_word + base_word)

    # Prefix/Suffix additions
    extended_variants = set()
    for variant in all_variants:
        for pre in common_prefixes:
            extended_variants.add(pre + variant)
        for suf in common_suffixes:
            extended_variants.add(variant + suf)
            extended_variants.add(variant + suf * 2)
            for year in ['1999', '2000', '2012', '2020', '2024', '2025','2061','2004']:
                extended_variants.add(variant + year)
    all_variants.update(extended_variants)

    # Insert symbols
    symbol_injected = set()
    for variant in all_variants:
        symbol_injected.update(insert_symbols(variant))
    all_variants.update(symbol_injected)

    return sorted(list(all_variants))

def main():
    print("\n🔐 PassMutator MAX — Hardcore Password Generator 🔐\n")
    base = input("Enter a base word (e.g. 'nepal'): ")
    passwords = generate_passwords(base)

    filename = f"ultra_passlist_{base}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for p in passwords:
            f.write(p + "\n")

    print(f"\n✅ Generated {len(passwords)} mutated passwords.")
    print(f"📁 Saved to {filename}")

if __name__ == "__main__":
    main()