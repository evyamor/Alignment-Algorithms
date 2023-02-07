def overlap_alignment(s1, s2, scoring_matrix, gap_penalty):
    # Initialize the alignment matrix with all cells set to 0

    n = len(s1)
    m = len(s2)
    # Initialize the alignment matrix
    alignment_matrix = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        alignment_matrix[i][0] = 0
    for j in range(1, m + 1):
        alignment_matrix[0][j] = 0

    char_to_int = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    # Iterate through the cells of the matrix and compute the maximum score
    # for i in range(1, n + 1):
    #     for j in range(1, m + 1):
    #         diagonal = alignment_matrix[i - 1][j - 1] + scoring_matrix[char_to_int[s1[i - 1]]][char_to_int[s2[j - 1]]]
    #         up = alignment_matrix[i - 1][j] + gap_penalty
    #         left = alignment_matrix[i][j - 1] + gap_penalty
    #         alignment_matrix[i][j] = max(0, diagonal, up, left)
    # Fill the alignment matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            alignment_matrix[i][j] = max(
                alignment_matrix[i - 1][j - 1] + scoring_matrix[char_to_int[s1[i - 1]]][char_to_int[s2[j - 1]]],
                alignment_matrix[i - 1][j] + gap_penalty,
                alignment_matrix[i][j - 1] + gap_penalty,
            )
    # Find the maximum score in the matrix
    max_score = max(alignment_matrix[n])

    # Print the alignment matrix
    print("Alignment matrix:")
    for row in alignment_matrix:
        print(row)

    # Find the optimal alignment and score

    # Find the maximum score in the matrix
    max_score = max(alignment_matrix[n])
    print("max score is : ", max_score)

    # Initialize a list to store the alignments
    alignments = []

    # Iterate through the cells of the matrix and find all alignments with the maximum score
    for j in range(m):
        if alignment_matrix[n][j] == max_score:
            # Trace back the optimal alignment
            s1_aligned = ""
            s2_aligned = ""
            i = n
            while i > 0 and j > 0:
                if alignment_matrix[i][j] == alignment_matrix[i - 1][j - 1] + scoring_matrix[char_to_int[s1[i - 1]]][char_to_int[s2[j - 1]]]:
                    s1_aligned = s1[i - 1] + s1_aligned
                    s2_aligned = s2[j - 1] + s2_aligned
                    i -= 1
                    j -= 1
                elif alignment_matrix[i][j] == alignment_matrix[i - 1][j] + gap_penalty:
                    s1_aligned = s1[i - 1] + s1_aligned
                    s2_aligned = "_" + s2_aligned
                    i -= 1
                else:
                    s1_aligned = "_" + s1_aligned
                    s2_aligned = s2[j - 1] + s2_aligned
                    j -= 1
                    # Add the alignment and score to the list
            alignments.append((s1_aligned, s2_aligned, max_score))
    # Return the list of alignments
    return alignments


# Test the function with the given input
s2 = "ACTTGAG"
s1 = "CGACTG"
scoring_matrix = [[3, -1, -2, -1],
                  [-1, 3, -1, -1],
                  [-2, -1, 3, -1],
                  [-1, -1, -1, 3]]
gap_penalty = -1
alignments = overlap_alignment(s1, s2, scoring_matrix, gap_penalty)

# Print the alignments and scores
print("Optimal alignments:")
for alignment in alignments:
    s1_aligned, s2_aligned, score = alignment
    # add unpenalized gaps to s1 and s2 respectfuly:
    oc1_s = s1.find(s1_aligned[0])
    oc1_e = oc1_s+len(s1_aligned)
    oc2_s = s2.find(s2_aligned[0])
    oc2_e = oc2_s+ len(s2_aligned)
    print(oc1_s,oc1_e,oc2_s,oc2_e)
    while oc1_s > 0 :
        s1_aligned = '_'+s1_aligned
        s2_aligned = s2[oc1_s] +s2_aligned
        oc1_s -= 1
        oc2_e +=1
    while oc2_s > 0 :
        s2_aligned = '_'+s2_aligned
        s1_aligned = s1[oc2_s] +s1_aligned
        oc2_s -= 1
        oc1_e += 1
    while oc1_e < len(s1):
        s1_aligned += '_'
        #s2_aligned = s2[oc1_s] + s2_aligned
        oc1_e += 1
    while oc2_e < len(s2):
        s2_aligned += '_'
        #s1_aligned = s1[oc2_s] + s1_aligned
        oc2_e += 1
    print(s1_aligned)
    print(s2_aligned)
    print("Score:", score)
    exit(1)