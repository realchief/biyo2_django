#!/bin/sh
# Run:
# sh fix_collations.sh <schema_name> <user> <host> [password]

# alter table <some_table> convert to character set utf8 collate utf8_unicode_ci;

SCHEMA=$1
DBUSER=$2
DBHOST=$3
DBPASS=$4

[ -z $DBPASS ] && echo -n "Enter password: " && stty -echo && read DBPASS && stty echo && echo

QUERY="SELECT CONCAT(\"ALTER TABLE $SCHEMA.\", TABLE_NAME, \" convert to character set utf8 collate utf8_unicode_ci;\") AS ExecuteTheString
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA=\"$SCHEMA\"
AND TABLE_TYPE=\"BASE TABLE\""

echo "SET foreign_key_checks = 0;" > /tmp/fix_coll_$SCHEMA.sql
echo $QUERY | mysql -u $DBUSER -h $DBHOST --password=$DBPASS -D $SCHEMA --skip-column-names >> /tmp/fix_coll_$SCHEMA.sql
echo "SET foreign_key_checks = 1;" >> /tmp/fix_coll_$SCHEMA.sql
cat /tmp/fix_coll_$SCHEMA.sql | mysql -u $DBUSER -h $DBHOST --password=$DBPASS -D $SCHEMA

rm /tmp/fix_coll_$SCHEMA.sql
