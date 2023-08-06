from data_understand.target_characteristics import \
    get_jupyter_nb_code_to_get_target


class TestTarget:
    def test_get_jupyter_nb_code_to_get_target(self):
        markdown, code = get_jupyter_nb_code_to_get_target("output")
        assert isinstance(markdown, str)
        assert isinstance(code, str)
        assert "output" in code
        assert "target_column" in code
