sudo service mysql stop
./cloud_sql_proxy -instances="nytrack-express:us-central1:polls"=tcp:3306
