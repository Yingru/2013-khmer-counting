

import khmer
import sys
import screed
from screed.fasta import fasta_iter

def process_file(filename,HT_SIZE_array):

    N_HT = 4
    K = 12

    list_average_miscount = []
    list_fp_miscount0 = []

    print filename
    for HT_SIZE in HT_SIZE_array:
        print HT_SIZE
        ht = khmer.new_counting_hash(K, HT_SIZE, N_HT)
        ht.consume_fasta(filename)
                
        ktable = khmer.new_ktable(K)
        for n, record in enumerate(fasta_iter(open(filename))):
            sequence = record['sequence']
#            ktable.consume(sequence)

            seq_len = len(sequence)
            for n in range(0,seq_len+1-K):
                kmer = sequence[n:n+K]
                ktable.count(kmer)

        list_miscount = []
        total_kmer = 0 # total number of unique k-mers
        miscount0 = 0
        
        for i in range(0, ktable.n_entries()):
            n = ktable.get(i)
            if n:
                total_kmer = total_kmer + 1
                kmer2 = ktable.reverse_hash(i)
                miscount = ht.get(kmer2) - ktable.get(kmer2)
                list_miscount.append(miscount)
                if miscount > 0:
                    miscount0 = miscount0 + 1

        average_miscount = float(sum(list_miscount))/len(list_miscount)
        list_average_miscount.append(average_miscount)
        fp_miscount0 = float(miscount0)/total_kmer
        list_fp_miscount0.append(fp_miscount0)

    to_return = [list_average_miscount,list_fp_miscount0,total_kmer]
    return to_return

def write_result(file,result,file_out_fp):
    file = file+'\n'
    file_out_fp.write(file)
    for i in range(2):
        r_list = result[i]
        line = ''
        for m in range(len(HT_SIZE_array)):
            line = line+' '+str(r_list[m])
        line = line+'\n'
        file_out_fp.write(line)
        
#ht_size = "100000,200000,400000"
ht_size = "100000,200000,400000,600000,800000,1000000,1200000"
file_list = "MH0001.trimmed.head176800.fa,random_kmers_1M_3c.fa,random_reads_1.67M_3c_0.03e.fa,random_reads_2.54M_3c_0.00e.fa"
file_out = sys.argv[1]

HT_SIZE = ht_size.split(',')
HT_SIZE_array = []
for ht in HT_SIZE:
    HT_SIZE_array.append(int(ht))
file_lists = file_list.split(',')
file_out_fp = open(file_out,'w')

for file_name in file_lists:
    result = process_file(file_name,HT_SIZE_array)
    write_result(file_name,result,file_out_fp)

    

