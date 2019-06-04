DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS MissionInfo;

CREATE TABLE User (
  idUser INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(45) UNIQUE NOT NULL,
  password VARCHAR(45) NOT NULL,
  sid VARCHAR(45) UNIQUE NOT NULL,
  realname VARCHAR(45) DEFAULT '',
  id_card_num VARCHAR(45) DEFAULT '',
  type INT DEFAULT 0,
  -- 注意一下sql里面id都是从1开始，所以下面这个id=0是无意义的，不能用，需要赋值后使用
  -- 并且记得添加管理员表之后，需要为下面的属性标注外键
  check_man_id INT DEFAULT 0,
  university VARCHAR(45) DEFAULT '',
  school VARCHAR(45) DEFAULT '',
  grade VARCHAR(45) DEFAULT '',
  gender INT DEFAULT 0,
  email VARCHAR(45) NOT NULL,
  phone VARCHAR(45) DEFAULT '',
  qq VARCHAR(45) DEFAULT '',
  wechat VARCHAR(45) DEFAULT '',
  avatar BLOB NULL,
  tag VARCHAR(45) DEFAULT '',
  mission_pub_num INT DEFAULT 0,
  mission_todo_num INT DEFAULT 0,
  mission_fin_num INT DEFAULT 0,
  balance DOUBLE DEFAULT 0.0
);

CREATE TABLE MissionInfo (
  idMissionInfo INTEGER PRIMARY KEY AUTOINCREMENT,
  publisher_id INTEGER NOT NULL,
  type INT DEFAULT 0,
  tag VARCHAR(45) NULL,
  create_time TIMESTAMP NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP,'localtime')),
  deadline TIMESTAMP NOT NULL,
  title VARCHAR(45) NOT NULL,
  description VARCHAR(45) NOT NULL,
  detail VARCHAR(45) DEFAULT '',
  Bounty DOUBLE DEFAULT 1,
  max_num INT DEFAULT 1,
  rcv_num INT DEFAULT 0,
  fin_num INT DEFAULT 0,
  state DOUBLE DEFAULT 0,
  FOREIGN KEY (publisher_id) REFERENCES User (id)
);

-- 如果不使用redis数据库，就需要将验证码存到邮箱的这个表
CREATE TABLE Verification (
  email VARCHAR(45) PRIMARY KEY,
  code VARCHAR(10) NOT NULL,
  send_time TIMESTAMP NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP,'localtime'))
)

-- 下面这些是整个sql数据库创建，mydb指的是数据库名字，这里我们可以去掉，因为数据库名字叫mission_craft

-- -----------------------------------------------------
-- Table mydb.Manager
-- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS mydb.Manager (
--   idManager INT NOT NULL,
--   managername VARCHAR(45) NOT NULL,
--   password VARCHAR(45) NOT NULL,
--   info VARCHAR(45) NULL,
--   PRIMARY KEY (idManager),
--   UNIQUE INDEX managername_UNIQUE (managername ASC) VISIBLE)
-- ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.User
-- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS mydb.User (
  -- idUser INT NOT NULL AUTO_INCREMENT,
  -- username VARCHAR(45) NOT NULL,
  -- password VARCHAR(45) NOT NULL,
  -- realname VARCHAR(45) NOT NULL,
  -- id_card_num VARCHAR(45) NOT NULL,
  -- type INT ZEROFILL NULL,
  -- check_man_id INT NOT NULL,
  -- school VARCHAR(45) NOT NULL,
  -- subject VARCHAR(45) NULL,
  -- grade VARCHAR(45) NULL,
  -- sex INT NULL,
  -- email VARCHAR(45) NOT NULL,
  -- phone VARCHAR(45) NOT NULL,
  -- qq VARCHAR(45) NULL,
  -- wechat VARCHAR(45) NULL,
  -- avatar BLOB NULL,
  -- tag VARCHAR(45) NULL,
  -- mission_pub_num INT ZEROFILL NULL,
  -- mission_fin_num INT ZEROFILL NULL,
  -- balance DOUBLE ZEROFILL NULL,
--   PRIMARY KEY (idUser),
--   UNIQUE INDEX username_UNIQUE (username ASC) VISIBLE,
--   UNIQUE INDEX id_card_num_UNIQUE (id_card_num ASC) VISIBLE,
--   INDEX fk_User_Manager1_idx (check_man_id ASC) VISIBLE,
--   CONSTRAINT fk_User_Manager1
--     FOREIGN KEY (check_man_id)
--     REFERENCES mydb.Manager (idManager)
--     ON DELETE NO ACTION
--     ON UPDATE NO ACTION)
-- ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.MissionInfo
-- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS mydb.MissionInfo (
--   idMissionInfo INT NOT NULL,
--   publisher_id INT NOT NULL,
--   tag VARCHAR(45) NULL,
--   create_time TIMESTAMP NOT NULL,
--   deadline TIMESTAMP NOT NULL,
--   title VARCHAR(45) NOT NULL,
--   description VARCHAR(45) NOT NULL,
--   detail VARCHAR(45) NULL,
--   Bounty VARCHAR(45) NOT NULL,
--   max_num INT NOT NULL,
--   state INT NOT NULL,
--   PRIMARY KEY (idMissionInfo),
--   INDEX fk_MissionInfo_User_idx (publisher_id ASC) VISIBLE,
--   CONSTRAINT fk_MissionInfo_User
--     FOREIGN KEY (publisher_id)
--     REFERENCES mydb.User (idUser)
--     ON DELETE NO ACTION
--     ON UPDATE NO ACTION)
-- ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.MissionOrder
-- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS mydb.MissionOrder (
--   idMissionOrder INT NOT NULL,
--   mission_id INT NOT NULL,
--   receiver_id INT NOT NULL,
--   publisher_confirm INT ZEROFILL NULL,
--   receiver_confirm INT ZEROFILL NULL,
--   order_state INT ZEROFILL NULL,
--   receive_time TIMESTAMP NOT NULL,
--   finish_time TIMESTAMP NULL,
--   PRIMARY KEY (idMissionOrder),
--   INDEX fk_MissionOrder_User1_idx (receiver_id ASC) VISIBLE,
--   INDEX fk_MissionOrder_MissionInfo1_idx (mission_id ASC) VISIBLE,
--   CONSTRAINT fk_MissionOrder_User1
--     FOREIGN KEY (receiver_id)
--     REFERENCES mydb.User (idUser)
--     ON DELETE NO ACTION
--     ON UPDATE NO ACTION,
--   CONSTRAINT fk_MissionOrder_MissionInfo1
--     FOREIGN KEY (mission_id)
--     REFERENCES mydb.MissionInfo (idMissionInfo)
--     ON DELETE NO ACTION
--     ON UPDATE NO ACTION)
-- ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.Appeal
-- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS mydb.Appeal (
--   idAppeal INT NOT NULL,
--   order_id INT NOT NULL,
--   process_man_id INT NOT NULL,
--   create_time TIMESTAMP NOT NULL,
--   description VARCHAR(45) NOT NULL,
--   PRIMARY KEY (idAppeal),
--   INDEX fk_Appeal_MissionOrder1_idx (order_id ASC) VISIBLE,
--   INDEX fk_Appeal_Manager1_idx (process_man_id ASC) VISIBLE,
--   CONSTRAINT fk_Appeal_MissionOrder1
--     FOREIGN KEY (order_id)
--     REFERENCES mydb.MissionOrder (idMissionOrder)
--     ON DELETE NO ACTION
--     ON UPDATE NO ACTION,
--   CONSTRAINT fk_Appeal_Manager1
--     FOREIGN KEY (process_man_id)
--     REFERENCES mydb.Manager (idManager)
--     ON DELETE NO ACTION
--     ON UPDATE NO ACTION)
-- ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.Problem
-- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS mydb.Problem (
--   idProblem INT NOT NULL,
--   mission_id INT NOT NULL,
--   type INT NOT NULL,
--   problem_stem VARCHAR(45) NOT NULL,
--   problem_detail VARCHAR(45) NULL,
--   must_be_answer INT NOT NULL,
--   jump_logic INT NULL,
--   statistics_info VARCHAR(45) NULL,
--   PRIMARY KEY (idProblem),
--   INDEX fk_Problem_MissionInfo1_idx (mission_id ASC) VISIBLE,
--   CONSTRAINT fk_Problem_MissionInfo1
--     FOREIGN KEY (mission_id)
--     REFERENCES mydb.MissionInfo (idMissionInfo)
--     ON DELETE NO ACTION
--     ON UPDATE NO ACTION)
-- ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.AnswerStatistics
-- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS mydb.AnswerStatistics (
--   idAnswerStatistics INT NOT NULL,
--   problem_id INT NOT NULL,
--   statistics_info VARCHAR(45) NULL,
--   supplement_info VARCHAR(45) NULL,
--   PRIMARY KEY (idAnswerStatistics),
--   INDEX fk_AnswerStatistics_Problem1_idx (problem_id ASC) VISIBLE,
--   CONSTRAINT fk_AnswerStatistics_Problem1
--     FOREIGN KEY (problem_id)
--     REFERENCES mydb.Problem (idProblem)
--     ON DELETE NO ACTION
--     ON UPDATE NO ACTION)
-- ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table mydb.Answer
-- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS mydb.Answer (
--   idAnswer INT NOT NULL,
--   order_id INT NOT NULL,
--   problem_id INT NOT NULL,
--   result VARCHAR(45) NOT NULL,
--   answer_time VARCHAR(45) NOT NULL,
--   feedback VARCHAR(45) NULL,
--   supplement_info VARCHAR(45) NULL,
--   PRIMARY KEY (idAnswer),
--   INDEX fk_Answer_MissionOrder1_idx (order_id ASC) VISIBLE,
--   INDEX fk_Answer_Problem1_idx (problem_id ASC) VISIBLE,
--   CONSTRAINT fk_Answer_MissionOrder1
--     FOREIGN KEY (order_id)
--     REFERENCES mydb.MissionOrder (idMissionOrder)
--     ON DELETE NO ACTION
--     ON UPDATE NO ACTION,
--   CONSTRAINT fk_Answer_Problem1
--     FOREIGN KEY (problem_id)
--     REFERENCES mydb.Problem (idProblem)
--     ON DELETE NO ACTION
--     ON UPDATE NO ACTION)
-- ENGINE = InnoDB;
