def smith_waterman(s1, s2, scoring_matrix, gap_penalty):
    m, n = len(s1), len(s2)
    # Initialize the alignment matrix with 0s
    align_matrix = [[0] * (n + 1) for _ in range(m + 1)]
    # Map the characters to integers
    char_to_int = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    curr_max = 0
    max_indicators = {}
    indic_number = 0
    # Iterate through the alignment matrix and fill it with the optimal scores
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Calculate the scores for each possible alignment
            # Calculate the score for the current alignment
            match = align_matrix[i - 1][j - 1] + scoring_matrix[char_to_int[s1[i - 1]]][char_to_int[s2[j - 1]]]
            delete = align_matrix[i - 1][j] + gap_penalty
            insert = align_matrix[i][j - 1] + gap_penalty
            # Take the maximum of the three scores
            align_matrix[i][j] = max(0, match, delete, insert)
            if align_matrix[i][j] > curr_max:
                curr_max = align_matrix[i][j]
                max_indicators = []
                max_indicators.append((i, j))
                indic_number = 1 # found bigger max
            elif align_matrix[i][j] == curr_max:
                max_indicators.append((i, j))
                indic_number += 1
    # Initialize the list of optimal alignments with the empty tuple
    all_alignments = []
    print(max_indicators)
    # Trace back through the matrix to find the optimal alignments using indicators
    for ind in range(0,indic_number):
        alignment_one = ""
        alignment_two = ""
        i = max_indicators[ind][0]
        j = max_indicators[ind][1]
        while align_matrix[i][j] != 0:
            alignment_one += s1[i-1]
            alignment_two += s2[j -1]
            i -= 1
            j -= 1
        all_alignments.append((alignment_one[::-1], alignment_two[::-1])) # reverse alignments before appending

    # Return the alignment matrix, the list of alignments, and the optimal score
    return align_matrix, all_alignments, curr_max


# # Test the function
# first example
# s1 = "ATAGGC"
# s2 = "CTACGA"
# scoring_matrix = [[3, -1, -2, -1],
#                   [-1, 3, -1, -1],
#                   [-2, -1, 3, -1],
#                   [-1, -1, -1, 3]]
# second example
#   s1 = "ABBABA"
#   s2 = "AB"
#   scoring_matrix = [[5, -3],
#                  [-3, 4]]
#
#   gap_penalty = -2
# third example
s2 = "TAATA"
s1 = "TACTAA"
scoring_matrix = [[1, -1, -1, -1],
                  [-1, 1, -1, -1],
                  [-1, -1, 1, -1],
                  [-1, -1, -1, 1]]
gap_penalty = -2
# Get the alignment matrix, alignments, and optimal score
align_matrix, alignments, optimal_score = smith_waterman(s1, s2, scoring_matrix, gap_penalty)

# Print the alignment matrix
print("Alignment Matrix:")
for row in align_matrix:
    print(row)

# Print the alignments
print("\nOptimal Alignments:")
for a in alignments:
    print(a[0])
    print(a[1])
    print()

# Print the optimal score
print("Optimal Score:", optimal_score)
