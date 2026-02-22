from tea_pot.sensors import TeaPotSensor


def test_operator_defers():
    operator = TeaPotSensor(task_id="test")
    
    with pytest.raises(TaskDeferred):
        x = operator.execute(context={})



def test_operator_execute_complete():

    operator = TeaPotSensor(task_id="test")
    
    event = {} 
    x = operator.execute(context={}, event=event)