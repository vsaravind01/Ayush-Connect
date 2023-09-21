# create user ayush_admin_client
sudo psql -U postgres -c "CREATE USER ayush_admin_client WITH PASSWORD 'ayush_admin_client_secret';"
# create database ayush_connect with owner ayush_admin_client and encoding UTF8
sudo psql -U postgres -c "CREATE DATABASE ayush_connect WITH OWNER ayush_admin_client ENCODING 'UTF8';"