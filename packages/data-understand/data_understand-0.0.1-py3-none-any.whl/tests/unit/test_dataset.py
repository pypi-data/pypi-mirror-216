from data_understand.load_dataset import \
    get_jupyter_nb_code_to_read_as_dataframe


class TestLoadDataset:
    def test_get_jupyter_nb_code_to_read_as_dataframe(self):
        markdown, code = get_jupyter_nb_code_to_read_as_dataframe("fake_name")
        assert isinstance(markdown, str)
        assert isinstance(code, str)
        assert "fake_name" in code
