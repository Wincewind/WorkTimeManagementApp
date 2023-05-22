DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

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
    role_id INTEGER REFERENCES roles
);
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    visible BOOLEAN
);
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers,
    name TEXT,
    cost_limit FLOAT,
    hour_limit INTEGER,
    visible BOOLEAN

);
CREATE TABLE task_types (
    id SERIAL PRIMARY KEY,
    description TEXT,
    hourly_cost FLOAT
);
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    duration_hours INTEGER,
    duration_minutes INTEGER,
    task_date TIMESTAMP,
    customer_id INTEGER REFERENCES customers,
    project_id INTEGER REFERENCES projects,
    task_type_id INTEGER REFERENCES task_types,
    invoiceable BOOLEAN,
    note TEXT
);
INSERT INTO roles (name, permission_level) VALUES ('manager',1);
INSERT INTO roles (name, permission_level) VALUES ('developer',2);