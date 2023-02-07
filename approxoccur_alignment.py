def approximate_occurrence_alignment(t, p, scoring_matrix, gap_penalty):
  # Initialize the alignment matrix with all zeros
  alignment_matrix = [[0 for j in range(len(p)+1)] for i in range(len(t)+1)]
  # set 'p' rows to gap penalties
  for j in range(1, len(p) + 1):
    alignment_matrix[0][j] = alignment_matrix[0][j - 1] + gap_penalty
  char_to_int = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
  # Fill out the alignment matrix
  for i in range(1, len(t)+1):
    for j in range(1, len(p)+1):
      align = alignment_matrix[i-1][j-1] + scoring_matrix[char_to_int[t[i - 1]]][char_to_int[p[j - 1]]]
      delete = alignment_matrix[i-1][j] + gap_penalty
      insert = alignment_matrix[i][j-1] + gap_penalty
      alignment_matrix[i][j] = max(0, align, delete, insert)

  # Find the optimal alignment score by searching the last row and column of the alignment matrix
  optimal_score = 0
  for i in range(len(t)+1):
    optimal_score = max(optimal_score, alignment_matrix[i][len(p)])
  for j in range(len(p)+1):
    optimal_score = max(optimal_score, alignment_matrix[len(t)][j])

  # Initialize the list of optimal alignments with an empty alignment
  alignments = [("", "")]

  # Find the optimal alignments by backtracking through the alignment matrix
  i = len(t)
  j = len(p)
  while i > 0 or j > 0:
    if i > 0 and alignment_matrix[i][j] == alignment_matrix[i - 1][j] + gap_penalty:
      alignments = [(a + t[i - 1], b + "-") for (a, b) in alignments]
      i -= 1
    elif j > 0 and alignment_matrix[i][j] == alignment_matrix[i][j - 1] + gap_penalty:
      alignments = [(a + "-", b + p[j - 1]) for (a, b) in alignments]
      j -= 1
    elif i > 0 and j > 0 and alignment_matrix[i][j] == alignment_matrix[i - 1][j - 1] + \
            scoring_matrix[char_to_int[t[i - 1]]][char_to_int[p[j - 1]]]:
      alignments = [(a + t[i - 1], b + p[j - 1]) for (a, b) in alignments]
      i -= 1
      j -= 1
    else:
      alignments = [(a + t[i - 1], b + "-") for (a, b) in alignments]
      i -= 1
      j -= 1

  # Reverse the alignments to get the original order
  alignments = [(a[::-1], b[::-1]) for (a,b) in alignments]

  return (optimal_score, alignments, alignment_matrix)

# Test the function
t = "CAGCGGTTGC"
p = "AGGA"
scoring_matrix = [[3, -1, -2, -1],
                  [-1, 3, -1, -1],
                  [-2, -1, 3, -1],
                  [-1, -1, -1, 3]]
gap_penalty = -1
score, alignments , matrix = approximate_occurrence_alignment(t, p, scoring_matrix, gap_penalty)
for row in matrix :
  print(row)
print(alignments)
print(score)
