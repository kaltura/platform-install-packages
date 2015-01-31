<?php
/**
 * @package Core
 * @subpackage externalWidgets
 */
class embedIframeJsAction extends sfAction
{
	/**
	 * Will forward to the regular swf player according to the widget_id
	 */
	public function execute()
	{
		$uiconf_id = $this->getRequestParameter('uiconf_id');
		if(!$uiconf_id)
			KExternalErrors::dieError(KExternalErrors::MISSING_PARAMETER, 'uiconf_id');
			
		$uiConf = uiConfPeer::retrieveByPK($uiconf_id);
		if(!$uiConf)
			KExternalErrors::dieError(KExternalErrors::UI_CONF_NOT_FOUND);
			
		$partner_id = $this->getRequestParameter('partner_id', $uiConf->getPartnerId());
		if(!$partner_id)
			KExternalErrors::dieError(KExternalErrors::MISSING_PARAMETER, 'partner_id');

		$widget_id = $this->getRequestParameter("widget_id", '_' . $partner_id);
		
		$protocol = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] == 'on') ? "https" : "http";
		$embed_host = (kConf::hasParam('cdn_api_host')) ? kConf::get('cdn_api_host') : kConf::get('www_host');
		$embed_host_https = (kConf::hasParam('cdn_api_host_https')) ? kConf::get('cdn_api_host_https') : kConf::get('www_host');
		$host = ($protocol == 'https') ? 'https://' . $embed_host_https : 'http://' . $embed_host;

		$ui_conf_html5_url = $uiConf->getHtml5Url();

		if (kConf::hasMap("optimized_playback"))
		{
			$optimizedPlayback = kConf::getMap("optimized_playback");
			if (array_key_exists($partner_id, $optimizedPlayback))
			{
				// force a specific kdp for the partner
				$params = $optimizedPlayback[$partner_id];
				if (array_key_exists('html5_url', $params))
				{
					$ui_conf_html5_url = $params['html5_url'];
				}
			}
		}

		$autoEmbed = $this->getRequestParameter('autoembed');
		if ($autoEmbed)
		{
			//$port = $_SERVER['SERVER_PORT'];
			$host = "$protocol://" . kConf::get('html5lib_host').'/';// . ":$port/";
		}

		$iframeEmbed = $this->getRequestParameter('iframeembed');
		$scriptName = ($iframeEmbed) ? 'mwEmbedFrame.php' : 'mwEmbedLoader.php';
		if($ui_conf_html5_url && $iframeEmbed) {
			$ui_conf_html5_url = str_replace('mwEmbedLoader.php', 'mwEmbedFrame.php', $ui_conf_html5_url);
		}

		$relativeUrl = true; // true if ui_conf html5_url is relative (doesnt start with an http prefix)

		if( kString::beginsWith( $ui_conf_html5_url , "http") )
		{
			$relativeUrl = false;
			$url = $ui_conf_html5_url; // absolute URL
		}
		else if ($ui_conf_html5_url)
		{
			$url =  $host . $ui_conf_html5_url;
		}
		else
		{
			$html5_version = kConf::get('html5_version');
			$url =  "$host/html5/html5lib/{$html5_version}/" . $scriptName;
		}

		// append uiconf_id and partner id for optimizing loading of html5 library. append them only for "standard" urls by looking for the mwEmbedLoader.php/mwEmbedFrame.php suffix
		if (kString::endsWith($url, $scriptName))
		{
			$url .= "/p/$partner_id/uiconf_id/$uiconf_id";

			if (!$autoEmbed) // auto embed will include any query string parameter anyway
			{
				$entry_id = $this->getRequestParameter('entry_id');
				if ($entry_id)
					$url .= "/entry_id/$entry_id";
			}
		}
		
		header("pragma:");

		if($iframeEmbed) {
			$url .= ((strpos($url, "?") === false) ? "?" : "&") . 'wid=' . $widget_id . '&' . $_SERVER["QUERY_STRING"];
		} else if ($autoEmbed) {
			header('Content-Type: application/javascript');
			$params = "protocol=$protocol&".$_SERVER["QUERY_STRING"];

			$url .= ((strpos($url, "?") === false) ? "?" : "&") . $params;

			if ($relativeUrl)
			{
				kFileUtils::dumpUrl($url."?".$params, true, false, array("X-Forwarded-For" =>  requestUtils::getRemoteAddress()));
			}
		}

		requestUtils::sendCachingHeaders(60);
		
		kFile::cacheRedirect($url);
		header("Location:$url");
		KExternalErrors::dieGracefully();
	}
}
