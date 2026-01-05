create database fittracker;
use fittracker;

create table users(
id int primary key auto_increment,
username varchar(50) not null,
email varchar(100) not null unique,
is_active boolean default true,
created_at datetime default current_timestamp
);

create table exercises(
id int primary key auto_increment,
name varchar(100) not null,
category enum('Strength', 'Cardio', 'Flexibility') not null,
description varchar(255)
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
