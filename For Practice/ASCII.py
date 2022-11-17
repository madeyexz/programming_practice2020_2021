n,m = map(int, input().split())

if n > 127 or n < 0:
    print('is not ASCII!!')
else:
    seq = bin(n)
    seq1 = [seq[i:i+2] for i in range(0, len(seq),2)]

    if seq.count('1') % 2 == m:
        seq1[0] = '0'
        seq2 = ''.join(seq1)
        for i in seq2:
            if i.isdigit() == True:
                print(i, end = ' ')
        
    else:
        seq1[0] = '1'
        seq2 = ''.join(seq1)
        for i in seq2:
            if i.isdigit() == True:
                print(i, end = ' ')