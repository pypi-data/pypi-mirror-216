import numpy as np
import pandas as pd

from data_understand.feature_correlation import (
    get_feature_correlations_as_tuple,
    get_jupyter_nb_code_to_generate_correlation_matrices,
    get_jupyter_nb_code_to_get_negatively_correlated_feature_pairs,
    get_jupyter_nb_code_to_get_postively_correlated_feature_pairs,
    get_top_k_negatively_correlated_feature_pairs,
    get_top_k_postively_correlated_feature_pairs)
from data_understand.feature_correlation.correlation import _get_number_figures


class TestFeatureCorrelation:
    def test_get_number_figures(self):
        few_features_data = {
            "Name": ["John", "Anna", "Peter", "Linda"],
            "Age": [25, 30, 21, 40],
            "Gender": ["Male", "Female", "Male", "Female"],
            "Salary": [50000, 75000, 40000, 90000],
        }

        few_features_df = pd.DataFrame(few_features_data)

        assert 10 == _get_number_figures(few_features_df)

        more_features_data = {
            "Name": ["John", "Anna", "Peter", "Linda"],
            "Age": [25, 30, 21, 40],
            "Gender": ["Male", "Female", "Male", "Female"],
            "Salary": [50000, 75000, 40000, 90000],
            "Department": ["Sales", "Marketing", "Engineering", "Finance"],
            "Hire Date": [
                "2020-05-01",
                "2019-08-01",
                "2021-01-15",
                "2018-12-01",
            ],
            "Title": [
                "Sales Representative",
                "Marketing Manager",
                "Software Engineer",
                "Chief Financial Officer",
            ],
            "Location": ["New York", "Los Angeles", "Seattle", "Chicago"],
            "Experience": [2, 5, 1, 10],
            "Education": ["Bachelor", "Master", "Bachelor", "PhD"],
            "Language": ["English", "Spanish", "Java", "Python"],
            "Nationality": ["American", "German", "Chinese", "Canadian"],
        }

        more_features_df = pd.DataFrame(more_features_data)

        assert len(more_features_df.columns) == _get_number_figures(
            more_features_df
        )

    def test_get_jupyter_nb_code_to_generate_correlation_matrices(self):
        (
            markdown,
            code,
        ) = get_jupyter_nb_code_to_generate_correlation_matrices()
        assert isinstance(markdown, str)
        assert isinstance(code, str)

    def test_get_top_k_correlated_feature_pairs(self):
        np.random.seed(777)

        # Generate positively correlated features
        pos_corr_feat1 = np.random.normal(loc=10, scale=1, size=1000)
        pos_corr_feat2 = pos_corr_feat1 + np.random.normal(
            loc=0, scale=0.5, size=1000
        )
        pos_corr_df = pd.DataFrame(
            {"col1": pos_corr_feat1, "col2": pos_corr_feat2}
        )

        # Generate negatively correlated features
        neg_corr_feat1 = np.random.normal(loc=10, scale=1, size=1000)
        neg_corr_feat2 = neg_corr_feat1 - np.random.normal(
            loc=0, scale=0.5, size=1000
        )
        neg_corr_df = pd.DataFrame(
            {"col3": neg_corr_feat1, "col4": neg_corr_feat2}
        )

        # Concatenate the two dataframes
        df = pd.concat([pos_corr_df, neg_corr_df], axis=1)

        positively_correlated_df = (
            get_top_k_postively_correlated_feature_pairs(df, 5)
        )
        assert len(positively_correlated_df) > 0
        assert np.all(positively_correlated_df["correlation"].values > 0.0)

        negatively_correlated_df = (
            get_top_k_negatively_correlated_feature_pairs(df, 5)
        )
        assert len(negatively_correlated_df) > 0
        assert np.all(negatively_correlated_df["correlation"].values < 0.0)

    def test_get_jupyter_nb_code_negatively_correlated_feature_pairs(self):
        (
            markdown,
            code,
        ) = get_jupyter_nb_code_to_get_negatively_correlated_feature_pairs()
        assert isinstance(markdown, str)
        assert isinstance(code, str)
        assert "negative" in markdown

    def test_get_jupyter_nb_code_positively_correlated_feature_pairs(self):
        (
            markdown,
            code,
        ) = get_jupyter_nb_code_to_get_postively_correlated_feature_pairs()
        assert isinstance(markdown, str)
        assert isinstance(code, str)
        assert "positive" in markdown

    def test_get_feature_correlations_as_tuple(self):
        np.random.seed(777)

        # Generate positively correlated features
        pos_corr_feat1 = np.random.normal(loc=10, scale=1, size=1000)
        pos_corr_feat2 = pos_corr_feat1 + np.random.normal(
            loc=0, scale=0.5, size=1000
        )
        pos_corr_df = pd.DataFrame(
            {"col1": pos_corr_feat1, "col2": pos_corr_feat2}
        )

        # Generate negatively correlated features
        neg_corr_feat1 = np.random.normal(loc=10, scale=1, size=1000)
        neg_corr_feat2 = neg_corr_feat1 - np.random.normal(
            loc=0, scale=0.5, size=1000
        )
        neg_corr_df = pd.DataFrame(
            {"col3": neg_corr_feat1, "col4": neg_corr_feat2}
        )

        # Concatenate the two dataframes
        df = pd.concat([pos_corr_df, neg_corr_df], axis=1)

        correlations = get_feature_correlations_as_tuple(df, 5, True)
        assert len(correlations) >= 1
        assert correlations[0][0] == "feature1"
        assert correlations[0][1] == "feature2"
        assert correlations[0][2] == "correlation"
