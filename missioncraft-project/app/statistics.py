from app.db import get_db
import json

def statistics_ana(pro_type, choices, problem_id):
    choices = json.loads(choices)
    db = get_db()
    if pro_type == 0:
        answer = [0]*len(choices)
        for row in db.execute(
            'SELECT result from Answer WHERE problem_id = ?', (problem_id,)
        ).fetchall():
            answer[json.loads(row['result'])] = answer[json.loads(row['result'])] + 1
    # 考虑到多选题也可以通过mission查询中的fin_num知道问题的回答人数，所以这里就不专门设置回答人数了，只设置回答的答案
    elif pro_type == 1:
        answer = [0]*len(choices)
        for row in db.execute(
            'SELECT result from Answer WHERE problem_id = ?', (problem_id,)
        ).fetchall():
            for item in json.loads(row['result']):
                answer[item] = answer[item] + 1
    else:
        answer = []
        for row in db.execute(
            'SELECT result from Answer WHERE problem_id = ?', (problem_id,)
        ).fetchall():
            answer.append(json.loads(row['result']))
    return answer
