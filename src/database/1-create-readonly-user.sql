-- Create the read-only user and grant permissions

-- [WARNING!]
-- Make sure to update the password before running the SQL database setup with the password mentioned in the wiki.
-- Otherwise the server setup is highly insecure and susceptible to attacks potentially resulting in unavailability and dataloss!
CREATE USER 'aris-read-only-user'@'%' IDENTIFIED BY 'Replace_me_wh3n_deploying_on_public_server';
GRANT SELECT ON aris.* TO 'aris-read-only-user'@'%';
FLUSH PRIVILEGES;
