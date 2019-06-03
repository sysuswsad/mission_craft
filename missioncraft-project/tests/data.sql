-- 下面test1用户的密码是123456加密后的结果
INSERT INTO User (username, password, sid, email)
VALUES
  ('test1', 'pbkdf2:sha256:50000$26WYbCSt$9014a8d3969053fd0b55af5dea48e2b509d0e0586b6d30bae3dde9c8cd86df90', '16340001', '123@qq.com'),
  ('test10', 'pbkdf2:sha256:50000$26WYbCSt$9014a8d3969053fd0b55af5dea48e2b509d0e0586b6d30bae3dde9c8cd86df90', '16340010', '456@qq.com');

INSERT INTO Verification (email, code)
VALUES 
  ('123@qq.com', '111111'),
  ('1234@qq.com', '123456')