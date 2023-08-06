def dna_kmer(dna_string, kmer, step):
    print(dna_string)

    kmerized = ""
    for i in range(0, len(dna_string)-kmer+1, step):
        kmerized = kmerized + dna_string[i:i+kmer] + " "

    return kmerized

if __name__ == "__main__":
    dna = "ACTGTCGTACAGTGACCAGTGGTAGT"
    kmerized_dna = dna_kmer(dna, 5, 1)
    print(kmerized_dna)