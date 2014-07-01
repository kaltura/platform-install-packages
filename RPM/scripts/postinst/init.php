<?php
require_once('/opt/kaltura/app/alpha/config/kConf.php');

$configPath = '/opt/kaltura/bin/sanity_config.ini'; 
if(!file_exists($configPath))
{
        echo "Configuration file [$configPath] does not exist\n";
        exit(-1);
}

$config = parse_ini_file($configPath, true);
if(!$config)
{
        echo "unable to parse configuration file [$configPath]\n";
        exit(-1);
}

function write_ini_file(array $config)
{
        global $configPath;

        $content = array();
        foreach($config as $section => $data)
        {
                if(!is_array($data) || !count($data))
                        continue;

                $content[] = "[$section]";
                foreach($data as $field => $value)
                        $content[] = "$field = \"$value\"";
                $content[] = "";
        }

        file_put_contents($configPath, implode("\n", $content));
}

function cUrl($url, $localFilePath, &$headers, $followLocation = true)
{
        echo "Downloading [$url] ";
        $headerFilePath = "$localFilePath.header";
        $verboseFilePath = "$localFilePath.log";

        $ch = curl_init();

        $chFile = fopen($localFilePath, 'w');
        $chWriteHeader = fopen($headerFilePath, 'w');
        $chStdErr = fopen($verboseFilePath, 'w');

        curl_setopt($ch, CURLOPT_URL, $url);
        //curl_setopt($ch, CURLOPT_HEADER, true);
        curl_setopt($ch, CURLOPT_FILE, $chFile);
        curl_setopt($ch, CURLOPT_WRITEHEADER, $chWriteHeader);
        curl_setopt($ch, CURLOPT_STDERR, $chStdErr);
        curl_setopt($ch, CURLOPT_VERBOSE, true);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, $followLocation);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 2);

        $ret = curl_exec($ch);
        curl_close($ch);

        fclose($chFile);
        fclose($chWriteHeader);
        fclose($chStdErr);

        echo file_get_contents($verboseFilePath);

        $errCode = null;
        $headers = array();
        $headerLines = file($headerFilePath);
        foreach($headerLines as $header)
        {
                if(preg_match('/HTTP\/?[\d.]{0,3} ([\d]{3}) ([^\n\r]+)/', $header, $matches))
                {
                        $errCode = $matches[1];
                        continue;
                }

                $parts = explode(':', $header, 2);
                if(count($parts) != 2)
                        continue;

                list($name, $value) = $parts;
                $headers[trim(strtolower($name))] = trim($value);
        }

        return $errCode;
}

require_once ('/opt/kaltura/web/content/clientlibs/php5/KalturaClient.php');

class SanityTestLogger implements IKalturaLogger
{
        function log($msg)
        {
                //echo "Client: $msg\n";
        }
}

$clientConfig = new KalturaConfiguration();
$clientConfig->setLogger(new SanityTestLogger());
$clientConfig->partnerId = null;
foreach($config['client'] as $field => $value)
        $clientConfig->$field = $value;

$client = new KalturaClient($clientConfig);
?>
