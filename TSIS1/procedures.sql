CREATE OR REPLACE PROCEDURE insert_or_update_contact(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_email VARCHAR,
    p_birthday DATE,
    p_group_name VARCHAR,
    p_phone VARCHAR,
    p_phone_type VARCHAR
)
AS $$
DECLARE
    v_group_id INT;
    v_contact_id INT;
BEGIN
    INSERT INTO groups(name)
    VALUES (COALESCE(p_group_name, 'Other'))
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id
    FROM groups
    WHERE name = COALESCE(p_group_name, 'Other');

    INSERT INTO contacts(first_name, last_name, email, birthday, group_id)
    VALUES (p_first_name, p_last_name, p_email, p_birthday, v_group_id)
    ON CONFLICT (first_name, last_name)
    DO UPDATE SET
        email = EXCLUDED.email,
        birthday = EXCLUDED.birthday,
        group_id = EXCLUDED.group_id
    RETURNING id INTO v_contact_id;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_phone_type)
    ON CONFLICT (phone)
    DO UPDATE SET
        contact_id = EXCLUDED.contact_id,
        type = EXCLUDED.type;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
AS $$
DECLARE
    v_contact_id INT;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE first_name = p_contact_name
       OR TRIM(first_name || ' ' || COALESCE(last_name, '')) = p_contact_name
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found: %', p_contact_name;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type)
    ON CONFLICT (phone)
    DO UPDATE SET
        contact_id = EXCLUDED.contact_id,
        type = EXCLUDED.type;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
AS $$
DECLARE
    v_group_id INT;
BEGIN
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE first_name = p_contact_name
       OR TRIM(first_name || ' ' || COALESCE(last_name, '')) = p_contact_name;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact not found: %', p_contact_name;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE delete_contact_by_name_or_phone(
    p_value TEXT
)
AS $$
BEGIN
    DELETE FROM contacts
    WHERE id IN (
        SELECT c.id
        FROM contacts c
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE c.first_name = p_value
           OR c.last_name = p_value
           OR TRIM(c.first_name || ' ' || COALESCE(c.last_name, '')) = p_value
           OR p.phone = p_value
    );
END;
$$ LANGUAGE plpgsql;