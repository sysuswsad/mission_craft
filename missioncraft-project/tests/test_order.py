import os
import json
import pytest
from werkzeug.security import check_password_hash
# from werkzeug import FileStorage
from werkzeug.datastructures import FileStorage

from app.db import get_db
from tests.test_user import get_token_auth_headers


# @pytest.mark.parametrize(('username', 'password', 'status_code', 'message', 'data'), (
#     ('pj', '123456', 200, 'return successfully', {'orders': [
#     {'order_id':1, 'receiver_id':3,'publisher_id':1,'order_state':0,'publisher_confirm':1,'receiver_confirm':1,'finish_time':'2019-06-08 12:12:12','receive_time':'2019-06-08 12:12:12'},
#     {'order_id':2, 'receiver_id':3,'publisher_id':1,'order_state':0,'publisher_confirm':1,'receiver_confirm':1,'finish_time':None,'receive_time':'2019-06-08 12:12:12'}]}),
#     ('pj2', '123456', 200, 'return successfully', {'orders': []}),

# ))
# def test_get_order(client, app, username, password, status_code, message, data):
#     response = client.get('api/order/',headers=get_token_auth_headers(client, app, username, password))
#     assert response
#     assert response.status_code == status_code
#     response_data = json.loads(response.get_data(as_text=True))
#     assert response_data.get('message') == message
#     if(response.status_code == 200):  
#         assert response_data.get('data') == data


# @pytest.mark.parametrize(('username', 'password', 'status_code', 'message', 'order_id', 'mission_id', 'state', 'rcv_num'), (
#     ('pj', '123456', 201,'Create order successfully', 3, 1, 0, 2),
#     ('pj', '123456', 400,'mission_id is invalid', 3, 100, 0, 2),
#     ('pj', '123456', 201, 'Create order successfully', 3, 2, 1, 100),
#     ('pj', '123456', 400,'Mission is closed', 3, 3, 1, 100),
#     ('pj', '123456', 400,'Mission is closed', 3, 4, 1, 50),
#     ('pj', '123456', 400,'mission reached its dealine', 3, 5, 1, 50),
#     ('pj', '123456', 201,'Create order successfully', 3, 6, 1, 1),
#     ('pj', '123456', 400,'Mission is closed', 3, 7, 1, 1),
#     ('pj', '123456', 400,'Mission is closed', 3, 8, 1, 0),
#     ('pj', '123456', 400,'mission reached its dealine', 3, 9, 1, 0)
# ))
# def test_create_order(client, app, username, password, status_code, message, order_id, mission_id, state, rcv_num):
#     response = client.post('api/order/',headers=get_token_auth_headers(client, app, username, password),data=json.dumps({'mission_id':mission_id}))
#     assert response
#     #assert response.status_code == status_code
#     response_data = json.loads(response.get_data(as_text=True))
#     assert response_data.get('message') == message
#     if(response.status_code == 201):  
#         assert response_data.get('data')['order_id'] == order_id
#     if(mission_id == 100):
#         return
#     with app.app_context():
#         mission = get_db().execute('SELECT * FROM MissionInfo  WHERE idMissionInfo = ?', (mission_id,)).fetchone()
#         assert mission
#         assert mission['state'] == state
#         assert mission['rcv_num'] == rcv_num


@pytest.mark.parametrize(('username', 'password', 'order_id', 'answers', 'status_code', 'message', 'finish_number', 'state_num'), (
    ('pj', '123456', None, None, 400, 'Parse order id error', None, None),
    ('pj', '123456', 100000, None, 400, 'No such mission', None, None),
    ('pj', '123456', 3, None, 400, 'The order has been confirmed', None, None),
    ('test1', '123456', 4, None, 403, 'You can not submit for other receivers', None, None),
    ('test1', '123456', 5, json.dumps({'test':'test'}), 400, 'Parse answers error', None, None),
    ('test1', '123456', 6, json.dumps([0,[0,1],'test']), 200, 'Confirm order successfully', 2, 0.2),
    ('test10', '123456', 7, None, 200, 'You can not submit for other publishers', None, None),
    ('test1', '123456', 7, None, 200, 'Confirm order successfully', 1, 1),
))
def test_confirm_order(client, app, username, password, order_id, answers, status_code, message, finish_number, state_num):
    response = client.put('api/order/',headers=get_token_auth_headers(client, app, username, password),data=json.dumps({
        'order_id':order_id, 'answers':answers}))
    # assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message
    if response.status_code == 200:
        with app.app_context():
            db = get_db()
            order_info = db.execute(
                'SELECT mission_id, receiver_id, publisher_confirm, receiver_confirm, order_state FROM MissionOrder WHERE idMissionOrder = ?', (order_id,)
            ).fetchone()
            assert order_info['publisher_confirm'] == 1
            assert order_info['receiver_confirm'] == 1
            assert order_info['order_state'] == 1

            assert db.execute(
                'SELECT mission_fin_num FROM User WHERE idUser = ?', (order_info['receiver_id'],)
            ).fetchone()['mission_fin_num'] == 1

            assert db.execute(
                'SELECT fin_num FROM MissionInfo WHERE idMissionInfo = ?', (order_info['mission_id'],)
            ).fetchone()['fin_num'] == finish_number
            assert db.execute(
                'SELECT state FROM MissionInfo WHERE idMissionInfo = ?', (order_info['mission_id'],)
            ).fetchone()['state'] == state_num
        with app.app_context():
            db = get_db()
            order_info = db.execute(
                'SELECT mission_id FROM MissionOrder WHERE idMissionOrder = ?', (order_id,)
            ).fetchone()
            problem_ids = db.execute(
                'SELECT idProblem FROM Problem WHERE mission_id = ?', (order_info['mission_id'],)
            ).fetchall()
            for i in range(0, len(problem_ids)):
                answer = db.execute(
                    'SELECT result from Answer WHERE problem_id = ? AND order_id = ?', (problem_ids[i]['idProblem'], order_id)
                ).fetchone()['result']
                assert json.loads(answers)[i] == json.loads(answer)
