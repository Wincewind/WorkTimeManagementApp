DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS task_types CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name TEXT,
    permission_level INTEGER,
    work_cost_modifier INTEGER
);
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    role_id INTEGER REFERENCES roles(id)
);
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    manager_id INTEGER REFERENCES users(id),
    visible BOOLEAN DEFAULT TRUE
);
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    name TEXT,
    use_cost_limit BOOLEAN DEFAULT FALSE,
    use_hour_limit BOOleAN DEFAULT FALSE,
    cost_limit FLOAT,
    hour_limit INTEGER,
    visible BOOLEAN DEFAULT TRUE

);
CREATE TABLE task_types (
    id SERIAL PRIMARY KEY,
    description TEXT,
    hourly_cost FLOAT
);
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    duration_hours INTEGER,
    duration_minutes INTEGER,
    task_date TIMESTAMP,
    customer_id INTEGER REFERENCES customers(id),
    project_id INTEGER REFERENCES projects(id),
    task_type_id INTEGER REFERENCES task_types(id),
    invoiceable BOOLEAN,
    note TEXT
);
INSERT INTO roles (name, permission_level) 
VALUES  ('manager',1),
        ('developer',2);
INSERT INTO task_types (description, hourly_cost) 
VALUES  ('Development',100),
        ('Consulting', 80),
        ('Documentation', 80),
        ('Accounting', 50);
INSERT INTO customers (name) 
VALUES  ('Kiinteistöhuolto Oy'),
        ('Sanomalehti Oy'),
        ('Google');
INSERT INTO projects (name, customer_id, use_cost_limit, hour_limit) 
VALUES  ('New homepage development',2, TRUE, 0),
        ('VR Glasses prototype',3, FALSE, 10),
        ('AI Overlord',3, TRUE, 20),
        ('Cleaning floors', 1, FALSE, 100000);
