import json
import numpy as np
global quiz, ratio_options, option

# a constant to compare values aVALUE +- ERROR
ERROR = 0.1 

with open('quiz.json', encoding='utf-8') as fh:
    quiz = json.load(fh)
    
ratio_options = {"1:5": 1/5, "1:2": 1/2,"1:3": 1/3, "1:4":1/4} 
option = np.random.choice(list(ratio_options))


def update_quiz(R1, R2):
        
    if R1 + R2 <= 0:
       print('Error: R1 + R2 should be greater that 0.')
       return -1

    with open('quiz.json', encoding='utf-8') as fh:
        quiz = json.load(fh)    
    
    q = quiz[8:]
    
    a_built = R2/(R1+R2) # a theoretical ratio according to Rs chosen
    a_given = ratio_options[option]
    s = q[0]['question']
    s = s.replace('%variant', "{:s}".format(option))
    s = s.replace('%R1', "{:.1f}".format(R1))
    s = s.replace('%R2', "{:.1f}".format(R2))
    q[0]['question'] = s
    
    # if a_chosen is close enough to a_given then answer is correct
    # close enough is interval +- 10%
    
    if (a_given * (1 - ERROR) < a_built) and (a_built < a_given *(1 + ERROR)):
        q[0]['answers'][0]['correct'] = True        
        q[0]['answers'][0]['feedback'] = "נכון!"        
    else:
        q[0]['answers'][0]['correct'] = False
        s = q[0]['answers'][0]['feedback']
        s = s.replace('%a', "{:.2f}".format(a_built))
        q[0]['answers'][0]['feedback'] = s         
    
    low = a_built * (1 - ERROR)
    high = a_built * (1 + ERROR)
    q[1]['answers'][0]['range'][0] = "{:f}".format(low)
    q[1]['answers'][0]['range'][1] = "{:f}".format(high)
    q[1]['answers'][1]['feedback'].replace('%a_build', "{:.2f}".format(a_built))

      
    return q