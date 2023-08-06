import os
from argparse import Namespace

import pandas as pd
import pytest
from raiutils.exceptions import UserErrorException

from data_understand.input_validations import validate_input_parameters


@pytest.fixture()
def args():
    return Namespace(file_name="test_file.csv", target_column="target")


class TestInputValidations:
    def test_valid_input_parameters(self, args):
        # Create a test CSV file and add a target column
        test_df = pd.DataFrame(
            {"col1": [1, 2, 3], "col2": [4, 5, 6], "target": [0, 1, 0]}
        )
        test_df.to_csv(args.file_name, index=False)

        # Test the function with valid input parameters
        assert validate_input_parameters(args) is None

        # Remove the test file
        os.remove(args.file_name)

    def test_missing_file_name(self, args):
        args.file_name = None
        with pytest.raises(
            UserErrorException,
            match="A valid file name None is required. "
            "Please provide a valid file path.",
        ):
            validate_input_parameters(args)

    def test_missing_target_column(self, args):
        args.target_column = None
        with pytest.raises(
            UserErrorException, match="A valid target column name is required."
        ):
            validate_input_parameters(args)

    def test_nonexistent_file_name(self, args):
        args.file_name = "nonexistent_file.csv"
        with pytest.raises(
            UserErrorException,
            match="The file nonexistent_file.csv doesn't exists.",
        ):
            validate_input_parameters(args)

    def test_non_csv_file_name(self, args):
        args.file_name = "test_file.txt"
        with pytest.raises(
            UserErrorException,
            match="The file test_file.txt is not a CSV file. "
            "Please provide a CSV file.",
        ):
            validate_input_parameters(args)

    def test_invalid_csv_file(self, args):
        # Create a test file with invalid CSV format
        with open(args.file_name, "w") as f:
            f.write("col1,col2,col3\n1,2,3\n4,5\n7,8,9,10")

        with pytest.raises(
            UserErrorException,
            match=f"Unable to read CSV file {args.file_name} as "
            "a pandas DataFrame",
        ):
            validate_input_parameters(args)

        # Remove the test file
        os.remove(args.file_name)

    def test_nonexistent_target_column(self, args):
        # Create a test CSV file without a target column
        test_df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
        test_df.to_csv(args.file_name, index=False)

        with pytest.raises(
            UserErrorException,
            match="The target column name target doesn't exist in dataset.",
        ):
            validate_input_parameters(args)

        # Remove the test file
        os.remove(args.file_name)
