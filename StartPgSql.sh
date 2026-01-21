sudo apt-get install build-essential
sudo apt install ninja-build
sudo apt-get update && sudo apt-get install -y postgresql postgresql-contrib
sudo pg_ctlcluster 16 main start
sudo pg_ctlcluster 16 main status
sudo setpriv --reuid=postgres --regid=postgres --init-groups psql

# Adding Drogon Ctl into path
echo 'export PATH="/workspaces/Swagger-Dragon-CPP/build/default/vcpkg_installed/x64-linux/tools/drogon/:$PATH"' >> ~/.bashrc
