DROP TABLE IF EXISTS classes;

CREATE TABLE classes
(
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    day TEXT NOT NULL,
    time TEXT NOT NULL,
    duration TEXT NOT NULL,
    trainer TEXT NOT NULL,
    description TEXT
);

INSERT INTO classes(name, day, time, duration, trainer, description)
VALUES
    ('Pilates', 'Monday', '07:00', '45 mins', 'Jason Quirke', 'A relaxing yet invigorating pilates class to start the week'),
    
    ('HIIT', 'Tuesday', '18:30', '30 mins', 'Sarah Connors', 'A high-intensity interval training class designed to burn calories fast.'),

    ('Yoga Flow', 'Wednesday', '08:00', '60 mins', 'Emma Lee', 'A dynamic yoga session to improve flexibility and mindfulness.'),

    ('Strength & Conditioning', 'Thursday', '17:45', '50 mins', 'Mark Reynolds', 'A strength-building class incorporating weights and bodyweight exercises.'),

    ('Spin Class', 'Friday', '06:30', '45 mins', 'Laura Kelly', 'An energetic indoor cycling session to boost endurance and cardio fitness.'),

    ('Zumba', 'Saturday', '10:00', '60 mins', 'Jessica Gomez', 'A fun dance-based workout to great music, perfect for all fitness levels.'),

    ('Boxing Fundamentals', 'Sunday', '15:00', '60 mins', 'Tommy Burke', 'Learn basic boxing techniques, footwork, and conditioning drills.'),

    ('Mobility & Stretch', 'Sunday', '17:30', '40 mins', 'Daniel Wong', 'A session focused on improving flexibility and preventing injuries.');

DROP TABLE IF EXISTS users;

CREATE TABLE users
(

    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL

);

DROP TABLE IF EXISTS admins;

CREATE TABLE admins
(

    admin_id TEXT PRIMARY KEY,
    password TEXT NOT NULL

);

DROP TABLE IF EXISTS free_trial_signups;

CREATE TABLE free_trial_signups 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    preferred_class TEXT NOT NULL
);