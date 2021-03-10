import csv
import Levenshtein

def check_grammer(input):

    with open('word.csv','r') as f:
        reader = csv.reader(f)
        total_string = [row[1] for row in reader];
    # print(total_string)

    match_list=[];

    for item in total_string:
        matchdic = { 'match' : Levenshtein.distance(input, item), 'Content':item };
        match_list.append(matchdic);
    new = sorted(match_list, key=lambda a: a.__getitem__('match'), reverse=True);

    if new[0].__getitem__('Content') == input:
        return None
    else:
        if new[0].__getitem__('match') != 0:
            pass
            # print(new[0].__getitem__('Content'))
            # print(new[1].__getitem__('Content'))
            # print(new[2].__getitem__('Content'))
    return new[0].__getitem__('Content')


test = check_grammer('structure apple')
print(test)