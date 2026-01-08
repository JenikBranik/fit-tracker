create database fittracker;
use fittracker;

SET autocommit = 0;
START TRANSACTION;

create table users(
id int primary key auto_increment,
username varchar(50) not null,
email varchar(100) not null unique,
created_at datetime default current_timestamp
);

create table exercises(
id int primary key auto_increment,
name varchar(100) not null,
category enum('Strength', 'Cardio', 'Flexibility') not null
);

create table workouts(
id int primary key auto_increment,
user_id int not null,
start_time datetime not null,
note varchar(255),
foreign key(user_id) references users(id)
);

create table workout_items(
id int primary key auto_increment,
workout_id int not null,
exercise_id int not null,
sets int not null,
reps int not null,
weight_kg float not null,
is_warmup boolean,
foreign key(workout_id) references workouts(id),
foreign key(exercise_id) references exercises(id)
);

create table body_measurements(
id int primary key auto_increment,
user_id int not null,
log_date date not null,
weight_kg float not null,
foreign key(user_id) references users(id)
);

CREATE VIEW user_summary AS
SELECT u.id AS user_id, u.username,COUNT(DISTINCT w.id) AS total_workouts,(
SELECT weight_kg FROM body_measurements bm 
WHERE bm.user_id = u.id 
ORDER BY log_date DESC
LIMIT 1
) AS current_weight_kg
FROM users u
LEFT JOIN workouts w ON u.id = w.user_id
GROUP BY u.id, u.username;

CREATE VIEW workout_details AS
SELECT 
    wi.workout_id,
    e.name AS exercise_name,
    wi.sets,
    wi.reps,
    wi.weight_kg,
    wi.is_warmup
FROM workout_items wi
JOIN exercises e ON wi.exercise_id = e.id;

COMMIT;