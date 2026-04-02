
CREATE OR REPLACE PROCEDURE insert_or_update_user(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR
)
AS $$
BEGIN
    INSERT INTO phonebook(first_name, last_name, phone_number)
    VALUES (p_first_name, p_last_name, p_phone)
    ON CONFLICT (first_name, last_name)
    DO UPDATE SET phone_number = EXCLUDED.phone_number;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE insert_many_users(
    p_first_names TEXT[],
    p_last_names TEXT[],
    p_phones TEXT[],
    INOUT p_invalid_data TEXT[] DEFAULT ARRAY[]::TEXT[]
)
AS $$
DECLARE
    i INT;
BEGIN
    IF array_length(p_first_names, 1) IS DISTINCT FROM array_length(p_last_names, 1)
       OR array_length(p_first_names, 1) IS DISTINCT FROM array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Arrays must have the same length';
    END IF;

    FOR i IN 1..COALESCE(array_length(p_first_names, 1), 0)
    LOOP
        IF p_phones[i] ~ '^\+?[0-9]{10,15}$' THEN
            INSERT INTO phonebook(first_name, last_name, phone_number)
            VALUES (p_first_names[i], p_last_names[i], p_phones[i])
            ON CONFLICT (first_name, last_name)
            DO UPDATE SET phone_number = EXCLUDED.phone_number;
        ELSE
            p_invalid_data := array_append(
                p_invalid_data,
                p_first_names[i] || ' ' || p_last_names[i] || ' -> ' || p_phones[i]
            );
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE delete_user_by_name_or_phone(
    p_value TEXT
)
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = p_value
       OR last_name = p_value
       OR (first_name || ' ' || last_name) = p_value
       OR phone_number = p_value;
END;
$$ LANGUAGE plpgsql;