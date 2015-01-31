<?php
/**
 * This file store all of mwEmbed local configuration ( in a default svn check out this file is empty )
 *
 * See includes/DefaultSettings.php for a configuration options
 */

// Old kConf path
$kConfPath = '/opt/kaltura/app/alpha/config/kConf.php';
if( ! file_exists( $kConfPath ) ) {
	// New kConf path
	$kConfPath = '../../../app/infra/kConf.php';
	if( ! file_exists( $kConfPath ) ) {
		die('Error: Unable to find kConf.php at ' . $kConfPath);
	}
}
// Load kaltura configuration file
require_once( $kConfPath );

$kConf = new kConf();

// Kaltura HTML5lib Version
$wgKalturaVersion = basename(getcwd()); // Gets the version by the folder name

// The default Kaltura service url:
$wgKalturaServiceUrl = wgGetUrl('cdn_api_host');
// Default Kaltura CDN url:
$wgKalturaCDNUrl = wgGetUrl('cdn_host');
// Default Stats URL
$wgKalturaStatsServiceUrl = wgGetUrl('stats_host');

// SSL host names
if( $wgHTTPProtocol == 'https' ){
	$wgKalturaServiceUrl = wgGetUrl('cdn_api_host_https');
	$wgKalturaCDNUrl = wgGetUrl('cdn_host_https');
	$wgKalturaStatsServiceUrl = wgGetUrl('stats_host_https');
}

// Default Asset CDN Path (used in ResouceLoader.php):
$wgCDNAssetPath = $wgKalturaCDNUrl;

// Default Kaltura Cache Path
$wgScriptCacheDirectory = $kConf->get('cache_root_path') . '/html5/' . $wgKalturaVersion;

$wgLoadScript = $wgKalturaServiceUrl . '/html5/html5lib/' . $wgKalturaVersion . '/load.php';
$wgResourceLoaderUrl = $wgLoadScript;

// Salt for proxy the user IP address to Kaltura API
if( $kConf->hasParam('remote_addr_header_salt') ) {
	$wgKalturaRemoteAddressSalt = $kConf->get('remote_addr_header_salt');
}

// Disable Apple HLS if defined in kConf
if( $kConf->hasParam('use_apple_adaptive') ) {
	$wgKalturaUseAppleAdaptive = $kConf->get('use_apple_adaptive');
}

// Get Kaltura Supported API Features
if( $kConf->hasParam('features') ) {
	$wgKalturaApiFeatures = $kConf->get('features');
}

// Allow Iframe to connect remote service
$wgKalturaAllowIframeRemoteService = true;

// Set debug for true (testing only)
$wgEnableScriptDebug = false;

// A helper function to get full URL of host
function wgGetUrl( $hostKey = null ) {
	global $wgHTTPProtocol, $wgServerPort, $kConf;
	if( $hostKey && $kConf->hasParam($hostKey) ) {
		return $wgHTTPProtocol . '://' . $kConf->get($hostKey) . $wgServerPort;
	}
	return null;
}
