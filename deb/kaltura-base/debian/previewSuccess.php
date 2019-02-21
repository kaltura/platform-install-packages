<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="lt-ie10 lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="lt-ie10 lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="lt-ie10 lt-ie9"> <![endif]-->
<!--[if lt IE 10]>     <html class="lt-ie10"> <![endif]-->
<!--[if gt IE 8]><!--> <html> <!--<![endif]-->
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<?php if( $entry_id ) { ?>
	<meta property="og:url" content="<?php echo $pageURL; ?>" />
	<meta property="og:title" content="<?php echo addslashes(strip_tags(html_entity_decode($entry_name))); ?>" />
	<meta property="og:description" content="<?php echo addslashes(strip_tags(html_entity_decode($entry_description))); ?>" />
	<meta property="og:type" content="video.other" />
	<meta property="og:image" content="<?php echo $entry_thumbnail_url; ?>/width/<?php echo $uiConf->getWidth();?>" />
	<meta property="og:image:secure_url" content="<?php echo $entry_thumbnail_secure_url; ?>/width/<?php echo $uiConf->getWidth();?>" />
	
	<?php if( isset($flavor_asset_id) ) { ?>
	<meta property="og:video" content="<?php echo $flavorUrl; ?>" />
	<meta property="og:video:type" content="video/mp4" />
	<?php } ?>
	<meta property="og:video:url" content="<?php echo $playerUrl; ?>">
	<meta property="og:video:secure_url" content="<?php echo $playerUrl; ?>">
	<meta property="og:video:type" content="text/html">	
	<meta property="og:video:width" content="<?php echo $uiConf->getWidth();?>" />
	<meta property="og:video:height" content="<?php echo $uiConf->getHeight();?>" />	

	<meta name="twitter:card" content="player"/>
    <meta name="twitter:site" content="@kaltura"/>
    <meta name="twitter:creator" content="@kaltura"/>
    <meta name="twitter:title" content="<?php echo htmlspecialchars($entry_name); ?>" />
    <meta name="twitter:description" content="<?php echo htmlspecialchars($entry_description); ?>" />
    <meta name="twitter:image" content="<?php echo $entry_thumbnail_secure_url; ?>/width/<?php echo $uiConf->getWidth();?>" />
    <meta name="twitter:player" content="<?php echo $playerUrl; ?>" />
    <?php if( isset($flavorUrl) ) { ?>
    <meta name="twitter:player:stream" content="<?php echo $flavorUrl; ?>" />
    <?php } ?>
	<meta name="twitter:player:stream:content_type" content="video/mp4"/>
    <meta name="twitter:player:height" content="<?php echo $uiConf->getHeight();?>" />
    <meta name="twitter:player:width" content="<?php echo $uiConf->getWidth();?>" />

	<meta property="og:site_name" content="Kaltura" />
	<?php } ?>
	<title><?php echo htmlspecialchars($entry_name); ?></title>
	<link type="text/css" rel="stylesheet" href="/lib/css/shortlink.css" />
	<?php if($framed)  { ?>
	<style>
	html, body {margin: 0; padding: 0; width: 100%; height: 100%; } 
	body { background-color: #fff !important; }
	#framePlayerContainer {margin: 0 auto; padding-top: 20px; text-align: center; } 
	object, div { margin: 0 auto; }
	</style>
	<?php } else { ?>
	<style>
	#main .content .title h1 { font-size: 24px; font-weight: bold; }
	#main p { margin-bottom: 20px; font-size: 18px; }
	</style>
	<?php } ?>
	<!--[if lte IE 7]>
	<script src="/lib/js/json2.min.js"></script>
	<![endif]-->
	<script src="/lib/js/jquery-1.8.3.min.js"></script>
	<script src="/lib/js/KalturaEmbedCodeGenerator-1.0.6.min.js"></script>	
</head>
<body>
	<?php if(!$framed) { ?>
	<div id="main" style="position: static;">

		<div class="content">
			<div class="title">
				<h1><?php echo htmlspecialchars($entry_name); ?></h1>
			</div>
			<div class="contwrap">
			<p><?php echo htmlspecialchars($entry_description); ?></p>
			<div id="videoContainer">
	<?php } ?>
				<div id="framePlayerContainer">
<script>
function isObject(item) {
    return item && typeof item === 'object' && !Array.isArray(item);
}

/*!
 * Merge two or more objects together.
 * (c) 2017 Chris Ferdinandi, MIT License, https://gomakethings.com
 * @param   {Boolean}  deep     If true, do a deep (or recursive) merge [optional]
 * @param   {Object}   objects  The objects to merge together
 * @returns {Object}            Merged values of defaults and options
 */
function extend() {
    // Variables
    var extended = {};
    var deep = false;
    var i = 0;

    // Check if a deep merge
    if ( Object.prototype.toString.call( arguments[0] ) === '[object Boolean]' ) {
        deep = arguments[0];
        i++;
    }

    // Merge the object into the extended object
    var merge = function (obj) {
        for (var prop in obj) {
            if (obj.hasOwnProperty(prop)) {
                // If property is an object, merge properties
                if (deep && Object.prototype.toString.call(obj[prop]) === '[object Object]') {
                    extended[prop] = extend(extended[prop], obj[prop]);
                } else {
                    extended[prop] = obj[prop];
                }
            }
        }
    };

    // Loop through each object and conduct a merge
    for (; i < arguments.length; i++) {
        var obj = arguments[i];
        merge(obj);
    }

    return extended;

};

function mergeDeep(target,source) {
    return extend(true,target,source);
}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}
var scriptToEval = ''; 
var code = new kEmbedCodeGenerator(<?php echo json_encode($embedParams); ?>).getCode();
var embedType = '<?php echo $embedType;?>';
var ltIE10 = $('html').hasClass('lt-ie10');
var isPlaykit = '<?php echo $isPlaykit?>';
if (isPlaykit === '1') {
    var data = <?php echo json_encode($embedParams); ?>;
    var width = <?php echo $uiConf->getWidth();?>;
    var height = <?php echo $uiConf->getHeight();?>;
    var playerConfig = {"provider":{"partnerId": data.partnerId,"uiConfId": data.uiConfId},"targetId":"framePlayerContainer"};
    var externalConfig = getParameterByName("playerConfig");
    if (externalConfig){
        try {
            var parsedConfig = JSON.parse(externalConfig);
            playerConfig = mergeDeep(playerConfig,parsedConfig);
        }
        catch(ee){}
    }
	//default
    if (!height) {
        height = 400;
    }
    if (!width) {
        width = 600;
    }
    var codeUrl = "//" + data.securedHost + "/p/" + data.partnerId +"/embedPlaykitJs/uiconf_id/"+ data.uiConfId;
    var iframeURL = codeUrl + "/entry_id/" + data.entryId + "?iframeembed=true";
    var embedCode = '<scr'+'ipt src="'+ codeUrl +'"></scr'+'ipt><scr'+'ipt> var kalturaPlayer = KalturaPlayer.setup('+ JSON.stringify(playerConfig)+');	kalturaPlayer.loadMedia({entryId: "'+ data.entryId +'"})</scr'+'ipt>';
    code = embedCode;
    if (data.embedType === 'iframe') {
        code = '<iframe id="kaltura_player" src="'+iframeURL+'" width="'+ width +'" height="'+height+'" allowfullscreen="" webkitallowfullscreen="" mozallowfullscreen="" allow="autoplay; fullscreen; encrypted-media" frameborder="0" style="width: '+width+'px; height: '+height+'px;" itemprop="video" itemscope="" itemtype="http://schema.org/VideoObject">';
    }
    document.getElementById('framePlayerContainer').style.height = height + 'px';
    document.getElementById('framePlayerContainer').style.width = width + 'px';

}

// IE9 and below has issue with document.write script tag
if( ltIE10 && (embedType == 'dynamic' || embedType == 'thumb') ) {
	$(code).each(function() {
		if( ! this.outerHTML ) return true;
		if( this.nodeName === 'SCRIPT' ) {
			// If we have external script, append to head
			if( this.src ) {
				$.getScript(this.src, function() {
					$.globalEval(scriptToEval);
				});
			} else {
				scriptToEval += this.innerHTML;
			}
		} else {
			// Write any other elements
			document.write(this.outerHTML);
		}
	});
} else {
	document.write(code);
}
</script>
				</div>
<?php if(!$framed) { ?>				
			</div>
<!--<br /><p>This page is for preview only. Not for production use.</p>-->
			</div><!-- end contwrap -->
		</div><!-- end content -->
	</div><!-- end #main -->
<?php } ?>
</body>
</html>
