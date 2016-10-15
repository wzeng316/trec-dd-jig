from collections import defaultdict
# used to extract results before (including) certain iteration from a complete run file.
# sample usage: python preprocess.py -run gu_1.txt -ct 3
import click

def preProcess(run, ct):
    runfile = open(run)
    output = open(run + '_' + str(ct), 'w')
    cache = []
    line_ct = 0
    while 1:
        line = runfile.readline()
        line_ct += 1
        if not line:
            break
        else:
            result = line.split('\t')
            if int(result[1]) <= int(ct):
               cache.append(`line_ct` + "\t" + line)

    if "LDA_Indri73" in run or "UL_" in run:
        cache.sort(cmp_items)
    else:
        cache.sort(cmp_items_with_rank)
    dup_check = {}
    for line in cache:
        result = line.split('\t')
        fields_ct = len(result)

        if result[1] in dup_check.keys() and result[3] in dup_check[result[1]].keys() :
           dup_ct = dup_check[result[1]][result[3]]
           dup_check[result[1]][result[3]] += 1
           result[3] = result[3] + "_dup" + str(dup_ct)
        else:
           if result[1] in dup_check.keys():
              dup_check[result[1]][result[3]] = 1
           else:
              dup_check[result[1]] = {}
              dup_check[result[1]][result[3]] = 1


        data = ""
        for number in range(fields_ct):
            if number > 0:
                data += result[number]
            if number > 0 and number < fields_ct - 1:
                data += '\t'

        output.write(data)

def cmp_items(a, b):
    result1 = a.split('\t')
    result2 = b.split('\t')

    line1 = int(result1[0])
    line2 = int(result2[0])

    topic1 = result1[1].split("-")[1]
    topic2 = result2[1].split("-")[1]

    topic_id1 = int(topic1)
    topic_id2 = int(topic2)

    it1 = int(result1[2])
    it2 = int(result2[2])

    #rank1 = float(result1[4])
    #rank2 = float(result2[4])

    if topic_id1 > topic_id2: #topic id
        return 1
    elif topic_id1 == topic_id2:
        if it1 > it2:
           return 1
        elif it1 == it2:
           if line1 > line2:
              return 1
           else:
              return -1
        else:
           return -1
    else:
        return -1

def cmp_items_with_rank(a, b):
    result1 = a.split('\t')
    result2 = b.split('\t')

    line1 = int(result1[0])
    line2 = int(result2[0])

    topic1 = result1[1].split("-")[1]
    topic2 = result2[1].split("-")[1]

    topic_id1 = int(topic1)
    topic_id2 = int(topic2)

    it1 = int(result1[2])
    it2 = int(result2[2])

    rank1 = float(result1[4])
    rank2 = float(result2[4])

    if topic_id1 > topic_id2: #topic id
        return 1
    elif topic_id1 == topic_id2:
        if it1 > it2:
           return 1
        elif it1 == it2:
           if rank1 < rank2:
              return 1
           elif rank1 == rank2:
              if line1 > line2:
                 return 1
              else:
                 return -1
           else:
              return -1
        else:
           return -1
    else:
        return -1

@click.command()
@click.option('-run', type=click.Path(exists=True))
@click.option('-ct', type=click.INT)
def main(run, ct):
    runfile = open(run, 'r')
    preProcess(run, ct)

if __name__ == '__main__':
    main()
