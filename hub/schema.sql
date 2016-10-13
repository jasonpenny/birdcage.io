DROP TABLE IF EXISTS thermostats;
CREATE TABLE thermostats (
    id text primary key,
    ip_address text NOT NULL,
    port integer NOT NULL,
    online boolean NOT NULL
);
