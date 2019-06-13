-- 下面test1用户的密码是123456加密后的结果
INSERT INTO User (username, password, sid, email)
VALUES
  ('test1', 'pbkdf2:sha256:50000$26WYbCSt$9014a8d3969053fd0b55af5dea48e2b509d0e0586b6d30bae3dde9c8cd86df90', '16340001', '123@qq.com'),
  ('test10', 'pbkdf2:sha256:50000$26WYbCSt$9014a8d3969053fd0b55af5dea48e2b509d0e0586b6d30bae3dde9c8cd86df90', '16340010', '456@qq.com'),
  ('pj', 'pbkdf2:sha256:50000$26WYbCSt$9014a8d3969053fd0b55af5dea48e2b509d0e0586b6d30bae3dde9c8cd86df90','16340176','666@qq.com'),
  ('pj2', 'pbkdf2:sha256:50000$26WYbCSt$9014a8d3969053fd0b55af5dea48e2b509d0e0586b6d30bae3dde9c8cd86df90','16340171','666@qq.com');


INSERT INTO Verification (email, code)
VALUES 
  ('123@qq.com', '111111'),
  ('1234@qq.com', '123456');

INSERT INTO Verification (email, code, send_time)
VALUES 
  ('12345@qq.com', '123456', datetime('now','+1 hours'));

INSERT INTO MissionInfo (publisher_id, title, description, deadline,type,max_num,rcv_num,fin_num, state)
VALUES 
  (1, '问卷1', '未到最大数,开放', datetime('2029-06-08 11:20:12'),0,100,1,1,0),
  (1, '问卷2', '最大数-1, 开放', datetime('2029-06-08 11:20:12'),0,100,99,99,0),
  (1, '问卷3', '达最大数', datetime('2029-06-08 11:20:12'),0,100,100,100,1),
  (1, '问卷4', '未达最大,但已取消', datetime('2029-06-08 11:20:12'),0,100,50,50,1),
  (1, '问卷5', '未达最大，已过期', datetime('2019-06-08 11:20:12'), 0,100,50,0,0),
  (1, '快递6', '开放且尚未接的任务', datetime('2029-06-08 11:20:12'),1,1,0,0,0),
  (1, '快递7', '已经接了的任务', datetime('2029-06-08 11:20:12'),1,1,1,0,1),
  (1, '快递8', '已经取消了的任务', datetime('2029-06-08 11:20:12'),1,0,0,0,1),
  (1, '快递9', '已过期的任务', datetime('2019-06-08 11:20:12'),1,1,0,0,0);

INSERT INTO MissionInfo (publisher_id, phone, qq, wechat, other_way, type, create_time, deadline, title, description, bounty, max_num, rcv_num, fin_num, state)
VALUES
  (1, '1360', '14735', 'ousx', 'no', 0, datetime('2019-06-08 11:20:12'), datetime('2019-07-08 11:20:12'), 'test mission title', 'test mission description', 
    10, 10, 2, 1, 0),
  (2, '1360', '14735', 'ousx', 'no', 0, datetime('2019-06-08 11:20:12'), datetime('2019-07-08 11:20:12'), 'test mission title', 'test mission description', 
    20, 10, 2, 1, 0),
  (2, '1360', '14735', 'ousx', 'no', 0, datetime('2019-06-08 11:20:12'), datetime('2019-07-08 11:20:12'), 'test mission title', 'test mission description', 
    15, 10, 2, 1, 0),
  (1, '1360', '14735', 'ousx', 'no', 0, datetime('2019-06-06 11:20:12'), datetime('2019-07-08 11:20:12'), 'test mission title', 'test mission description', 
    5, 10, 2, 1, 0)
;

INSERT INTO MissionInfo (publisher_id, title, description, deadline,type,max_num,rcv_num,fin_num, state)
VALUES 
  (1, '问卷14', '问卷发布者取消任务', datetime('2029-06-08 11:20:12'),0,100,1,1,0),
  (1, '问卷15', '问卷填写者取消任务', datetime('2029-06-08 11:20:12'),0,100,50,49,0),
  (1, '问卷16', '问卷填写者取消任务,重新开放', datetime('2029-06-08 11:20:12'),0,100,100,99,1),
  (1, '快递17', '发布者取消未接任务', datetime('2029-06-08 11:20:12'),1,0,0,0,0),
  (1, '快递18', '发布者取消已接任务', datetime('2029-06-08 11:20:12'),1,1,1,0,1),
  (1, '快递19', '领取者放弃任务', datetime('2029-06-08 11:20:12'),1,1,1,0,1);

INSERT INTO MissionOrder (mission_id, receiver_id, publisher_confirm, receiver_confirm, receive_time, finish_time)
VALUES 
  (1, 3, 1, 1, datetime('2019-06-08 12:12:12'), datetime('2019-06-08 12:12:12')),
  (2, 3, 1, 1, datetime('2019-06-08 12:12:12'), Null)
;

INSERT INTO MissionOrder (mission_id, receiver_id, publisher_confirm, receiver_confirm, order_state, receive_time, finish_time)
VALUES 
  (11, 3, 1, 1, 1, datetime('2019-06-08 12:12:12'), datetime('2019-06-08 12:12:12')),
  (11, 3, 1, 1, 0, datetime('2019-06-08 12:12:12'), datetime('2019-06-08 12:12:12')),
  (11, 1, 0, 0, 0, datetime('2019-06-08 12:12:12'), datetime('2019-06-08 12:12:12')),
  (11, 1, 0, 0, 0, datetime('2019-06-08 12:12:12'), datetime('2019-06-08 12:12:12')),
  (6, 2, 0, 0, 0, datetime('2019-06-08 12:12:12'), datetime('2019-06-08 12:12:12')),
  (15, 3, 0, 0, 0, datetime('2019-06-08 12:12:12'), datetime('2019-06-08 12:12:12')),
  (16, 3, 0, 0, 0, datetime('2019-06-08 12:12:12'), datetime('2019-06-08 12:12:12')),
  (16, 3, 0, 0, 0, datetime('2019-06-08 12:12:12'), datetime('2019-06-08 12:12:12')),
  (18, 3, 0, 0, 0, datetime('2019-06-08 12:12:12'), datetime('2019-06-08 12:12:12')),
  (19, 3, 0, 0, 0, datetime('2019-06-08 12:12:12'), datetime('2019-06-08 12:12:12')),
  -- ousx新添加
  (7, 3, 0, 0, 0, datetime('2019-06-08 12:12:12'), datetime('2019-06-08 12:12:12'))
;

INSERT INTO Problem (mission_id, type, problem_stem, problem_detail)
VALUES 
  (11, 0, 'are you pj', '["yes", "no", "pardon"]'),
  (11, 1, 'what do you like', '["apple", "banana", "watermelon"]'),
  (11, 2, 'what is your name', '""')
;

INSERT INTO Answer (order_id, problem_id, result)
VALUES 
  (3, 1, '0'),
  (3, 2, '[1,2]'),
  (3, 3, '"ousuixin"'),
  (4, 1, '1'),
  (4, 2, '[0,2]'),
  (4, 3, '"pj"'),
  (5, 1, '2'),
  (5, 2, '[0,2]'),
  (5, 3, '"pjh"')
;