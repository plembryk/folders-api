from groups.grouping import Node, prepare_structure


class TestPrepareStructure:
    def test_single_word(self):
        word = "word"
        structure = prepare_structure(words_list=[word], delimiter="_")
        expected_structure = {word: Node(name=word, children=set(), parent=None, words={word})}
        assert structure == expected_structure

    def test_single_word_delimited(self):
        word = "word_part-1_part-2"
        structure = prepare_structure(words_list=[word], delimiter="_")
        expected_structure = {
            "word": Node(
                name="word",
                children={"word_part-1"},
                parent=None,
                words={word},
            ),
            "word_part-1": Node(
                name="word_part-1",
                children={"word_part-1_part-2"},
                parent="word",
                words={word},
            ),
            "word_part-1_part-2": Node(
                name="word_part-1_part-2",
                children=set(),
                parent="word_part-1",
                words={word},
            ),
        }
        assert structure == expected_structure

    def test_words_with_common_prefix(self):
        words = {
            "prefix.1_prefix.2_word",
            "prefix.1_prefix.2_prefix.3_word",
            "prefix.1",
        }
        structure = prepare_structure(words_list=words, delimiter="_")
        expected_structure = {
            "prefix.1": Node(
                name="prefix.1",
                children={"prefix.1_prefix.2"},
                parent=None,
                words=words,
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
        assert structure == expected_structure

    def test_different_prefixes(self):
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
        structure = prepare_structure(words_list=words_with_prefix_1.union(words_with_prefix_2), delimiter="_")
        expected_structure_prefix_1 = {
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
        expected_structure_prefix_2 = {
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

        expected_structure = {**expected_structure_prefix_1, **expected_structure_prefix_2}

        assert structure == expected_structure
