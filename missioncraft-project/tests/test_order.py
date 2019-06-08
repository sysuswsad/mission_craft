import os
import json
import pytest
from werkzeug.security import check_password_hash
# from werkzeug import FileStorage
from werkzeug.datastructures import FileStorage

from app.db import get_db
from tests.test_user import get_token_auth_headers


@pytest.mark.parametrize(('username', 'password', 'status_code', 'message', 'data'), (
    ('pj', '123456', 200, 'return successfully', {'orders': [
    {'order_id':1, 'receiver_id':3,'publisher_id':1,'order_state':0,'publisher_confirm':1,'receiver_confirm':1,'finish_time':'2019-06-08 12:12:12','receive_time':'2019-06-08 12:12:12'},
    {'order_id':2, 'receiver_id':3,'publisher_id':1,'order_state':0,'publisher_confirm':1,'receiver_confirm':1,'finish_time':None,'receive_time':'2019-06-08 12:12:12'}]}),
    ('pj2', '123456', 200, 'return successfully', {'orders': []}),

))
def test_get_order(client, app, username, password, status_code, message, data):
    response = client.get('api/order/',headers=get_token_auth_headers(client, app, username, password))
    assert response
    assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message
    if(response.status_code == 200):  
        assert response_data.get('data') == data

@pytest.mark.parametrize(('username', 'password', 'status_code', 'message', 'order_id', 'mission_id', 'state', 'rcv_num'), (
    ('pj', '123456', 201,'Create order successfully', 3, 1, 0, 2),
    ('pj', '123456', 400,'mission_id is invalid', 3, 100, 0, 2),
    ('pj', '123456', 201, 'Create order successfully', 3, 2, 1, 100),
    ('pj', '123456', 400,'Mission is closed', 3, 3, 1, 100),
    ('pj', '123456', 400,'Mission is closed', 3, 4, 1, 50),
    ('pj', '123456', 400,'mission reached its dealine', 3, 5, 1, 50),
    ('pj', '123456', 201,'Create order successfully', 3, 6, 1, 1),
    ('pj', '123456', 400,'Mission is closed', 3, 7, 1, 1),
    ('pj', '123456', 400,'Mission is closed', 3, 8, 1, 0),
    ('pj', '123456', 400,'mission reached its dealine', 3, 9, 1, 0)
))
def test_create_order(client, app, username, password, status_code, message, order_id, mission_id, state, rcv_num):
    response = client.post('api/order/',headers=get_token_auth_headers(client, app, username, password),data=json.dumps({'mission_id':mission_id}))
    assert response
    #assert response.status_code == status_code
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get('message') == message
    if(response.status_code == 201):  
        assert response_data.get('data')['order_id'] == order_id
    if(mission_id == 100):
        return
    with app.app_context():
        mission = get_db().execute('SELECT * FROM MissionInfo  WHERE idMissionInfo = ?', (mission_id,)).fetchone()
        assert mission
        assert mission['state'] == state
        assert mission['rcv_num'] == rcv_num
        
     
    
    

