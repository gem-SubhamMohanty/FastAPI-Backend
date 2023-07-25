import pytest
from app.calculations import add

@pytest.mark.parametrize("num1,num2,expected",[
    (3,4,7),
    (7,1,8),
    (12,4,16)
])
def test_add(num1, num2, expected):
    print("Testing add")
    assert add(num1,num2) == expected
