SELECT id, name, path, description, created_at
FROM metasystem_modules
WHERE name = :name;