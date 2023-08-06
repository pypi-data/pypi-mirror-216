import sys
from io import StringIO

import pandas as pd

from data_understand.dataset_characteristics import (
    find_columns_having_missing_values, get_column_types_as_tuple,
    get_jupyter_nb_code_to_dataframe_head,
    get_jupyter_nb_code_to_dataframe_types,
    get_message_columns_having_missing_values)


class TestDatasetCharacteristics:
    def test_get_jupyter_nb_code_to_dataframe_types(self):
        markdown, code = get_jupyter_nb_code_to_dataframe_types()
        assert isinstance(markdown, str)
        assert isinstance(code, str)

    def test_get_jupyter_nb_code_to_dataframe_head(self):
        markdown, code = get_jupyter_nb_code_to_dataframe_head()
        assert isinstance(markdown, str)
        assert isinstance(code, str)

    def test_find_columns_having_missing_values(self):
        sys.stdout = StringIO()
        df_missing_values = pd.DataFrame(
            {"A": [1, None, 3], "B": [4, 5, None], "C": [4, 5, 9]}
        )
        find_columns_having_missing_values(df_missing_values)
        output = sys.stdout.getvalue()
        assert "The columns having missing values are: A,B" in output

        df_no_missing_values = pd.DataFrame(
            {"A": [1, 2, 3], "B": [4, 5, 5], "C": [4, 5, 9]}
        )
        find_columns_having_missing_values(df_no_missing_values)
        output = sys.stdout.getvalue()
        assert "No columns were found to have missing values" in output

    def test_get_message_columns_having_missing_values(self):
        df_missing_values = pd.DataFrame(
            {"A": [1, None, 3], "B": [4, 5, None], "C": [4, 5, 9]}
        )
        output = get_message_columns_having_missing_values(df_missing_values)
        assert "The columns having missing values are: A,B" in output

        df_no_missing_values = pd.DataFrame(
            {"A": [1, 2, 3], "B": [4, 5, 5], "C": [4, 5, 9]}
        )
        output = get_message_columns_having_missing_values(
            df_no_missing_values
        )
        assert "No columns were found to have missing values" in output

    def test_get_column_types_as_tuple(self):
        df = pd.DataFrame(
            {"A": [1, 2, 3], "B": [4, 5, 5], "C": ["a", "b", "c"]}
        )
        tuple_of_column_types = get_column_types_as_tuple(df)
        assert len(tuple_of_column_types) == 1 + len(df.columns)
        assert tuple_of_column_types[0][0] == "Column"
        assert tuple_of_column_types[0][1] == "Type"
