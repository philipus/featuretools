import numpy as np
from woodwork.column_schema import ColumnSchema
from featuretools.primitives.base.aggregation_primitive_base import AggregationPrimitive

class SumIf(AggregationPrimitive):
    """Calculates the sum of values that meet a specified condition.
    
    Parameters:
        condition (callable, optional): Function that takes an array and returns 
            a boolean mask. Default is lambda x: True (sum all values)
        condition_name (str, optional): Name for the condition used in feature names.
            Default is None.
    
    Examples:
        >>> from featuretools.primitives import SumIf
        >>> sum_if = SumIf(condition=lambda x: x > 0)
        >>> sum_if([1, -2, 3, -4, 5])
        9.0
        
        >>> # With named condition
        >>> positive_sum = SumIf(condition=lambda x: x > 0, condition_name="positive")
        >>> feature = Feature(df["value"], primitive=positive_sum)
        >>> feature.get_name()
        'SUM_IF(value, condition=positive)'
    """
    name = "sum_if"
    input_types = [ColumnSchema(semantic_tags={"numeric"})]
    return_type = ColumnSchema(semantic_tags={"numeric"})
    stack_on_self = False
    default_value = 0
    description_template = "the conditional sum of {}"
    
    def __init__(self, condition=None, condition_name=None, options=None):
        if options:
            self.condition = options.get("condition", lambda x: True)
            self.condition_name = options.get("condition_name")
        else:
            self.condition = condition or (lambda x: True)
            self.condition_name = condition_name
        super().__init__()
    
    def get_function(self):
        def sum_if_func(array):
            if len(array) == 0:
                return self.default_value
            array = np.array(array)
            mask = self.condition(array)
            return np.sum(array[mask])
        return sum_if_func
        
    def generate_name(self, base_feature_names, relationship_path_name, parent_dataframe_name, where_str, use_prev_str):
        base_features_str = ", ".join(base_feature_names)
        condition_str = f", condition={self.condition_name}" if self.condition_name else ""
        if relationship_path_name:
            return "%s(%s.%s%s%s%s)" % (
                self.name.upper(),
                relationship_path_name,
                base_features_str,
                where_str,
                use_prev_str,
                condition_str,
            )
        return "%s(%s%s%s%s)" % (
            self.name.upper(),
            base_features_str,
            where_str,
            use_prev_str,
            condition_str,
        )
        
    @classmethod
    def get_options(cls, options):
        """Handle primitive options for SumIf.
        
        Args:
            options (dict): Dictionary of options for the primitive.
            
        Returns:
            dict: Dictionary with condition and condition_name if present.
        """
        if not options:
            return {}
            
        result = {}
        if "condition" in options:
            result["condition"] = options["condition"]
        if "condition_name" in options:
            result["condition_name"] = options["condition_name"]
        return result 