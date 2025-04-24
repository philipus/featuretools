# SumIf Primitive Development Guide

## Purpose
The `SumIf` primitive extends Featuretools' aggregation capabilities by allowing conditional summation based on user-defined criteria. It enables users to:
- Sum values that meet specific conditions (e.g., positive values only)
- Apply complex conditions (e.g., values within a range)
- Generate meaningful feature names that include condition descriptions

## Implementation Location
The primitive was implemented in:
```
featuretools/primitives/standard/aggregation/sum_if_primitive.py
```

## Class Structure
```python
class SumIf(AggregationPrimitive):
    name = "sum_if"
    input_types = [ColumnSchema(semantic_tags={"numeric"})]
    return_type = ColumnSchema(semantic_tags={"numeric"})
    stack_on_self = False
    default_value = 0
    description_template = "the sum of {} where {}"
```

### Extending AggregationPrimitive
The class extends `AggregationPrimitive` by:
1. Defining input/output types using `ColumnSchema`
2. Implementing `get_function()` for the core aggregation logic
3. Overriding `generate_name()` to include condition information
4. Adding custom parameters (`condition` and `condition_name`)

## Testing Strategy
Tests were implemented in:
```
featuretools/tests/primitive_tests/test_agg_feats.py
```

### Test Categories
1. **Basic Functionality**
   - Simple conditions (e.g., x > 0)
   - Empty input handling
   - Default value behavior

2. **Complex Conditions**
   - Multiple conditions (e.g., x > 0 & x < 4)
   - Edge cases and boundary conditions

3. **DFS Integration**
   - Feature name generation
   - EntitySet relationship handling
   - Primitive instantiation and usage

## Development Challenges & Solutions

### 1. Condition Handling
**Issue**: Lambda functions in feature names
- Initial implementation showed raw lambda functions in feature names
- Made feature names unreadable and inconsistent

**Solution**:
- Added `condition_name` parameter
- Modified `generate_name()` to use descriptive names
- Result: `SUM_IF(column, condition=positive)` instead of `SUM_IF(column, condition=<lambda>)`

### 2. DFS Integration
**Issue**: Primitive options not propagating
- Attempted to use `primitive_options` in DFS
- Options weren't being properly passed to primitive instances

**Solution**:
- Created pre-configured primitive instances
- Passed instances directly to DFS
- Example:
```python
sum_if = SumIf(condition=lambda x: x > 0, condition_name="positive")
feature_matrix, features = ft.dfs(
    entityset=es,
    target_dataframe_name="customers",
    agg_primitives=[sum_if]
)
```

### 3. EntitySet Setup
**Issue**: Incorrect relationship direction
- Initially tried to create relationship from child to parent
- Caused errors in feature calculation

**Solution**:
- Created parent dataframe first
- Added child dataframe with proper index
- Established relationship from parent to child
```python
es.add_dataframe(dataframe_name="customers", dataframe=customers_df, index="id")
es.add_dataframe(dataframe_name="transactions", dataframe=transactions_df, index="id")
es.add_relationship("customers", "id", "transactions", "customer_id")
```

## Lessons for Future Primitive Development

### 1. Primitive Design
- Always include descriptive parameters for customization
- Consider how parameters will appear in feature names
- Design for both simple and complex use cases

### 2. Testing
- Test both primitive-level and DFS-level functionality
- Include edge cases and error conditions
- Verify feature name generation
- Test with different data types and structures

### 3. DFS Integration
- Prefer primitive instances over primitive options
- Document proper usage patterns
- Consider how primitives interact with other features

### 4. Documentation
- Include clear examples of both simple and complex usage
- Document parameter behavior and defaults
- Provide common use cases and patterns

### 5. Error Handling
- Implement clear error messages for invalid inputs
- Handle edge cases gracefully
- Consider performance implications

## Best Practices for Custom Primitives

1. **Start with a clear use case**
   - Define the problem being solved
   - Identify target users and their needs

2. **Design for flexibility**
   - Allow customization through parameters
   - Support both simple and complex use cases

3. **Test thoroughly**
   - Unit tests for core functionality
   - Integration tests with DFS
   - Edge cases and error conditions

4. **Consider performance**
   - Optimize for large datasets
   - Handle missing values appropriately
   - Consider memory usage

5. **Document clearly**
   - Usage examples
   - Parameter descriptions
   - Common patterns and anti-patterns

## Future Improvements

1. **Enhanced Condition Support**
   - Multiple conditions
   - String-based conditions
   - Custom condition types

2. **Performance Optimization**
   - Vectorized operations
   - Parallel processing support
   - Memory efficiency

3. **Extended Functionality**
   - Additional aggregation types
   - Custom aggregation functions
   - Integration with other primitives 