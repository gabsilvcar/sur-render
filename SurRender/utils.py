def adjacents(sequence, circular=False):
    size = len(sequence) - 1

    for i in range(size):
        yield (sequence[i], sequence[i+1])

    if circular:
        yield (sequence[-1], sequence[0])