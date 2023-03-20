import json
import numpy as np

global quiz, ratio_options, option

with open('quiz.json', encoding='utf-8') as fh:
    quiz = json.load(fh)
    
ratio_options = {"1:5": 1/5, "1:2": 1/2,"1:3": 1/3, "1:4":1/4} 
option = np.random.choice(list(ratio_options))

template = '''
  {
        "question": "To build Voltage Divider with ratio %a_given you have chosen resistances R1=%R1 and R2=%R2. Please enter ratio you received:",
        "type": "numeric",
        "precision": 2,
        "answers": [
            {
                "type": "range",
                "range": [ %low, %high], 
                "correct": true,
                "feedback": "Correct"
            },
            {
                "type": "default",
                "feedback": "$a$ = %a_calc. Try choose other resistances."
            }
        ]
    }'''

def ratio_quiz(R1, R2):
    if R1 + R2 <= 0:
        return -1
    rq = template.replace('\n','')
    rq = rq.replace('%a_given', option)
    rq = rq.replace('%R1', str(R1))
    rq = rq.replace('%R2', str(R2))
    a_calc = R2/(R1+R2)
    a_given = ratio_options[option]
    low = a_given * 0.8
    high = a_given * 1.2
    rq = rq.replace('%low', str(low))
    rq = rq.replace('%high', str(high))
    rq = rq.replace('%a_calc', str(a_calc))

    return json.loads(rq)
