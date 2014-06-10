Sign Kaltura's CLA
===================
http://agentcontribs.kaltura.org/agreements/KalturaCommunity/platform-install-packages

Which repo should I contribue to?
=================================
The main repos are:

* https://github.com/kaltura/platform-install-packages - The RPMs and install scripts
* https://github.com/kaltura/server - Core Beckend
* https://github.com/kaltura/kmc - KMC
* https://github.com/kaltura/kdp - KDP3 player [legacy Flash version]
* https://github.com/kaltura/mwEmbed - HTML5 player [universal v2 player]
* https://github.com/kaltura/player-studio - HTML5 Studio [studio v2]

If you are uncertain where the contribution should go to, please do:
```
$ rpm -qf /path/to/file
$ rpm -qi package | grep URL
```
For example:
```
$ rpm -qf /opt/kaltura/app/batch/bootstrap.php 
kaltura-base-9.16.0-1.noarch
$ rpm -qi kaltura-base | grep URL
URL         : https://github.com/kaltura/server/tree/IX-9.16.0
```

In this case, the file belongs to Kaltura's Core at https://github.com/kaltura/server

Reporting issues
================
When reporting an issue, please make sure you include the version used.
```
# You can get the version using:
$ rpm -q package
```
Also, run:

# /opt/kaltura/bin/kaltura-sanity.sh

This might help you diagnose the issue yourself, if not, paste the results along with your report.

Contribution Guildlines
=======================
* No big Pull Requests. It makes reviewing and ensuring correctness hard. If possible, break it to smaller commits/pulls, each related to a specific issue.
* Every commit must have a meaningful subject
* If the code has tests, they must pass before submitting the pull request.
* When submitting a new feature, unit tests must be submitted as well
* Whenever possible, implement features as plugins, not by modifying Core code.
* Always keep performance in mind 

Submitting a contribution
=========================
0. Fork the default branch of the relevant repo
1. Create a branch with a meaningful name; i.e - some-feature-name-fix
2. Commit and make a pull request

