#Qseq to fastq
f = open("sampleqseq2.txt","r")
lib = {}
#f.readline()
sep = ":"
for line in f:
    a = line.split('|')
    headers = "@" + sep.join(a[0:8])
    seq = a[8]
    qual = a[9]
    filter = a[21].strip()
    print(headers)
    print (seq)
    print(qual)
    print (filter)




    #f.close()
