#!/bin/bash
# For Production server we're going to run daily backups
# with this script with a cronjob
cd backups
echo 'Backup up the wordpress database'
docker exec -t wordpress_db mysqldump -u ${WORDPRESS_DB_USER} -p${WORDPRESS_DB_PASSWORD} ${WORDPRESS_DB_NAME} > latest_mysql_dump.sql
gzip latest_mysql_dump.sql

mv latest_mysql_dump.sql.gz wordpress_db_dump_$(date +%s).sql.gz