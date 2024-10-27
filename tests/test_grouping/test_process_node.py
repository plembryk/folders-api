from groups.grouping import Node, prepare_structure, process_node


class TestProcessNode:
    def test_node_name_in_node_words(self):
        words = ["word", "word_a", "word_b"]
        word, word_a, word_b = words
        node_to_process = Node(name=word, children={word_a, word_b}, parent=None, words=set(words))
        input_structure = {
            "word": Node(name="word", children={word_a, word_b}, parent=None, words=set(words)),
            "word_a": Node(name="word_a", children=set(), parent="word", words={word_a}),
            "word_b": Node(name="word_b", children=set(), parent="word", words={word_b}),
        }
        expected_result = {word: set(words)}
        result = process_node(input_structure=input_structure, node=node_to_process)
        assert result == expected_result

    def test_one_leave_and_no_further_processing(self):
        word = "word_a_b_c"
        node_to_process = Node(name=word, children={"word_a"}, parent=None, words={word})
        input_structure = {
            "word": Node(name="word", children={"word_a"}, parent=None, words={word}),
            "word_a": Node(name="word_a", children={"word_a_b"}, parent="word_a", words={word}),
            "word_a_b": Node(name="word_a_b", children={"word_a_b_c"}, parent="word_a_b", words={word}),
            "word_a_b_c": Node(name="word_a_b_c", children=set(), parent="word_a_b", words={word}),
        }
        expected_result = {word: {word}}
        result = process_node(input_structure=input_structure, node=node_to_process)
        assert result == expected_result

    def test_one_leave_and_further_processing(self):
        words = ["word_a_b", "word_a_c", "word_a_c_d", "word_a_c_e"]
        word_a_b, word_a_c, word_a_c_d, word_a_c_e = words
        node_to_process = Node(name="word_a", children={word_a_b, word_a_c}, parent="word", words=set(words))
        input_structure = {
            "word": Node(name="word", children={"word_a"}, parent=None, words=set(words)),
            "word_a": Node(name="word_a", children={word_a_b, word_a_c}, parent="word", words=set(words)),
            word_a_b: Node(name=word_a_b, children=set(), parent="word_a", words={word_a_b}),
            word_a_c: Node(
                name=word_a_c,
                children={word_a_c_d, word_a_c_e},
                parent="word_a",
                words={word_a_c, word_a_c_e, word_a_c_d},
            ),
            word_a_c_e: Node(name=word_a_c_e, children=set(), parent=word_a_c, words={word_a_c_e}),
            word_a_c_d: Node(name=word_a_c_d, children=set(), parent=word_a_c, words={word_a_c_d}),
        }
        expected_result = {"word_a": set(words)}
        result = process_node(input_structure=input_structure, node=node_to_process)
        assert result == expected_result

    def test_one_leave_with_children_no_nodes_for_further_processing(self):
        word = "word_a_b_c"
        node_to_process = Node(name="word", children={"word_a"}, parent=None, words={word})
        input_structure = {
            "word": Node(name="word", children={"word_a"}, parent=None, words={word}),
            "word_a": Node(name="word_a", children={"word_a_b"}, parent="word", words={word}),
            "word_a_b": Node(name="word_a_b", children={word}, parent="word_a", words={word}),
            word: Node(name=word, children=set(), parent="word_a_b", words={word}),
        }
        expected_result = {word: {word}}
        result = process_node(input_structure=input_structure, node=node_to_process)
        assert result == expected_result

    def test_many_leaves_node_name_not_in_node_words_no_further_processing(self):
        words = ["word_a", "word_b", "word_c"]
        word_a, word_b, word_c = words
        node_to_process = Node(name="word", children={word_a, word_b, word_c}, parent=None, words=set(words))
        input_structure = {
            "word": Node(name="word", children={word_a, word_b, word_c}, parent=None, words=set(words)),
            word_a: Node(name=word_a, children=set(), parent="word", words={word_a}),
            word_b: Node(name=word_b, children=set(), parent="word", words={word_b}),
            word_c: Node(name=word_c, children=set(), parent="word", words={word_c}),
        }
        expected_result = {"word": set(words)}
        result = process_node(input_structure=input_structure, node=node_to_process)
        assert result == expected_result

    def test_many_leaves_node_name_in_node_words_further_processing(self):
        words = ["word_a", "word_b", "word_c_a", "word_c_b", "word_c_c"]
        word_a, word_b, word_c_a, word_c_b, word_c_c = words
        node_to_process = Node(name="word", children={word_a, word_b, "word_c"}, parent=None, words=set(words))
        input_structure = {
            "word": Node(name="word", children={word_a, word_b, "word_c"}, parent=None, words=set(words)),
            word_a: Node(name=word_a, children=set(), parent="word", words={word_a}),
            word_b: Node(name=word_b, children=set(), parent="word", words={word_b}),
            "word_c": Node(
                name="word_c",
                children={word_c_a, word_c_b, word_c_c},
                parent="word",
                words={word_c_a, word_c_b, word_c_c},
            ),
            word_c_a: Node(name=word_c_a, children=set(), parent="word_c", words={word_c_a}),
            word_c_b: Node(name=word_c_b, children=set(), parent="word_c", words={word_c_b}),
            word_c_c: Node(name=word_c_c, children=set(), parent="word_c", words={word_c_c}),
        }
        expected_result = {"word": {word_a, word_b}, "word_c": {word_c_a, word_c_b, word_c_c}}
        result = process_node(input_structure=input_structure, node=node_to_process)
        assert result == expected_result
