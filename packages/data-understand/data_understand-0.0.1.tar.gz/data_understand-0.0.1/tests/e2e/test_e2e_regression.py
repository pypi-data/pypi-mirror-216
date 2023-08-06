import uuid

import pandas as pd
import pytest
from rai_test_utils.datasets.tabular import (create_diabetes_data,
                                             create_energy_data,
                                             create_housing_data)

from .common import TestE2ECommon


@pytest.mark.e2e_tests()
class TestE2ERegression(TestE2ECommon):
    @pytest.mark.parametrize("dataset_name", ["diabetes", "housing", "energy"])
    @pytest.mark.parametrize("generate_jupyter_notebook", [True, False])
    @pytest.mark.parametrize("generate_pdf", [True, False])
    def test_e2e_regression(
        self, dataset_name, generate_jupyter_notebook, generate_pdf
    ):
        dataset_to_fixture_dict = {
            "diabetes": create_diabetes_data,
            "housing": create_housing_data,
            "energy": create_energy_data,
        }
        dataset = dataset_to_fixture_dict[dataset_name]
        X_train, X_test, y_train, y_test, feature_names = dataset()
        if not isinstance(X_train, pd.DataFrame):
            X_train = pd.DataFrame(data=X_train, columns=feature_names)

        X_train["target"] = y_train
        csv_file_name = dataset_name + str(uuid.uuid4()) + ".csv"
        X_train.to_csv(csv_file_name, index=False)

        self.execute_and_verify_data_understand(
            csv_file_name, generate_jupyter_notebook, generate_pdf
        )
