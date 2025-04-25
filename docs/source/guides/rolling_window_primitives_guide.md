# Guide to Implementing Rolling Window Primitives

This guide outlines the process for implementing new rolling window primitives in Featuretools, based on the successful implementation of `RollingSum`. Follow these steps to create consistent and well-tested rolling primitives.

## 1. File Structure

Create your new primitive in `featuretools/primitives/standard/transform/time_series/` with the naming convention `rolling_[operation].py`. For example:
- `rolling_sum.py`
- `rolling_mean.py`
- `rolling_std.py`

## 2. Class Definition Template

```python
from featuretools.primitives import TransformPrimitive
from featuretools.primitives.standard.transform.time_series.utils import (
    apply_rolling_agg_to_series,
)

class Rolling[Operation](TransformPrimitive):
    """[Description of what the primitive does]"""
    
    name = "rolling_[operation]"
    input_types = [ColumnSchema(logical_type=Datetime, semantic_tags={"time_index"}),
                  ColumnSchema(logical_type=Numeric)]
    return_type = ColumnSchema(logical_type=Double)
    
    def __init__(self, window_length=3, gap=1, min_periods=1):
        self.window_length = window_length
        self.gap = gap
        self.min_periods = min_periods
        
    def get_function(self):
        def rolling_operation(datetime_col, numeric_col):
            series = pd.Series(numeric_col, index=datetime_col)
            return apply_rolling_agg_to_series(
                series,
                self.window_length,
                self.gap,
                self.min_periods,
                [your_aggregation_function],
                ignore_window_nans=True,
            )
        return rolling_operation
```

## 3. Key Components

### 3.1 Parameters
- `window_length`: Size of the rolling window (int or pandas offset string)
- `gap`: Distance between current row and window start (int or pandas offset string)
- `min_periods`: Minimum observations required for calculation

### 3.2 Required Methods
- `__init__`: Initialize parameters with sensible defaults
- `get_function`: Return the function that performs the rolling calculation

### 3.3 Utility Functions
Leverage existing utilities from `featuretools/primitives/standard/transform/time_series/utils.py`:
- `apply_rolling_agg_to_series`: Core rolling window logic
- `roll_series_with_gap`: Window creation with gap handling
- `apply_roll_with_offset_gap`: Offset-based window handling

## 4. Testing Requirements

Create tests in `featuretools/tests/primitive_tests/aggregation_primitive_tests/test_rolling_primitive.py`. Include:

### 4.1 Basic Functionality
```python
def test_rolling_[operation]_basic():
    # Test basic functionality with numeric window_length and gap
    pass

def test_rolling_[operation]_offset():
    # Test with string offset window_length and gap
    pass
```

### 4.2 Parameter Variations
```python
def test_rolling_[operation]_min_periods():
    # Test different min_periods values
    pass

def test_rolling_[operation]_window_length():
    # Test different window_length values
    pass
```

### 4.3 Edge Cases
```python
def test_rolling_[operation]_edge_cases():
    # Test NaN handling
    # Test empty series
    # Test single value
    pass
```

## 5. Common Pitfalls and Solutions

### 5.1 min_periods Handling
- Always treat `min_periods=0` the same as `min_periods=1`
- Ensure consistent behavior across all rolling primitives
- Test edge cases thoroughly

### 5.2 NaN Handling
- Set `ignore_window_nans=True` in `apply_rolling_agg_to_series`
- Test various combinations of NaN values
- Verify behavior matches pandas' rolling operations

### 5.3 Parameter Validation
- Handle both numeric and string offset parameters
- Validate parameter combinations
- Consider edge cases in parameter ranges

## 6. Best Practices

1. **Consistency**
   - Follow established patterns in existing primitives
   - Maintain uniform parameter handling
   - Use consistent documentation style

2. **Testing**
   - Cover all parameter combinations
   - Include both numeric and string offset tests
   - Test edge cases and NaN handling
   - Compare with pandas' native rolling functionality

3. **Documentation**
   - Include clear examples
   - Document parameter behavior
   - Note any special cases or limitations
   - Add type hints and docstrings

4. **Performance**
   - Leverage existing utility functions
   - Avoid redundant calculations
   - Consider memory usage with large windows

## 7. Example Implementation

See `RollingSum` implementation in `featuretools/primitives/standard/transform/time_series/rolling_sum.py` for a complete example.

## 8. Registration

Don't forget to:
1. Add the primitive to `__all__` in `featuretools/primitives/standard/transform/time_series/__init__.py`
2. Update relevant documentation
3. Add to appropriate test suites

## 9. Maintenance

When updating rolling primitives:
1. Update all related primitives for consistency
2. Run full test suite
3. Update documentation
4. Consider backward compatibility 