from tea_pot.operators import TeaPotOperator


def test_operator():
    operator = TeaPotOperator(task_id="test")
    x = operator.execute(context={})



