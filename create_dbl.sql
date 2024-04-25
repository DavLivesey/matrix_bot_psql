create table workers
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(255) NOT NULL,
    APTEKA VARCHAR DEFAULT 'Нет',
    ZKGU VARCHAR DEFAULT 'Нет',
    BGU_1 VARCHAR DEFAULT 'Нет',
    BGU_2 VARCHAR DEFAULT 'Нет',
    DIETA VARCHAR DEFAULT 'Нет',
    MIS VARCHAR DEFAULT 'Нет',
    TIS VARCHAR DEFAULT 'Нет',
    SED VARCHAR DEFAULT 'Нет',
    EMAIL VARCHAR DEFAULT 'Нет'
);

create table sertificates
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    worker_id INTEGER,
    center_name VARCHAR,
    serial_number INTEGER,
    DATE_START DATE,
    DATE_FINISH DATE,
    FOREIGN KEY(worker_id) REFERENCES workers(id)
);
