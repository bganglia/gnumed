
#reads the filelist generated by bootstrap-parse and approximates a 
#gnumed schema install as per redo-max.sh , which is broken currently in cygwin

sql_path=../../server/sql
bootstrap_path=../../server/bootstrap
python bootstrap-parse.py $bootstrap_path/bootstrap-monolithic_core.conf filelist;

echo 
echo
echo **  THIS SCRIPT assumes the root windows postgres user is postgres.

echo dropdb -Upostgres -h127.0.0.1 gnumed
dropdb  -h127.0.0.1 -Upostgres gnumed
echo createdb -h.127.0.0.1 -Upostgres gnumed
createdb -h127.0.0.1 -Upostgres gnumed

echo creatuser -h127.0.0.1 -Upostgres -a -d -e -P  gm-dbo 
createuser -h127.0.0.1 -Upostgres -a -d -e -P gm-dbo 
echo enter password for gm-dbo
createlang -d gnumed -h127.0.0.1 -Ugm-dbo "plpgsql"
rm all
touch all

echo create group \"gm-public\"\; >> all
echo create group \"gm-doctors\"\; >> all
echo create user \"any-doc\" with password \'any-doc\' in group \"gm-doctors\", \"gm-public\"\; >> all

for  x in `cat filelist`;do
	cat $sql_path/$x >> all
done

#some of the country specific data is needed, such as enum_ext_id_types
sh append_local_schema.sh

x=all
echo psql -Ugm-dbo -f $x -h127.0.0.1 gnumed
echo **  enter password for gm-dbo
psql -f$x -Ugm-dbo -h127.0.0.1 gnumed 2>> err


sh append_test_data.sh

