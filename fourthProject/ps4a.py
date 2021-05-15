# Problem Set 4A
# Name: Michael Sargsyan
# Collaborators:
# Time Spent: 3 hours

def get_permutations(sequence):
    if len(sequence) < 2:
        return [sequence]
    result = []
    for i in range(len(sequence)):
        for p in get_permutations(sequence[:i] + sequence[i + 1:]):
            result += [sequence[i] + p]
    return result

if __name__ == '__main__':
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
