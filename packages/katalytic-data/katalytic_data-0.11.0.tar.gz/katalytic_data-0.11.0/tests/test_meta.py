import pytest as pytest
from katalytic.data import all_types_besides
from katalytic.data.meta import reference_caller_function, reference_current_function


def _f0(depth): return reference_caller_function(depth=depth)
def _f1(depth): return _f0(depth)
def _f2(depth): return _f1(depth)


class Test_reference_caller_function:
    @pytest.mark.parametrize('caller, depth, expected', [
        (_f1, 0, _f0),
        (_f1, 1, _f1),
        (_f2, 0, _f0),
        (_f2, 1, _f1),
        (_f2, 2, _f2),
    ])
    def test_depth_ok(self, caller, depth, expected):
        assert caller(depth=depth) == expected

    def test_precondition_depth_should_be_positive(self):
        with pytest.raises(ValueError):
            _f1(-1)

    def test_depth_should_not_be_larger_than_the_stack(self):
        with pytest.raises(ValueError):
            # Use a large number because of the pytest internal calls
            _f1(100)

    @pytest.mark.parametrize('depth', all_types_besides('int'))
    def test_precondition_depth_should_be_an_integer(self, depth):
        with pytest.raises(TypeError):
            _f1(depth)


class Test_reference_current_function:
    def test_should_be_equivalent_to_reference_caller_function_with_depth_0(self):
        current = reference_current_function()
        caller = reference_caller_function(depth=0)

        assert current is not None
        assert current is caller
