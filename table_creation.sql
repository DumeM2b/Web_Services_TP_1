CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    age INT,
    email VARCHAR(100),
    job VARCHAR(100)
);

CREATE TABLE public.applications (
    id SERIAL PRIMARY KEY,
    appname VARCHAR(100) NOT NULL,
    username VARCHAR(100),
    lastconnection DATE,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
