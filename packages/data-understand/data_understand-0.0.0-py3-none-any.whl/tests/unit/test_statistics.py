from data_understand.dataset_characteristics import (
    get_jupyter_nb_code_to_dataframe_head,
    get_jupyter_nb_code_to_dataframe_types)


class TestDatasetCharacteristics:
    def test_get_jupyter_nb_code_to_dataframe_head(self):
        markdown, code = get_jupyter_nb_code_to_dataframe_head()
        assert isinstance(markdown, str)
        assert isinstance(code, str)

    def test_get_jupyter_nb_code_to_dataframe_types(self):
        markdown, code = get_jupyter_nb_code_to_dataframe_types()
        assert isinstance(markdown, str)
        assert isinstance(code, str)
