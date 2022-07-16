def adjacents(sequence, circular=False):
    if not sequence:
        return None

    size = len(sequence) - 1

    for i in range(size):
        yield (sequence[i], sequence[i + 1])

    if circular:
        yield (sequence[-1], sequence[0])


def group_by(sequence, group_size):
    iterable = iter(sequence)
    try:
        while True:
            output = []
            for _ in range(group_size):
                output.append(next(iterable))
            yield output
    except StopIteration:
        pass
