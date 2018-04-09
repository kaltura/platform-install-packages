<!DOCTYPE html>
<?php
include_once(__DIR__ . '/../alpha/config/kConf.php');
?>

<!-- This landing page is based on a template taken from https://github.com/BlackrockDigital/startbootstrap-landing-page, license: MIT -->

<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Kaltura Platform Start Page - Getting Started</title>

    <!-- Bootstrap Core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="css/landing-page.css" rel="stylesheet">

    <!-- Custom Fonts -->
    <link href="font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
    <link href="css/google_font.css" rel="stylesheet" type="text/css">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
    <script>
    function subscribe_to_list()
    {
        var email = document.getElementById('email').value;
        var name = document.getElementById('name').value;
        var company = document.getElementById('company').value;
        message=document.getElementById("message");
        message.style.color = 'blue';
	message.innerHTML = 'In progress... This may take a few seconds.';
        $.ajax({
                  type: 'POST',
                  url: 'https://installytics.kaltura.org/report/mailinglist.php',
                  data: {'name': name,'email': email,'company':company},
                  success: function(data){
                      if (data!==null){
                        if (data.indexOf("ERR") !==-1) {
                            message.style.color = 'red';
                        }else{
                            message.style.color = 'green';
                        }
                        message.className='unhidden';
                        message.innerHTML = data;
                        message.style.fontWeight="bold";
                        } 
                      } 
        });
    }
    </script>

</head>

<body>

    <!-- Header -->
    <a name="about"></a>
    <div class="intro-header">
        <div class="container">

            <div class="row">
                <div class="col-lg-12">
                    <div class="intro-message">
                        <h1>Kaltura Video Platform (<?php echo kConf::get('kaltura_version');?>)</h1>
                        <h3>Getting Started With Your Deployment</h3>
                        <hr class="intro-divider">
                        <ul class="intro-links-list">
                            <li>
                                <a href="#adminconsole" class="intro-link"><span class="network-name">Server Admin &amp; Create Accounts</span></a>
                            </li>
                            <li>
                                <a href="#kmc" class="intro-link"><span class="network-name">Manage a Content Account</span></a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

        </div>
        <!-- /.container -->

    </div>
    <!-- /.intro-header -->

    <!-- Page Content -->
    <a name="vid" id="vid"></a>
    <div class="content-section-b">

        <div class="container">

            <div class="row">
                <div class="col-lg-5 col-lg-offset-1 col-sm-push-6  col-sm-6">
                    <hr class="section-heading-spacer">
                    <div class="clearfix"></div>
                    <h2 class="section-heading">Kaltura CE Intro Video</h2>
                    <p class="lead">Take a look at this short video presented by Zohar Babin, Kaltura VP Platform and Community, and get some tips and tricks for how to get started with your new Kaltura Community Edition.</p>
                </div>
                <div class="col-lg-5 col-sm-pull-6  col-sm-6">
			<div style="width: 100%;display: inline-block;position: relative;"> 
				<!--  inner pusher div defines aspect ratio: in this case 16:9 ~ 56.25% -->
				<div id="dummy" style="margin-top: 56.25%;"></div>
				<!--  the player embed target, set to take up available absolute space   -->
				<div id="kaltura_player" style="position:absolute;top:0;left:0;left: 0;right: 0;bottom:0;">
				</div>
			</div>
			<script src="https://cdnapisec.kaltura.com/p/2353151/sp/235315100/embedIframeJs/uiconf_id/42286192/partner_id/2353151"></script> 
			<script> 
			kWidget.embed(
				{ "targetId": "kaltura_player", 
				"wid": "_2353151", 
				"uiconf_id": 42286192, 
				"flashvars": { "streamerType": "auto" }, 
				"cache_st": 1523029447, 
				"entry_id": "1_uhucc5ac" 
				}
			); 
			</script>
                </div>
            </div>

        </div>
    </div>

	<a name="adminconsole" id="adminconsole"></a>
    <div class="content-section-a">

        <div class="container">
            <div class="row">
                <div class="col-lg-5 col-sm-6">
                    <hr class="section-heading-spacer">
                    <div class="clearfix"></div>
                    <h2 class="section-heading">The Kaltura Admin Console<br /><a href="//<?php echo kConf::get('apphome_url_no_protocol')?>/admin_console" target="_blank">Admin Your Platform Backend</a></h2>
                    <p class="lead">The Admin Console makes it easy to manage your Kaltura backend and administer Kaltura accounts. View and access all accounts, manage permissions, register new accounts using templates, view usage reports for each account or the entire group, manage backend services and investigate jobs, and more. <a href="https://knowledge.kaltura.com/kaltura-admin-console-user-manual" target="_blank">Learn more about the Admin Console</a>.</p>
                    <p>As your first step, login to the Admin Console using the credentials provided during the installation, and create a new Kaltura account.</p>
                </div>
                <div class="col-lg-5 col-lg-offset-2 col-sm-6">
                    <img class="img-responsive" src="img/ipad.png" alt="">
                </div>
            </div>

        </div>

    </div>

    </div>

    <a name="kmc" id="kmc"></a>
    <div class="content-section-b">

        <div class="container">

            <div class="row">
                <div class="col-lg-5 col-lg-offset-1 col-sm-push-6  col-sm-6">
                    <hr class="section-heading-spacer">
                    <div class="clearfix"></div>
                    <h2 class="section-heading">KMC: Kaltura Management Console<br /><a href="//<?php echo kConf::get('apphome_url_no_protocol')?>/kmc" target="_blank">Manage Specific Accounts</a></h2>
                    <p class="lead">The KMC is a comprehensive media management application. Perform bulk ingestion/upload, create transcoding profiles, manage metadata and categories, design and configure players, create playlists, view analytics, configure live streaming, distribute content across the web, configure ad campaigns, control access to media, manage your account, users, entitlements and permissions, and much more. <a href="https://knowledge.kaltura.com/node/1606/attachment/field_media" target="_blank">Learn more about the KMC application</a>.</p>
		    <p>Once you have created a Kaltura account in the Admin Console, login to the KMC to get started!</p>
                </div>
                <div class="col-lg-5 col-sm-pull-6  col-sm-6">
                    <img class="img-responsive" src="img/dog.png" alt="">
                </div>
            </div>

        </div>
    </div>
    <a name="newsletter" id="newsletter"></a>
    <div class="content-section-a">

        <div class="container">

            <div class="row">
                <div class="col-lg-5 col-lg-offset-1 col-sm-push-6  col-sm-6">
                    <hr class="section-heading-spacer">
                    <div class="clearfix"></div>
                    <h2 class="section-heading">Register for updates</h2>
                    <p class="lead">Join our mailing list to get release notifications.</p>
		    <form action="javascript:subscribe_to_list()" method="post">
			<fieldset>
			<div class="form-group valid-row">
			    <label for="email">E-mail address: <span class="required">*</span></label>
			    <input id="email" required name="email"  type="text" class="form-control required">
			</div>
			<div class="form-group valid-row">
			    <label for="name">Name: <span class="required">*</span></label>
			    <input id="name" required name="name" class="form-control required">
			</div>
			<div class="form-group valid-row">
			    <label for="company">Company:</label>
			    <input id="company" name="company" class="form-control">
			</div>
			<div class="btn-holder">
			    <input type="submit" class="btn btn-default" value="Register">
			</div>
			</fieldset>
		    </form>
		    </br>
		    <div id="message"></div>
		    </br>

                </div>
                <div class="col-lg-5 col-sm-pull-6  col-sm-6">
                    <img class="img-responsive" src="img/newsletter.png" alt="">
                </div>
            </div>

        </div>

    </div>
	<a name="survey" id="survey"></a>
    <div class="content-section-b">

        <div class="container">
            <div class="row">
                <div class="col-lg-5 col-sm-6">
                    <hr class="section-heading-spacer">
                    <div class="clearfix"></div>
                    <h2 class="section-heading"><a href="https://www.kaltura.com/tiny/u08ud" target="_blank">Send Us Your Feedback</a></h2>
                    <p class="lead">Help us to continue to improve by filling out the <a href="https://www.kaltura.com/tiny/u08ud" target="_blank">Kaltura Community Edition survey</a>.</p>
		    <p>We greatly appreciate your input!</p>
                </div>
                <div class="col-lg-5 col-lg-offset-2 col-sm-6">
                    <img class="img-responsive" src="img/survey.png" alt="">
                </div>
            </div>

        </div>

    </div>

	<a  name="contact"></a>
    <div class="banner">

        <div class="container">

            <div class="row">
                <div class="col-lg-6">
                    <h2>Get in touch:</h2>
                </div>
                <div class="col-lg-6">
                    <ul class="list-inline banner-social-buttons">
                        <li>
                            <a href="https://twitter.com/Kaltura" class="btn btn-default btn-lg"><i class="fa fa-twitter fa-fw"></i> <span class="network-name">@Kaltura</span></a>
                        </li>
                        <li>
                            <a href="https://github.com/kaltura/platform-install-packages/blob/master/doc/Contributing-to-the-Kaltura-Platform.md" class="btn btn-default btn-lg"><i class="fa fa-github fa-fw"></i> <span class="network-name">Contribute</span></a>
                        </li>
                        <li>
                            <a href="https://forum.kaltura.org" class="btn btn-default btn-lg"><i class="fa fa-users fa-fw"></i> <span class="network-name">Forum</span></a>
                        </li>
                    </ul>
                </div>
            </div>

        </div>
        <!-- /.container -->

    </div>
    <!-- /.banner -->

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <ul class="list-inline">
                        <li>
                            <a href="https://www.kaltura.org" target="_blank">Kaltura.org</a>
                        </li>
                        <li class="footer-menu-divider">|</li>
                        <li>
                            <a href="https://corp.kaltura.com" target="_blank">Kaltura.com</a>
                        </li>
                        <li class="footer-menu-divider">|</li>
                        <li>
                            <a href="https://vpaas.kaltura.com" target="_blank">Kaltura VPaaS</a>
                        </li>
                        <li class="footer-menu-divider">|</li>
                        <li>
                            <a href="https://developer.kaltura.com" target="_blank">Kaltura Developer Tools</a>
                        </li>
                    </ul>
                    <p class="copyright text-muted small">Copyright &copy; Kaltura <script type="text/javascript">document.write(new Date().getFullYear());</script>.</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- jQuery -->
    <script src="js/jquery.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.min.js"></script>

</body>

</html>
