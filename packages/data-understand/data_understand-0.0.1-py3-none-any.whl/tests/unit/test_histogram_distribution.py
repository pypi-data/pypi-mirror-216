from data_understand.value_distributions import \
    get_jupyter_nb_code_to_generate_histogram_distributions


class TestHistogramDistribution:
    def test_get_jupyter_nb_code_to_generate_histogram_distributions(self):
        (
            markdown,
            code,
        ) = get_jupyter_nb_code_to_generate_histogram_distributions()
        assert isinstance(markdown, str)
        assert isinstance(code, str)
