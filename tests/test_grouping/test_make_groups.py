from unittest.mock import patch

from groups.grouping import make_groups


def test_make_groups():
    words_list = ["word_a_b_c_d"]
    delimiter = "_"
    mocked_structure = {}

    with patch("groups.grouping.prepare_structure", return_value=mocked_structure) as prepare_structure_mock, patch(
        "groups.grouping.process_structure"
    ) as process_structure_mock:
        make_groups(words_list=words_list, delimiter=delimiter)

    prepare_structure_mock.assert_called_once_with(words_list=words_list, delimiter=delimiter)
    process_structure_mock.assert_called_once_with(
        input_structure=mocked_structure, delimiter=delimiter, words_list=words_list
    )
