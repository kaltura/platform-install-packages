<?PHP
// Script: Simple PHP Proxy: Get external HTML, JSON and more!
//
// *Version: 1.6, Last updated: 1/24/2009*
// *Update by michael.dale@kaltura.com*
// * added validate xml and content type
// * added X-Forwarded-For header for geoLookup services
//
// @@todo add cache and 304 support ( not very high priority since ad servers are generally 
//		dynamic content. 
// @@todo add crossdomain.xml lookup ( to better emulate flash ) 
//	( Adding crossdomain.xml lookup is important because we pass X-Forward-For header ) 
// 
// Project Home - http://benalman.com/projects/php-simple-proxy/
// GitHub		 - http://github.com/cowboy/php-simple-proxy/
// Source		 - http://github.com/cowboy/php-simple-proxy/raw/master/ba-simple-proxy.php
// 
// About: License
// 
// Copyright (c) 2010 "Cowboy" Ben Alman,
// Dual licensed under the MIT and GPL licenses.
// http://benalman.com/about/license/
// 
// About: Examples
// 
// This working example, complete with fully commented code, illustrates one way
// in which this PHP script can be used.
// 
// Simple - http://benalman.com/code/projects/php-simple-proxy/examples/simple/
// 
// About: Release History
// 
// 1.6 - (1/24/2009) Now defaults to JSON mode, which can now be changed to
//			 native mode by specifying ?mode=native. Native and JSONP modes are
//			 disabled by default because of possible XSS vulnerability issues, but
//			 are configurable in the PHP script along with a url validation regex.
// 1.5 - (12/27/2009) Initial release
// 
// Topic: GET Parameters
// 
// Certain GET (query string) parameters may be passed into ba-simple-proxy.php
// to control its behavior, this is a list of these parameters. 
// 
//	 url - The remote URL resource to fetch. Any GET parameters to be passed
//		 through to the remote URL resource must be urlencoded in this parameter.
//	 mode - If mode=native, the response will be sent using the same content
//		 type and headers that the remote URL resource returned. If omitted, the
//		 response will be JSON (or JSONP). <Native requests> and <JSONP requests>
//		 are disabled by default, see <Configuration Options> for more information.
//	 callback - If specified, the response JSON will be wrapped in this named
//		 function call. This parameter and <JSONP requests> are disabled by
//		 default, see <Configuration Options> for more information.
//	 user_agent - This value will be sent to the remote URL request as the
//		 `User-Agent:` HTTP request header. If omitted, the browser user agent
//		 will be passed through.
//	 send_cookies - If send_cookies=1, all cookies will be forwarded through to
//		 the remote URL request.
//	 send_session - If send_session=1 and send_cookies=1, the SID cookie will be
//		 forwarded through to the remote URL request.
//	 full_headers - If a JSON request and full_headers=1, the JSON response will
//		 contain detailed header information.
//	 full_status - If a JSON request and full_status=1, the JSON response will
//		 contain detailed cURL status information, otherwise it will just contain
//		 the `http_code` property.
// 
// Topic: POST Parameters
// 
// All POST parameters are automatically passed through to the remote URL
// request.
// 
// Topic: JSON requests
// 
// This request will return the contents of the specified url in JSON format.
// 
// Request:
// 
// > ba-simple-proxy.php?url=http://example.com/
// 
// Response:
// 
// > { "contents": "<html>...</html>", "headers": {...}, "status": {...} }
// 
// JSON object properties:
// 
//	 contents - (String) The contents of the remote URL resource.
//	 headers - (Object) A hash of HTTP headers returned by the remote URL
//		 resource.
//	 status - (Object) A hash of status codes returned by cURL.
// 
// Topic: JSONP requests
// 
// This request will return the contents of the specified url in JSONP format
// (but only if $enable_jsonp is enabled in the PHP script).
// 
// Request:
// 
// > ba-simple-proxy.php?url=http://example.com/&callback=foo
// 
// Response:
// 
// > foo({ "contents": "<html>...</html>", "headers": {...}, "status": {...} })
// 
// JSON object properties:
// 
//	 contents - (String) The contents of the remote URL resource.
//	 headers - (Object) A hash of HTTP headers returned by the remote URL
//		 resource.
//	 status - (Object) A hash of status codes returned by cURL.
// 
// Topic: Native requests
// 
// This request will return the contents of the specified url in the format it
// was received in, including the same content-type and other headers (but only
// if $enable_native is enabled in the PHP script).
// 
// Request:
// 
// > ba-simple-proxy.php?url=http://example.com/&mode=native
// 
// Response:
// 
// > <html>...</html>
// 
// Topic: Notes
// 
// * Assumes magic_quotes_gpc = Off in php.ini
// 
// Topic: Configuration Options
// 
// These variables can be manually edited in the PHP file if necessary.
// 
//	 $enable_jsonp - Only enable <JSONP requests> if you really need to. If you
//		 install this script on the same server as the page you're calling it
//		 from, plain JSON will work. Defaults to false.
//	 $enable_native - You can enable <Native requests>, but you should only do
//		 this if you also whitelist specific URLs using $valid_url_regex, to avoid
//		 possible XSS vulnerabilities. Defaults to false.
//	 $valid_url_regex - This regex is matched against the url parameter to
//		 ensure that it is valid. This setting only needs to be used if either
//		 $enable_jsonp or $enable_native are enabled. Defaults to '/.*/' which
//		 validates all URLs.
// 
// ############################################################################

// Include our configuration file
require_once( realpath( dirname( __FILE__ ) ) . '/includes/DefaultSettings.php' );

require_once( dirname( __FILE__ ) . '/modules/KalturaSupport/KalturaCommon.php' );
$requestHelper = $container['request_helper'];

function isValidHost( $url = null ){
	global $kConf;
	
	if(!$url)
		return false;
    $scheme = parse_url($url, PHP_URL_SCHEME);
    if ( $scheme != "http" && $scheme != "https"){
        return false;
    }
	$host = parse_url($url, PHP_URL_HOST);
	if( $host === null ){
		return false;
	}

	// Get our whitelist from kConf
	if( isset( $kConf ) ){
		if( $kConf->hasMap("proxy_whitelist") ){
			$whitelist = $kConf->getMap("proxy_whitelist");
		} else {
			return true;
		}
	} else {
		return true;
	}

	return in_array($host, $whitelist);
}

// Change these configuration options if needed, see above descriptions for info.
$enable_jsonp = true;
$enable_native = false;
$valid_url_regex = '/.*/';

$enable_fullHeaders = true;
$contentType_regex = '/(text|application)\/(xml|x-srt|html|plain|x-pascal)/';
$validateXML = false;
$encodeCDATASections = true;
$proxyCookies = true;
$proxySession = false;

// ############################################################################

$url = isset($_GET['url']) ? urldecode( $_GET['url'] ) : false;
//Replace white spaces with compliant %20
$url = str_replace(" ","%20",$url);
$header ='';
if ( !$url ) {
	
	// Passed url not specified.
	$contents = 'ERROR: url not specified';
	$status = array( 'http_code' => 'ERROR' );
	
} else if ( !preg_match( $valid_url_regex, $url ) ) {
	
	// Passed url doesn't match $valid_url_regex.
	$contents = 'ERROR: invalid url';
	$status = array( 'http_code' => 'ERROR' );
	
} else if( !isValidHost($url) ) {
	// URL host is not whitelisted
	$contents = 'ERROR: URL not in Kaltura domain whitelist [DENIED]';
	$status = array( 'http_code' => 'ERROR' );
} else {
	$ch = curl_init( $url );
	
	// Always follow redirects: 
	curl_setopt( $ch, CURLOPT_AUTOREFERER, true );
		
	// Add a total curl execute timeout of 10 seconds: 
	curl_setopt( $ch, CURLOPT_TIMEOUT, 10 );
	
	if ( strtolower($_SERVER['REQUEST_METHOD']) == 'post' ) {
		curl_setopt( $ch, CURLOPT_POST, true );
		curl_setopt( $ch, CURLOPT_POSTFIELDS, $_POST );
	}
	
	if ( isset( $_GET['send_cookies'] ) || $proxyCookies ) {
		$cookie = array();
		foreach ( $_COOKIE as $key => $value ) {
			$cookie[] = $key . '=' . $value;
		}
		if (	isset( $_GET['send_session'] ) || $proxySession ) {
			@session_start();
			$cookie[] = SID;
		}
		$cookie = implode( '; ', $cookie );
		
		curl_setopt( $ch, CURLOPT_COOKIE, $cookie );
	}
	
	curl_setopt( $ch, CURLOPT_FOLLOWLOCATION, true );
	curl_setopt( $ch, CURLOPT_HEADER, true );
	curl_setopt( $ch, CURLOPT_RETURNTRANSFER, true );

	// Forward the client ip for GeoLookup: ( geo-lookup server hopefully is not dumb and uses X-Forwarded-For ) 
	curl_setopt($ch, CURLOPT_HTTPHEADER, array(
		'X-Forwarded-For: ' . $_SERVER['REMOTE_ADDR'],
		// Add kaltura x-remote-address headers:
		$requestHelper->getRemoteAddrHeader(),
		'Expect:' // used to ignore "100 Continue Header" when using POST
	));
	
	// Forward the user agent:
	curl_setopt( $ch, CURLOPT_USERAGENT, isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '' );
	$parts = preg_split( '/([\r\n][\r\n])\\1/', curl_exec( $ch ), 2 );
	if( count($parts) != 2 ){
	$status = array( 'http_code' => 'ERROR' );
	$contents = curl_error( $ch );
	} else {
	if ( preg_match( '/302 Moved Temporarily/', $parts[0] ) ) {
		$parts = preg_split( '/([\r\n][\r\n])\\1/', $parts[1], 2 );
	}
	list( $header, $contents ) = $parts;
	}
	$status = curl_getinfo( $ch );
	
	curl_close( $ch );
}

// check for empty contents: 
if( trim( $contents ) == '' ){
	$status = array( 'http_code' => 'ERROR' );
	$contents = 'ERROR: empty response';
}

// Be sure to utf8_encode contents so no remote content break JSON encoding
if( mb_detect_encoding($contents, 'UTF-8', true) != "UTF-8" ) {
	$contents = utf8_encode( $contents );
}
// remove leading ? in some kaltura cc xml responses :(
if( is_string( $contents ) && isset($contents[0]) && $contents[0] == '?' ){
	$contents = substr( $contents, 1 );
}

// Split header text into an array.
$header_text = preg_split( '/[\r\n]+/', $header );

if ( isset( $_GET['mode'] ) == 'native' ) {
	if ( !$enable_native ) {
		$contents = 'ERROR: invalid mode';
		$status = array( 'http_code' => 'ERROR' );
	}
	
	// Propagate headers to response.
	foreach ( $header_text as $header ) {
		if ( preg_match( '/^(?:Content-Type|Content-Language|Set-Cookie):/i', $header ) ) {
			header( $header );
		}
	}
	
	print $contents;
	
} else {
	
	// $data will be serialized into JSON data.
	$data = array();
	
	// Propagate all HTTP headers into the JSON data object.
	if ( isset( $_GET['full_headers'] ) || $enable_fullHeaders ) {
		$data['headers'] = array();
		
		foreach ( $header_text as $header ) {
			preg_match( '/^(.+?):\s+(.*)$/', $header, $matches );
			if ( $matches ) {
				$data['headers'][ $matches[1] ] = $matches[2];
			}
		}
	}
	
	// Check if the content type matches filters
	if( $contentType_regex && $status['http_code'] != 'ERROR' ){
			$contentType ='';
			// Servers don't have consistent case for content-type: 
			foreach( $data['headers'] as $headKey=>$headValue){
				if( strtolower( $headKey) == 'content-type' ){
					$contentType =	$headValue;
				}
			}
		if( 0 == preg_match( $contentType_regex, $contentType ) ){
			$status = array( 'http_code' => 'ERROR');
			$contents = "Error invalid content type did not match: " . str_replace( '/', '' , $contentType_regex);		
		}
	}
	
	// Check if we should validate the xml ( by parsing it with simple xml )
	if( $validateXML && $status['http_code'] != 'ERROR' ){
		// OpenX ad Server hack / work around :: Should be utf-8 not UTF_8 !
		$xmlReadyData = str_replace( 'encoding="UTF_8"' , 'encoding="utf-8"' , $contents);
		libxml_use_internal_errors(true);
		if( false === simplexml_load_string( $xmlReadyData ) ){
			$status = array( 'http_code' => 'ERROR');
			$contents = "XML failed to validate";
		}
	}
 
	// Check if there is extra header info leading up to the xml: 
	if( strpos( $contents, '<?xml' ) !== false &&	strpos( $contents, '<?xml' ) != 0 ){
		// strip all leading conetnt 
		$contents = trim( substr( $contents, strpos( $contents, '<?xml' ) ) );
	}
	
	//$encodeCDATASections = false;
	// Check if we should encode CDATA sections: 
	if( $encodeCDATASections ){
		$contents = preg_replace_callback('/\<\!\[CDATA\[(.*?)\]\]>/',
	 		create_function(
	 			'$matches',
				'return htmlentities( $matches[1] );'
	 		), $contents );
	}
	
	
	// Propagate all cURL request / response info to the JSON data object.
	if ( isset( $_GET['full_status'] ) ) {
		$data['status'] = $status;
	} else {
		$data['status'] = array();
		$data['status']['http_code'] = $status['http_code'];
	}
	
	// Set the JSON data object contents, decoding it from JSON if possible.
	$data['contents'] = $contents;
	
	// Generate appropriate content-type header.	
	if( isset(	$_SERVER['HTTP_X_REQUESTED_WITH'] ) ){
		$is_xhr = ( strtolower( $_SERVER['HTTP_X_REQUESTED_WITH'] ) == 'xmlhttprequest' );
	} else {
		$is_xhr = false;
	}
	header( 'Content-type: application/' . ( $is_xhr ? 'json' : 'x-javascript' ) );
	
	// Get JSONP callback.
	$jsonp_callback = $enable_jsonp && isset($_GET['callback']) ? $_GET['callback'] : null;

	// Generate JSON/JSONP string
	$json = json_encode( $data );

	print $jsonp_callback ? "$jsonp_callback($json)" : $json;
}

?>