CREATE USER admin WITH PASSWORD 'password';
CREATE DATABASE postgres_db OWNER admin;
GRANT ALL PRIVILEGES ON DATABASE postgres_db TO admin;
