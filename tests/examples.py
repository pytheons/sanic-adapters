def top_level_function():
    return True

def top_level_function_with_nested_function():
    def second_level_function():
        return True

    return second_level_function

def nested_3_layers_function():
    def nested_2_level_function():
        def nested_3_level_function():
            return True
        return nested_3_level_function
    return nested_2_level_function()

class Examples(object):
    def class_method(self):
        return f"{self.__class__.__name__}"

    def class_method_with_nested_function(self):
        def wrapper():
            return f"{self.__class__.__name__}"

        return wrapper

    def class_method_with_nested_class(self):
        class NestedClass:
            def nested_method_in_nested_class(self):
                return f"{self.__class__.__name__}"

        return NestedClass.nested_method_in_nested_class

    def class_method_with_nested_class_with_nested_function(self):
        class NestedClassWithNestedFunction:
            def nested_method_in_nested_class_with_nested_function(self):
                def wrapper():
                    return f"{self.__class__.__name__}"
                return wrapper

        return NestedClassWithNestedFunction().nested_method_in_nested_class_with_nested_function()