
use timetable;

CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(50) UNIQUE
);


CREATE TABLE teachers (
    teacher_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);


CREATE TABLE subjects (
    Subcode VARCHAR(10) PRIMARY KEY,
    Subname VARCHAR(100)
);


CREATE TABLE timeslots (
    slot_id SERIAL PRIMARY KEY,
    day VARCHAR(10),
    start_time TIME,
    end_time TIME  
);

INSERT INTO teachers (name) VALUES
('MR. ASHISH GARG'),
('MR. RAHUL CHAUHAN'),
('DR. MAHESH MANCHANDA'),
('MR. AKSHAY RAJPUT'),
('DR. SEEMA GULATI'),
('DR. PRAKASH'),
('MS. SHRADDHA'),
('MR. GAURAV'),
('MS. AANCHAL'),
('MS. SWATI JOSHI'),
('MS. NUPUR DUBEY'),
('DR. DEVESH TIWARI'),
('DR. PRATEEK SRIVASTAVA'),
('MR. PURUSHOTTAM DAS'),
('MR. ANSHUMAN SHARMA'),
('DR. ANUPAM SINGH');

INSERT INTO rooms (room_name) VALUES
('LAB 9'), ('MICRO LAB 2'), ('TCL 1'), ('MICRO LAB 1'), ('LAB 3'),
('LT 201'), ('NEW AUDI'), ('CR 204'), ('LT 202'), ('UBUNTU LAB 1'),
('VENUE 1'),('LT-301'),('CR-201'),('CR-202'),('TCL-4'),('CR-204'),('LAB-1'),('UBUNTU LAB 2'),('LT-202');
INSERT INTO subjects (Subcode, Subname) VALUES
('TCS 402', 'FINITE AUTOMATA & FORMAL LANGUAGES'),
('TCS 403', 'MICROPROCESSOR'),
('TCS 408', 'JAVA PROGRAMMING LANGUAGE'),
('TCS 409', 'DESIGN & ANALYSIS OF ALGORITHMS'),
('TCS 421', 'FUNDAMENTALS OF STATISTICS AND AI'),
('TCS 451', 'VIRTUALIZATION & CLOUD COMPUTING'),
('TCS 495', 'FOUNDATION OF CYBER SECURITY'),
('XCS 401', 'CAREER SKILLS'),
('PCS 403', 'MICROPROCESSOR LAB'),
('PCS 408', 'JAVA LAB'),
('PCS 409', 'DAA LAB'),
('PESE 400', 'PRACTICAL FOR EMPLOYABILITY SKILLS ENHANCEMENT');

INSERT INTO timeslots (day, start_time, end_time) VALUES
('MON', STR_TO_DATE('08:00 AM', '%h:%i %p'), STR_TO_DATE('08:55 AM', '%h:%i %p')),
('MON', STR_TO_DATE('08:55 AM', '%h:%i %p'), STR_TO_DATE('09:50 AM', '%h:%i %p')),
('MON', STR_TO_DATE('10:10 AM', '%h:%i %p'), STR_TO_DATE('11:05 AM', '%h:%i %p')),
('MON', STR_TO_DATE('12:00 PM', '%h:%i %p'), STR_TO_DATE('12:55 PM', '%h:%i %p')),
('MON', STR_TO_DATE('12:55 PM', '%h:%i %p'), STR_TO_DATE('01:50 PM', '%h:%i %p')),
('MON', STR_TO_DATE('02:10 PM', '%h:%i %p'), STR_TO_DATE('03:05 PM', '%h:%i %p')),
('MON', STR_TO_DATE('04:00 PM', '%h:%i %p'), STR_TO_DATE('04:55 PM', '%h:%i %p')),
('MON', STR_TO_DATE('04:55 PM', '%h:%i %p'), STR_TO_DATE('05:50 PM', '%h:%i %p')),

('TUE', STR_TO_DATE('08:00 AM', '%h:%i %p'), STR_TO_DATE('08:55 AM', '%h:%i %p')),
('TUE', STR_TO_DATE('08:55 AM', '%h:%i %p'), STR_TO_DATE('09:50 AM', '%h:%i %p')),
('TUE', STR_TO_DATE('10:10 AM', '%h:%i %p'), STR_TO_DATE('11:05 AM', '%h:%i %p')),
('TUE', STR_TO_DATE('12:00 PM', '%h:%i %p'), STR_TO_DATE('12:55 PM', '%h:%i %p')),
('TUE', STR_TO_DATE('12:55 PM', '%h:%i %p'), STR_TO_DATE('01:50 PM', '%h:%i %p')),
('TUE', STR_TO_DATE('02:10 PM', '%h:%i %p'), STR_TO_DATE('03:05 PM', '%h:%i %p')),
('TUE', STR_TO_DATE('04:00 PM', '%h:%i %p'), STR_TO_DATE('04:55 PM', '%h:%i %p')),
('TUE', STR_TO_DATE('04:55 PM', '%h:%i %p'), STR_TO_DATE('05:50 PM', '%h:%i %p')),

('WED', STR_TO_DATE('08:00 AM', '%h:%i %p'), STR_TO_DATE('08:55 AM', '%h:%i %p')),
('WED', STR_TO_DATE('08:55 AM', '%h:%i %p'), STR_TO_DATE('09:50 AM', '%h:%i %p')),
('WED', STR_TO_DATE('10:10 AM', '%h:%i %p'), STR_TO_DATE('11:05 AM', '%h:%i %p')),
('WED', STR_TO_DATE('12:00 PM', '%h:%i %p'), STR_TO_DATE('12:55 PM', '%h:%i %p')),
('WED', STR_TO_DATE('12:55 PM', '%h:%i %p'), STR_TO_DATE('01:50 PM', '%h:%i %p')),
('WED', STR_TO_DATE('02:10 PM', '%h:%i %p'), STR_TO_DATE('03:05 PM', '%h:%i %p')),
('WED', STR_TO_DATE('04:00 PM', '%h:%i %p'), STR_TO_DATE('04:55 PM', '%h:%i %p')),
('WED', STR_TO_DATE('04:55 PM', '%h:%i %p'), STR_TO_DATE('05:50 PM', '%h:%i %p')),

('THU', STR_TO_DATE('08:00 AM', '%h:%i %p'), STR_TO_DATE('08:55 AM', '%h:%i %p')),
('THU', STR_TO_DATE('08:55 AM', '%h:%i %p'), STR_TO_DATE('09:50 AM', '%h:%i %p')),
('THU', STR_TO_DATE('10:10 AM', '%h:%i %p'), STR_TO_DATE('11:05 AM', '%h:%i %p')),
('THU', STR_TO_DATE('12:00 PM', '%h:%i %p'), STR_TO_DATE('12:55 PM', '%h:%i %p')),
('THU', STR_TO_DATE('12:55 PM', '%h:%i %p'), STR_TO_DATE('01:50 PM', '%h:%i %p')),
('THU', STR_TO_DATE('02:10 PM', '%h:%i %p'), STR_TO_DATE('03:05 PM', '%h:%i %p')),
('THU', STR_TO_DATE('04:00 PM', '%h:%i %p'), STR_TO_DATE('04:55 PM', '%h:%i %p')),
('THU', STR_TO_DATE('04:55 PM', '%h:%i %p'), STR_TO_DATE('05:50 PM', '%h:%i %p')),

('FRI', STR_TO_DATE('08:00 AM', '%h:%i %p'), STR_TO_DATE('08:55 AM', '%h:%i %p')),
('FRI', STR_TO_DATE('08:55 AM', '%h:%i %p'), STR_TO_DATE('09:50 AM', '%h:%i %p')),
('FRI', STR_TO_DATE('10:10 AM', '%h:%i %p'), STR_TO_DATE('11:05 AM', '%h:%i %p')),
('FRI', STR_TO_DATE('12:00 PM', '%h:%i %p'), STR_TO_DATE('12:55 PM', '%h:%i %p')),
('FRI', STR_TO_DATE('12:55 PM', '%h:%i %p'), STR_TO_DATE('01:50 PM', '%h:%i %p')),
('FRI', STR_TO_DATE('02:10 PM', '%h:%i %p'), STR_TO_DATE('03:05 PM', '%h:%i %p')),
('FRI', STR_TO_DATE('04:00 PM', '%h:%i %p'), STR_TO_DATE('04:55 PM', '%h:%i %p')),
('FRI', STR_TO_DATE('04:55 PM', '%h:%i %p'), STR_TO_DATE('05:50 PM', '%h:%i %p')),
('SAT', STR_TO_DATE('08:00 AM', '%h:%i %p'), STR_TO_DATE('08:55 AM', '%h:%i %p')),
('SAT', STR_TO_DATE('08:55 AM', '%h:%i %p'), STR_TO_DATE('09:50 AM', '%h:%i %p')),
('SAT', STR_TO_DATE('10:10 AM', '%h:%i %p'), STR_TO_DATE('11:05 AM', '%h:%i %p')),
('SAT', STR_TO_DATE('12:00 PM', '%h:%i %p'), STR_TO_DATE('12:55 PM', '%h:%i %p')),
('SAT', STR_TO_DATE('12:55 PM', '%h:%i %p'), STR_TO_DATE('01:50 PM', '%h:%i %p')),
('SAT', STR_TO_DATE('02:10 PM', '%h:%i %p'), STR_TO_DATE('03:05 PM', '%h:%i %p')),
('SAT', STR_TO_DATE('04:00 PM', '%h:%i %p'), STR_TO_DATE('04:55 PM', '%h:%i %p')),
('SAT', STR_TO_DATE('04:55 PM', '%h:%i %p'), STR_TO_DATE('05:50 PM', '%h:%i %p'));
SHOW tables;
select *from teachers;
select *from subjects ;
select *from rooms;
select *from timeslots;
 