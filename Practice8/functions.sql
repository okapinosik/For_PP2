CREATE OR REPLACE FUNCTION search_phonebook(p_pattern TEXT)
RETURNS TABLE (
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone_number VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        pb.id,
        pb.first_name,
        pb.last_name,
        pb.phone_number
    FROM phonebook pb
    WHERE pb.first_name ILIKE '%' || p_pattern || '%'
       OR pb.last_name ILIKE '%' || p_pattern || '%'
       OR pb.phone_number ILIKE '%' || p_pattern || '%'
    ORDER BY pb.id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_phonebook_page(p_limit INT, p_offset INT)
RETURNS TABLE (
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone_number VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        pb.id,
        pb.first_name,
        pb.last_name,
        pb.phone_number
    FROM phonebook pb
    ORDER BY pb.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;