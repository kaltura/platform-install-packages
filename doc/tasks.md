# Admin Console

- Mask passwds in admin console
- Mark mandatory field with '*', red, whatever. For example - the 'Add publisher' form.
- Testme fixes
- format output of testme console in tree-like XML structure
- allow configuration of package and publisher types from admin console
- provide an option to validate a KS, and display what capabilities it provides (especially handy for resolving a missing sview capability)
- when inputting an invalid KS in admin console's sys helper:
```PHP
2014-04-20 05:27:46 [0.000542] [10.0.80.24] [2024683882] [API] [ks->logError] ERR: Hash [>M��!���b�ZHD���] doesn't match sha1 on partner [174].
2014-04-20 05:27:46 [0.000378] [10.0.80.24] [2024683882] [API] [KalturaFrontController->getExceptionObject] CRIT: exception 'Exception' with message 'INVALID_STR' in /opt/kaltura/app/alpha/apps/kaltura/lib/webservices/kSessionUtils.class.php:272
Stack trace: 
#0 /opt/kaltura/app/plugins/admin_console/kaltura_internal_tools/services/KalturaInternalToolsSystemHelperService.php(22): ks::fromSecureString('djJ8MTc0fHK3sNK...')
```

But this is not displayed, instead only: 'Internal server error occurred'
Need to catch the exception and display.

# KMC
- Storage: force 'http' in http delivery URL
- Disallow login to KMC if partner is -2
- Change KMC login to be JS instead of FLASH

# Package
- Add our packages to ClearOS' repo
- (optionally) add package to EPEL

# plugins
- Create a plugin for the Monit monitoring tab in admin console
