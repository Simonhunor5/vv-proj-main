import calculator


def test_calc_addition():
    output = calculator.add(1, 2)
    assert output == 3


def test_calc_substraction():
    output = calculator.substract(3, 1)
    assert output == 2


def test_calc_multiply():
    output = calculator.multiply(2, 3)
    assert output == 6

def test_calc_divide():
    output = calculator.divide(6,3)
    assert output == 2

    output1 = calculator.divide(5,2)
    assert output1 == 2.5