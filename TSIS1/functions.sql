CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name AS group_name,
        STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.last_name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
    ORDER BY c.id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit INT,
    p_offset INT,
    p_sort_by TEXT DEFAULT 'id',
    p_group_name TEXT DEFAULT NULL
)
RETURNS TABLE (
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name AS group_name,
        STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE p_group_name IS NULL OR g.name = p_group_name
    GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
    ORDER BY
        CASE WHEN p_sort_by = 'name' THEN c.first_name END ASC,
        CASE WHEN p_sort_by = 'birthday' THEN c.birthday END ASC,
        CASE WHEN p_sort_by = 'date_added' THEN c.created_at END ASC,
        c.id ASC
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;