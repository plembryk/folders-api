from groups.grouping import Node, process_structure


class TestProcessStructure:
    def test_process_structure_one_word(self):
        word = "word_a_b_c"
        input_structure = {
            "word": Node(name="word", children={"word_a"}, parent=None, words={word}),
            "word_a": Node(name="word_a", children={"word_a_b"}, parent="word_a", words={word}),
            "word_a_b": Node(name="word_a_b", children={"word_a_b_c"}, parent="word_a_b", words={word}),
            "word_a_b_c": Node(name="word_a_b_c", children=set(), parent="word_a_b", words={word}),
        }
        expected_result = {word: {word}}
        result = process_structure(input_structure=input_structure, words_list=[word], delimiter="_")
        assert result == expected_result

    def test_process_structure_words_with_the_same_prefix_resulting_in_one_group(self):
        words = ["word_a_b", "word_a_c", "word_a_c_d", "word_a_c_e"]
        word_a_b, word_a_c, word_a_c_d, word_a_c_e = words
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
        result = process_structure(input_structure=input_structure, words_list=words, delimiter="_")
        assert result == expected_result

    def test_process_structure_words_with_the_same_prefix_resulting_in_two_groups(self):
        words = ["word_a", "word_b", "word_c_a", "word_c_b", "word_c_c"]
        word_a, word_b, word_c_a, word_c_b, word_c_c = words
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
        result = process_structure(input_structure=input_structure, words_list=words, delimiter="_")
        assert result == expected_result

    def test_process_structure_words_with_the_different_prefixes(self):
        words_with_prefix_1 = {
            "prefix.1_prefix.2_word",
            "prefix.1_prefix.2_prefix.3_word",
            "prefix.1",
        }
        words_with_prefix_2 = {
            "prefix.2_prefix.3_word",
            "prefix.2_prefix.3_prefix.4_word",
            "prefix.2",
        }
        input_structure_prefix_1 = {
            "prefix.1": Node(
                name="prefix.1",
                children={"prefix.1_prefix.2"},
                parent=None,
                words=words_with_prefix_1,
            ),
            "prefix.1_prefix.2": Node(
                name="prefix.1_prefix.2",
                children={"prefix.1_prefix.2_word", "prefix.1_prefix.2_prefix.3"},
                parent="prefix.1",
                words={"prefix.1_prefix.2_word", "prefix.1_prefix.2_prefix.3_word"},
            ),
            "prefix.1_prefix.2_word": Node(
                name="prefix.1_prefix.2_word",
                children=set(),
                parent="prefix.1_prefix.2",
                words={"prefix.1_prefix.2_word"},
            ),
            "prefix.1_prefix.2_prefix.3": Node(
                name="prefix.1_prefix.2_prefix.3",
                children={"prefix.1_prefix.2_prefix.3_word"},
                parent="prefix.1_prefix.2",
                words={"prefix.1_prefix.2_prefix.3_word"},
            ),
            "prefix.1_prefix.2_prefix.3_word": Node(
                name="prefix.1_prefix.2_prefix.3_word",
                children=set(),
                parent="prefix.1_prefix.2_prefix.3",
                words={"prefix.1_prefix.2_prefix.3_word"},
            ),
        }
        input_structure_prefix_2 = {
            "prefix.2": Node(
                name="prefix.2",
                children={"prefix.2_prefix.3"},
                parent=None,
                words=words_with_prefix_2,
            ),
            "prefix.2_prefix.3": Node(
                name="prefix.2_prefix.3",
                children={"prefix.2_prefix.3_word", "prefix.2_prefix.3_prefix.4"},
                parent="prefix.2",
                words={"prefix.2_prefix.3_word", "prefix.2_prefix.3_prefix.4_word"},
            ),
            "prefix.2_prefix.3_word": Node(
                name="prefix.2_prefix.3_word",
                children=set(),
                parent="prefix.2_prefix.3",
                words={"prefix.2_prefix.3_word"},
            ),
            "prefix.2_prefix.3_prefix.4": Node(
                name="prefix.2_prefix.3_prefix.4",
                children={"prefix.2_prefix.3_prefix.4_word"},
                parent="prefix.2_prefix.3",
                words={"prefix.2_prefix.3_prefix.4_word"},
            ),
            "prefix.2_prefix.3_prefix.4_word": Node(
                name="prefix.2_prefix.3_prefix.4_word",
                children=set(),
                parent="prefix.2_prefix.3_prefix.4",
                words={"prefix.2_prefix.3_prefix.4_word"},
            ),
        }

        input_structure = {**input_structure_prefix_1, **input_structure_prefix_2}
        expected_result = {"prefix.1": words_with_prefix_1, "prefix.2": words_with_prefix_2}
        result = process_structure(
            input_structure=input_structure, words_list=words_with_prefix_1 | words_with_prefix_2, delimiter="_"
        )
        assert result == expected_result
