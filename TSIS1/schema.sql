CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups(name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_contact_name UNIQUE (first_name, last_name)
);

CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile')),
    CONSTRAINT uq_phones_phone UNIQUE (phone)
);