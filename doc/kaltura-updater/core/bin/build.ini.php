<?php

define ('CONFIG_DIR','/opt/kaltura/app/alpha/config/');
$kConfLocalPath = CONFIG_DIR.'/kConfLocal.php';
$kConfPath = CONFIG_DIR.'/kConf.php';
require_once $kConfLocalPath;
require_once $kConfPath;

class kConfMigrator extends kConf
{
	public static function getAll()
	{
		self::$map = array();
		kConfLocal::addConfig();
		return self::$map;
	}
	
	protected static $file = null; 
	
	protected static function writeArray($prefix, $array)
	{
		fputs(self::$file, "\n");
		
		foreach($array as $field => $value)
		{
			if(is_array($value))
			{
				self::writeArray("$prefix.$field", $value);
			}
			else 
			{
				if(preg_match('/[=()]/', $value))
					$value = "\"$value\"";
					
				fputs(self::$file, "$prefix.$field = $value\n");
			}
		}
	}
	
	public static function writeFile($fileName, $map)
	{
		self::$file = fopen("$fileName.ini", 'w');
		self::writeMap($map);
		fclose(self::$file);
	}
	
	protected static function writeMap($map)
	{
		if(!$map || !is_array($map) || !count($map))
			return;
			
		$arrays = array();
		foreach($map as $field => $value)
		{
			if(is_array($value))
			{
				$arrays[$field] = $value;
			}
			else
			{
				if(preg_match('/[=()]/', $value))
					$value = "\"$value\"";
				
				fputs(self::$file, "$field = $value\n");
			}
		}
		
		foreach($arrays as $field => $value)
		{
			fputs(self::$file, "\n\n[$field]\n");
			foreach($value as $subField => $subValue)
			{
				if(is_array($subValue))
				{
					self::writeArray($subField, $subValue);
				}
				else 
				{
					if(preg_match('/[=()]/', $subValue))
						$subValue = "\"$subValue\"";
					
					fputs(self::$file, "$subField = $subValue\n");
				}
			}
		}
	}
}

if (count($argv) < 2){
	die ('Usage: ' . __FILE__ . " </path/to/new/config/dir>\n");
}
$outdir=$argv[1];
if (!is_dir($outdir) && !mkdir ($outdir)){
	echo "Failed to create $outdir\n";
	exit (1);
}
$local = fopen($outdir.'/local.ini', 'w');
$map = kConfMigrator::getAll();
$db = kConfMigrator::getDB();
$dcConfig = $map['dc_config'];
if (isset($map['v3cache_getfeed_expiry'])){
	$v3cacheGetfeedExpiry = $map['v3cache_getfeed_expiry'];
	kConfMigrator::writeFile($outdir.'/v3cache_getfeed_expiry', $v3cacheGetfeedExpiry);
}
if (isset($map['v3cache_ignore_admin_ks'])){
	$v3cacheIgnoreAdminKS = $map['v3cache_ignore_admin_ks'];
	kConfMigrator::writeFile($outdir.'/v3cache_ignore_admin_ks',$v3cacheIgnoreAdminKS);
}
if (isset($map['optimized_playback'])){
	$optimizedPlayback = $map['optimized_playback'];
	kConfMigrator::writeFile($outdir.'/optimized_playback', $optimizedPlayback);
}
if (isset($map['url_managers'])){
	$urlManagers = $map['url_managers'];
	$urlManagers['override'] = $map['url_managers_override'] ? $map['url_managers_override'] : array();
	kConfMigrator::writeFile($outdir.'/url_managers', $urlManagers);
}
$plugins = $map['default_plugins'];

//v3cache_ignore_admin_ks
//v3cache_getfeed_expiry

kConfMigrator::writeFile($outdir.'/db', $db);
kConfMigrator::writeFile($outdir.'/dc_config',$dcConfig);

unset($map['dc_config']);
unset($map['v3cache_getfeed_expiry']);
unset($map['v3cache_ignore_admin_ks']);
unset($map['optimized_playback']);
unset($map['url_managers']);
unset($map['url_managers_override']);
unset($map['default_plugins']);

$arrays = array();
foreach($map as $field => $value)
{
	if(is_array($value))
	{
		$arrays[$field] = $value;
	}
	else
	{
		if(preg_match('/[=()]/', $value))
			$value = "\"$value\"";
	
		fputs($local, "$field = $value\n");
	}
}

fputs($local, "\n");
foreach($plugins as $plugin)
{
	fputs($local, "default_plugins[] = $plugin\n");
}

foreach($arrays as $field => $value)
{
	fputs($local, "\n\n[$field]\n");
	foreach($value as $subField => $subValue)
	{
		if(is_array($subValue))
		{
			echo "$field/$subField is array\n";
			exit;
		}
		
		if(preg_match('/[=()]/', $subValue))
			$subValue = "\"$subValue\"";
	
		fputs($local, "$subField = $subValue\n");
	}
}

fclose($local);

echo "Done [" . time() . "]. Go to $outdir for the results.\n";
