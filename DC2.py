import json
import numpy as np
global quiz, ratio_options, option

# a constant to compare values aVALUE +- ERROR
ERROR = 0.1 

with open('quiz.json', encoding='utf-8') as fh:
    quiz = json.load(fh)
    
ratio_options = {"1:5": 1/5, "1:2": 1/2,"1:3": 1/3, "1:4":1/4} 
option = np.random.choice(list(ratio_options))

template = '''
[
    {
        "question": "To build Voltage Divider with ratio %variant you have chosen resistances R1=%R1 Ohm and R2=%R2 Ohm. Check if it is correct:",
        "type": "multiple_choice",
        "answers": [
            {
                "answer": "בודק",
                "correct": "%correct",
                "feedback": "%feedback"
            }
        ]
    }
,

    {
        "question": "What Voltage Divider ratio did you actually received?",
        "type": "numeric",
        "precision": 2,
        "answers": [
            {
                "type": "range",
                "range": ["%low", "%high"], 
                "correct": true,
                "feedback": "נכון! מצויין!"
            },
            {
                "type": "default",
                "correct": false,                
                "feedback": "You should get ratio $a = R_2 / (R_1+R_2)$  ±10%."
            }
        ]
    }
]
'''

def ratio_quiz(R1, R2):
    if R1 + R2 <= 0:
        return -1

    a_built = R2/(R1+R2) # a theoretical ratio according to Rs chosen
    a_given = ratio_options[option]
    rq = template
    rq = rq.replace('\n','')
    rq = rq.replace('%variant', "{:s}".format(option))
    rq = rq.replace('%R1', "{:d}".format(R1))
    rq = rq.replace('%R2', "{:d}".format(R2))
    low = a_built * (1 - ERROR)
    high = a_built * (1 + ERROR)
    rq = rq.replace('%low', str(low))
    rq = rq.replace('%high', str(high))
    rq = rq.replace('%a_build', "{:.2f}".format(a_built))

    # question 1: check if R1 and R2 were chosen correct
     
    # if a_chosen is close enough to a_given then answer is correct
    # close enough is interval +- 10%
    
    if (a_given * (1 - ERROR) < a_built) and (a_built < a_given *(1 + ERROR)):
        rq = rq.replace('%correct', 'true')
        rq = rq.replace('%feedback', '"נכון!"')
    else:
        rq = rq.replace('%correct', 'false')
        rq = rq.replace('%feedback', "No... You will get ratio $a = {R_2 / (R_1+R_2)}$ =" + "{:.2f}".format(a_built))
    return json.loads(rq)