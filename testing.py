from typing import Any

from dht import parse_ring_description


ASSERT_SUCCESS = "SUCCESS"
ASSERT_FAIL = "FAILED"


def print_assertion_message(test_name: str, is_successful: bool, test_case_id: Any = None):
    print(f"<ASSERTION: {ASSERT_SUCCESS if is_successful else ASSERT_FAIL}> ", end="")

    if test_case_id is not None:
        print(f"<ID={test_case_id}> ")

    print(f"{test_name}")


def print_assertion_comparison(expected: Any, actual: Any):
    print(f"\t expected: '{str(expected)}',")
    print(f"\t   actual: '{str(actual)}'.")


def assert_equals(expected: Any, actual: Any, test_name: str,
                  verbose: bool = True, test_case_id: Any = None) -> bool:
    is_successful = expected == actual

    if verbose or not is_successful:
        print_assertion_message(test_name, is_successful, test_case_id=test_case_id)

    if not is_successful:
        print_assertion_comparison(expected, actual)

    return is_successful


def assert_description_parsing(description: str,
                               ex_ks_start: int, ex_ks_end: int,
                               ex_node_values: [int], ex_shortcuts: [(int, int)],
                               test_case_id_supplier: callable = lambda: None) -> bool:
    (ks_start, ks_end), node_values, shortcuts = parse_ring_description(
            [line.strip() for line in description.split("\n")])

    return all([
        assert_equals(expected, actual, message, test_case_id=test_case_id_supplier())
        for expected, actual, message in [
            (ex_ks_start, ks_start, f"Key-space start value."),
            (ex_ks_end, ks_end, f"Key-space end value."),
            (ex_node_values, node_values, f"Node values."),
            (ex_shortcuts, shortcuts, f"Shortcuts.")
        ]
    ])


def test_description_parsing():
    # TODO: Ask if we can always assume the shortcuts to be present (keyword and list)
    # TODO: Is the data always in the same order? In the same places?
    # TODO: are the commented keywords actual keywords or just guides for us in the example?

    assert_description_parsing("""#---here starts the file--
    
    #key-space
    1, 100
    
    #nodes
    5, 56, 22, 17, 89, 71, 92, 110
    
    #shortcuts
    5:56, 5:71, 22:89
    
    #---here end the file--
    """, 1, 100, [5, 56, 22, 17, 89, 71, 92, 110], [(5, 56), (5, 71), (22, 89)])

    assert_description_parsing("""
    #short cuts

    # nodes

    # key-space

    #key-space
    1, 9000
    
    #nodes
    500, 1337, 0, 9001, 8999, 2
    
    #shortcuts
    3:200
    """, 1, 9000, [500, 1337, 0, 9001, 8999, 2], [(3, 200)])

    assert_description_parsing("""
    # gibberish comments
    # cool stuff

    # oh man
    # shortcuts
    4:204
    #short cuts
    3:200

    # nodes
    500, 1337, 0, 9001, 8999, 2

    # key-space
    1, 2

    #key-space
    12, 9002
    
    #nodes
    502, 1332, 0, 9001, 8992, 2
    
    #shortcuts
    32:202


    #asd
    """, 12, 9002, [502, 1332, 0, 9001, 8992, 2], [(32, 202)])


def main():
    test_description_parsing()


if __name__ == '__main__':
    main()
