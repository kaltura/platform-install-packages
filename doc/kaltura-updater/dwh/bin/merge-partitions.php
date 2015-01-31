<?PHP

echo "\nDrop partitioning\n";

$root = $argv[1];
$pw = $argv[2];

if ( !$root || !$pw ){
	die("\nplease configure as follows: drop-partitioning.php [mysql super user] [mysql password]\n");
}

mysql_connect('localhost',$root,$pw);
mysql_select_db('information_schema');


mysql_query("grant all privileges on *.* to 'etl'@'localhost';");
mysql_query("grant all privileges on *.* to 'etl'@'127.0.0.1';");

$partitions = mysql_query("SELECT DISTINCT TABLE_SCHEMA, TABLE_NAME, PARTITION_EXPRESSION FROM `PARTITIONS` where PARTITION_NAME is not null AND TABLE_SCHEMA = 'kalturadw'");
$value = date('Ymd');
$name = date('Ymd', time() - 24*60*60 );

while ( $partition = mysql_fetch_array($partitions ) ){
	list($schema,$table,$column) = $partition;
	echo "Dropping {$schema}.{$table}:{$column}\n";
	mysql_query("ALTER TABLE {$schema}.{$table} REMOVE PARTITIONING;");

	echo "- Creating archive partition p_{$name} {$value}\n";
	mysql_query("ALTER TABLE {$schema}.{$table} PARTITION BY RANGE ({$column}) (partition p_{$name} VALUES LESS THAN ({$value}));");
	echo mysql_error();
}