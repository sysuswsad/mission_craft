DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS mission;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    nickname TEXT NOT NULL,
    realname TEXT NOT NULL,
    IDcard_number INTEGER NOT NULL,
    usertype TEXT NOT NULL,
    university TEXT NOT NULL,
    school TEXT NOT NULL,
    major TEXT NOT NULL,
    grade TEXT NOT NULL,
    email TEXT NOT NULL,
    tel INTEGER NOT NULL,
    qq INTEGER,
    wechat TEXT,
    sex TEXT NOT NULL,
    tags TEXT,
    icon BLOB,
    balance INTEGER NOT NULL DEFAULT 0,
    number_of_missions_give INTEGER NOT NULL DEFAULT 0,
    number_of_missions_get INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE mission (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    consigner_id INTEGER NOT NULL,
    consignee_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (consigner_id) REFERENCES user (id),
    FOREIGN KEY (consignee_id) REFERENCES user (id)
);