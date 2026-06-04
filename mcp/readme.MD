# tool 전달 형태
```
name='add' 
title=None 
description='\n    두 수를 더하는 계신기\n\n    Args:\n        a: 첫 번째 수치\n        b: 두 번째 수치\n    \n    Returns\n        계산 결과\n    ' 

inputSchema={
    'properties': {
        'a': {'title': 'A', 'type': 'number'}, 
        'b': {'title': 'B', 'type': 'number'}}, 
    'required': ['a', 'b'], 
    'title': 'addArguments', 
    'type': 'object'
} 

outputSchema={
    'properties': {
        'result': {'title': 'Result', 'type': 'string'}
    }, 
    'required': ['result'], 
    'title': 'addOutput', 
    'type': 'object'
} 

icons=None 
annotations=None 
meta=None 
execution=None
```