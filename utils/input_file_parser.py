def read_ring_description(path: str) -> [str]:
    with open(path, "r", encoding="UTF-8") as f:
        return f.read().split("\n")


def parse_ring_description(lines: [str]) -> ((int, int), [int], [(int, int)]):
    """
    :param lines: lines from the ring description file (assumed to be correctly formatted).
    :return: a triple of key-space start/end pair, node values and shortcuts
    """

    lines: [str] = [line
                    for line in [line.strip() for line in lines]
                    if 0 < len(line) and not line.startswith("#")]

    key_min, key_max = [int(part.strip()) for part in lines[0].split(",")]

    node_values: [int] = [int(part.strip()) for part in lines[1].split(",")]

    # considering this one as optional (can be missing, therefore empty)
    shortcuts: [(int, int)] = (
        []
        if len(lines) < 3
        else [(int(source.strip()), int(target.strip()))
              for source, target in [part.split(":")
                                     for part in lines[2].split(",")]]
    )

    return (key_min, key_max), node_values, shortcuts
