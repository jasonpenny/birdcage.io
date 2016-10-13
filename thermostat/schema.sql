DROP TABLE IF EXISTS info;
CREATE TABLE info(
    unique_id text,
    nickname text
);

DROP TABLE IF EXISTS target_temperatures;
CREATE TABLE target_temperatures (
    id integer PRIMARY KEY AUTOINCREMENT,
    temperature integer
);
