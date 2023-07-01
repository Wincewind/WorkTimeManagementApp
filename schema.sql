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
    invoiceable BOOLEAN DEFAULT FALSE,
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
        ('Google'),
        ('University of Helsinki');
INSERT INTO projects (name, customer_id, use_cost_limit, hour_limit) 
VALUES  ('New homepage development',2, TRUE, 0),
        ('VR Glasses prototype',3, FALSE, 10),
        ('AI Overlord',3, TRUE, 20),
        ('Cleaning floors', 1, FALSE, 100000),
        ('Tsoha project', 4, FALSE, 777);

INSERT INTO users (username, password, role_id) VALUES ('Wincewind', 'pbkdf2:sha256:600000$luKrGvnv26qd9mZp$623e47f6fc4124339ee630c15ed0af14b4daf9e51fde3025f2760c8a4bc515b7', 2);

INSERT INTO tasks (user_id, duration_hours, duration_minutes, task_date, customer_id, project_id, task_type_id, note) 
VALUES  (1, 2, 0, '20230519', 4, 5, 1, 'Started creating basic login functions and defining db tables'),
        (1, 3, 0, '20230520', 4, 5, 1, 'Continued working on login and signup functionality'),
        (1, 2, 0, '20230527', 4, 5, 1, 'Developed task creation functionality'),
        (1, 6, 0, '20230526', 4, 5, 1, 'Continued developing task creation functionality'),
        (1, 2, 0, '20230528', 4, 5, 1, 'Finished first version of task creation func'),
        (1, 3, 0, '20230529', 4, 5, 1, 'Started developing app visuals with bootstrap'),
        (1, 3, 0, '20230530', 4, 5, 1, 'Updating the visuals of home page'),
        (1, 4, 0, '20230531', 4, 5, 1, 'Continued updating the home page visuals and added some functionality to it'),
        (1, 3, 0, '20230602', 4, 5, 1, 'Started working on the customer services and management page'),
        (1, 4, 0, '20230603', 4, 5, 1, 'Completed customer management page and its functionality'),
        (1, 2, 0, '20230608', 4, 5, 1, 'Modified task cards to be clickable'),
        (1, 2, 0, '20230609', 4, 5, 1, 'Started implementing task selection and adding automatic filling of selected task details to its form'),
        (1, 5, 0, '20230611', 4, 5, 1, 'Finished implementing task editing, deletion and selection cancellation in the home page view'),
        (1, 2, 0, '20230615', 4, 5, 1, 'Started work on Projects page'),
        (1, 4, 0, '20230617', 4, 5, 1, 'Worked on Projects page, added creation and edit functions'),
        (1, 2, 0, '20230618', 4, 5, 1, 'Added delete function to projects'),
        (1, 1, 0, '20230627', 4, 5, 1, 'Refactoring code'),
        (1, 3, 0, '20230629', 4, 5, 3, 'Refactoring and adding docstrings to code'),
        (1, 4, 30, '20230701', 4, 5, 1, 'Added a query page to view tasks in table format which can be filtered'),
        (1, 2, 0, '20230701', 4, 5, 3, 'Updating documentation and adding mock data to application');
