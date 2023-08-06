import pandas as pd

from data_understand.value_distributions import \
    get_jupyter_nb_code_to_generate_cat_frequency_distributions
from data_understand.value_distributions.cat_frequency_distribution import \
    _generate_cat_frequency


class TestCategoricalFrequencyDistribution:
    def test_generate_cat_frequency(self):
        df = pd.DataFrame(
            {
                "category": ["A", "A", "B", "C", "C", "C"],
                "numeric": [1, 2, 3, 4, 5, 6],
            }
        )
        value_counts_dict = _generate_cat_frequency(df)
        assert "category" in value_counts_dict
        assert isinstance(value_counts_dict["category"], pd.Series)
        assert "numeric" not in value_counts_dict

    def test_get_jupyter_nb_code_to_generate_cat_frequency_distributions(
        self,
    ):
        (
            markdown,
            code,
        ) = get_jupyter_nb_code_to_generate_cat_frequency_distributions()
        assert isinstance(markdown, str)
        assert isinstance(code, str)
