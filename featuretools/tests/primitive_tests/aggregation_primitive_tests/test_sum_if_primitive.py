import numpy as np
import pandas as pd
import pytest
from featuretools.primitives.standard.aggregation.sum_if_primitive import SumIf

def test_sum_if_primitive():
    # Test case 1: Basic sum if condition
    primitive = SumIf(condition=lambda x: x > 0)
    values = pd.Series([-1, 2, -3, 4, 5])
    expected = 11  # 2 + 4 + 5
    assert primitive.get_function()(values) == expected

    # Test case 2: Sum if condition with all values meeting condition
    primitive = SumIf(condition=lambda x: x > -10)
    values = pd.Series([1, 2, 3, 4, 5])
    expected = 15  # 1 + 2 + 3 + 4 + 5
    assert primitive.get_function()(values) == expected

    # Test case 3: Sum if condition with no values meeting condition
    primitive = SumIf(condition=lambda x: x > 10)
    values = pd.Series([1, 2, 3, 4, 5])
    expected = 0  # No values > 10
    assert primitive.get_function()(values) == expected

    # Test case 4: Sum if condition with empty series
    primitive = SumIf(condition=lambda x: x > 0)
    values = pd.Series([])
    expected = 0  # Empty series should return 0
    assert primitive.get_function()(values) == expected

    # Test case 5: Sum if condition with NaN values
    primitive = SumIf(condition=lambda x: x > 0)
    values = pd.Series([1, np.nan, 3, np.nan, 5])
    expected = 9  # 1 + 3 + 5 (NaN values ignored)
    assert primitive.get_function()(values) == expected

def test_sum_if_primitive_with_custom_condition_name():
    # Test case with custom condition name
    primitive = SumIf(condition=lambda x: x > 0, condition_name="positive_values")
    assert primitive.condition_name == "positive_values"
    values = pd.Series([-1, 2, -3, 4, 5])
    expected = 11  # 2 + 4 + 5
    assert primitive.get_function()(values) == expected

def test_sum_if_primitive_with_complex_condition():
    # Test case with complex condition
    primitive = SumIf(condition=lambda x: (x > 0) & (x % 2 == 0))
    values = pd.Series([-2, 1, 2, 3, 4, 5, 6])
    expected = 12  # 2 + 4 + 6
    assert primitive.get_function()(values) == expected 