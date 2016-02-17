<?php

require_once('/opt/kaltura/app/tests/lib/KalturaClient.php');
require_once ('/opt/kaltura/app/tests/monitoring/KalturaMonitorResult.php');

$options = getopt('', array(
	'service-url:',
	'debug',
));

if(!isset($options['service-url']))
{
	echo "Argument service-url is required";
	exit(-1);
}

class KalturaMonitorClientLogger implements IKalturaLogger
{
	function log($msg)
	{
		echo "Client: $msg\n";
	}
}

class KalturaMonitorClient extends KalturaClient
{
	protected function doHttpRequest($url, $params = array(), $files = array())
	{
		$this->addParam($params, 'nocache', true);
		return parent::doHttpRequest($url, $params, $files);
	}
	
	public function extWidget(&$url, array $params, array &$headers, $followLocation = true)
	{
		$url = rtrim($url, '/');
		foreach($params as $param => $value)
			$url .= "/$param/$value";
			
		$ch = curl_init();
	
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_FOLLOWLOCATION, $followLocation);
		
		curl_setopt($ch, CURLOPT_ENCODING, 'gzip,deflate');
		curl_setopt($ch, CURLOPT_USERAGENT, $this->config->userAgent);
		curl_setopt($ch, CURLOPT_TIMEOUT, $this->config->curlTimeout);

		if (isset($this->config->proxyHost)) {
			curl_setopt($ch, CURLOPT_HTTPPROXYTUNNEL, true);
			curl_setopt($ch, CURLOPT_PROXY, $this->config->proxyHost);
			if (isset($this->config->proxyPort)) {
				curl_setopt($ch, CURLOPT_PROXYPORT, $this->config->proxyPort);
			}
			if (isset($this->config->proxyUser)) {
				curl_setopt($ch, CURLOPT_PROXYUSERPWD, $this->config->proxyUser.':'.$this->config->proxyPassword);
			}
			if (isset($this->config->proxyType) && $this->config->proxyType === 'SOCKS5') {
				curl_setopt($ch, CURLOPT_PROXYTYPE, CURLPROXY_SOCKS5);
			}
		}

		// Set SSL verification
		if(!$this->getConfig()->verifySSL)
		{
			curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
			curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 2);
		}
		elseif($this->getConfig()->sslCertificatePath)
		{
			curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
			curl_setopt($ch, CURLOPT_CAINFO, $this->getConfig()->sslCertificatePath);
		}

		// Set custom headers
		curl_setopt($ch, CURLOPT_HTTPHEADER, $this->config->requestHeaders );

		// Save response headers
		curl_setopt($ch, CURLOPT_HEADERFUNCTION, array($this, 'readHeader') );
		
	
		$destinationResource = null;
		if($this->destinationPath)
		{
			$destinationResource = fopen($this->destinationPath, "wb");
			curl_setopt($ch, CURLOPT_FILE, $destinationResource);
		}
		else
		{
			curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		}
		
		$result = curl_exec($ch);
		
		if($destinationResource)
			fclose($destinationResource);
	
		$curlError = curl_error($ch);
		curl_close($ch);
		
		$errCode = null;
		$responseHeaders = $this->getResponseHeaders();
		foreach($responseHeaders as $header)
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
		
		$this->resetRequest();
		return $errCode;
	}
}

$config = parse_ini_file(dirname(__FILE__).'/sanity_config.ini', true);

$serviceUrl = $config['client']['serviceUrl'];
$clientConfig = new KalturaConfiguration();
$clientConfig->partnerId = null;
$clientConfig->serviceUrl = $serviceUrl;

/*foreach($config['client-config'] as $attribute => $value)
	$clientConfig->$attribute = $value;

if(isset($options['debug']))
	$clientConfig->setLogger(new KalturaMonitorClientLogger());
*/
$client = new KalturaMonitorClient($clientConfig);
