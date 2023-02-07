def traceback(optimal_score, s1, s2, scoring_matrix, gap_penalty, alignment_matrix, i, j, alignment1, alignment2,
              alignments):
    # Base case: if we have reached the first cell of the matrix, append the current alignments to the list and return
    if i == 0 and j == 0:
        alignments.append((alignment1, alignment2))
        return

    # Check if the current cell came from the diagonal, left, or top
    if i > 0 and j > 0 and alignment_matrix[i][j] == alignment_matrix[i - 1][j - 1] + \
            scoring_matrix[['A', 'C', 'G', 'T'].index(s1[i - 1])][['A', 'C', 'G', 'T'].index(s2[j - 1])]:
        # If the current cell came from the diagonal, align character s1[i-1] with s2[j-1] and call traceback with updated indices and alignments
        traceback(optimal_score, s1, s2, scoring_matrix, gap_penalty, alignment_matrix, i - 1, j - 1,
                  s1[i - 1] + alignment1, s2[j - 1] + alignment2, alignments)
    if i > 0 and alignment_matrix[i][j] == alignment_matrix[i - 1][j] + gap_penalty:
        # If the current cell came from the top, insert a gap in s2 and call traceback with updated indices and alignments
        traceback(optimal_score, s1, s2, scoring_matrix, gap_penalty, alignment_matrix, i - 1, j - 1,
                  s1[i - 1] + alignment1, '_' + alignment2, alignments)
    if j > 0 and alignment_matrix[i][j] == alignment_matrix[i][j - 1] + gap_penalty:
        # If the current cell came from the left, insert a gap in s1 and call traceback with updated indices and alignments
        traceback(optimal_score, s1, s2, scoring_matrix, gap_penalty, alignment_matrix, i - 1, j - 1, '_' + alignment1,
                  s2[j - 1] + alignment2, alignments)


def get_optimal_alignments(optimal_score, s1, s2, scoring_matrix, gap_penalty, alignment_matrix):
    alignments = []
    traceback(optimal_score, s1, s2, scoring_matrix, gap_penalty, alignment_matrix, len(s1), len(s2), '', '',
              alignments)
    return alignments


def needleman_wunsch(s1, s2, scoring_matrix, gap):
    # Initialize the alignment matrix with zeros and dimensions (len(s1)+1) x (len(s2)+1)
    alignment_matrix = [[0 for j in range(len(s2) + 1)] for i in range(len(s1) + 1)]

    # Initialize the gap penalty for each cell in the first row and column
    for i in range(1, len(s1) + 1):
        alignment_matrix[i][0] = alignment_matrix[i - 1][0] + gap
    for j in range(1, len(s2) + 1):
        alignment_matrix[0][j] = alignment_matrix[0][j - 1] + gap

    # Fill the rest of the matrix using the recurrence relation
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            # Get the score for aligning character s1[i-1] with s2[j-1]
            # The -1 is because Python uses 0-indexing and the alignment matrix has an extra row and column
            s = scoring_matrix[['A', 'C', 'G', 'T'].index(s1[i - 1])][['A', 'C', 'G', 'T'].index(s2[j - 1])]
            alignment_matrix[i][j] = max(alignment_matrix[i - 1][j - 1] + s,
                                         alignment_matrix[i - 1][j] + gap,
                                         alignment_matrix[i][j - 1] + gap)

    score = alignment_matrix[len(s1)][len(s2)]
    all_alignments = []
    # Find all optimal alignments by recursively backtracking through the alignment matrix
    all_alignments = get_optimal_alignments(score, s1, s2, scoring_matrix, gap, alignment_matrix)
    return alignment_matrix, all_alignments, score


#   Input insertion:

s1 = 'ATAGGC'
s2 = 'CTACGA'
gap = -1
scoring_matrix = [[3, -1, -2, -1], [-1, 3, -1, -1], [-2, -1, 3, -1], [-1, -1, -1, 3]]
#   scoring_matrix = [[3, -2, -3, -2], [-2, 3, -2, -2], [-3, -2, 3, -2], [-2, -2, -2, 3]]
alignment_matrix, optimal_alignment, score = needleman_wunsch(s1, s2, scoring_matrix, gap)
for row in alignment_matrix:
    print(row)
for alignment in optimal_alignment:
    print(alignment)
print(score)
