def parse_csv():
    syn_lookup = {}
    with open('dataset/english_synonyms_and_antonyms.csv','r') as f:
        for line in f:
            word = line.split('\t')[0]
            synonym = line.split('\t')[1].split(', ')[0]
            syn_lookup[word] = synonym
    return syn_lookup

table = parse_csv()
print(table)