import uuid

import pandas as pd
import pytest
from rai_test_utils.datasets.tabular import (create_adult_census_data,
                                             create_cancer_data,
                                             create_iris_data,
                                             create_simple_titanic_data,
                                             create_wine_data)

from .common import TestE2ECommon


@pytest.mark.e2e_tests()
class TestE2EClassification(TestE2ECommon):
    @pytest.mark.parametrize(
        "dataset_name", ["iris", "titanic", "cancer", "wine", "adult"]
    )
    @pytest.mark.parametrize("generate_jupyter_notebook", [True, False])
    @pytest.mark.parametrize("generate_pdf", [True, False])
    def test_e2e_classification(
        self, dataset_name, generate_jupyter_notebook, generate_pdf
    ):
        dataset_to_fixture_dict = {
            "iris": create_iris_data,
            "cancer": create_cancer_data,
            "wine": create_wine_data,
            "titanic": create_simple_titanic_data,
            "adult": create_adult_census_data,
        }
        dataset = dataset_to_fixture_dict[dataset_name]

        if dataset_name == "adult":
            X_train, _, y_train, _, _ = dataset()
            feature_names = list(X_train.columns)
        else:
            X_train, _, y_train, _, feature_names, _ = dataset()
        if not isinstance(X_train, pd.DataFrame):
            X_train = pd.DataFrame(data=X_train, columns=feature_names)

        X_train["target"] = y_train
        csv_file_name = dataset_name + str(uuid.uuid4()) + ".csv"
        X_train.to_csv(csv_file_name, index=False)

        self.execute_and_verify_data_understand(
            csv_file_name, generate_jupyter_notebook, generate_pdf
        )
