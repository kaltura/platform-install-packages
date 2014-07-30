Signing the Kaltura Contributor License Agreement (aka CLA)
===================
When you merge new code to the Kaltura Platform, we require that you sign the Kaltura Contributor License Agreement (or "CLA"). The CLA license is for your protection as a Contributor as well as the protection of the Project and its community members. It does not change your rights to use your own Contributions for any other purpose, and does not require any IP assignment of any kind.
If you're working on a Kaltura project, or can clearly claim ownership of copyright in what you'll be contributing to the project, the CLA will ensure that your contributions are protected and that the project will forever remain free to be used and modified by the global community. 

As references, we encourage reviewing other known projects and their respective CLAs - 
* [The Apache Software Foundation](http://www.apache.org/licenses/#clas).
* [The Fedora Project](https://fedoraproject.org/wiki/Legal:Fedora_Project_Contributor_Agreement).
* [Ubuntu, Canonical Projects](http://www.canonical.com/contributors).
* [MongoDB](http://www.mongodb.com/legal/contributor-agreement).

Please [CLICK HERE TO SIGN](http://agentcontribs.kaltura.org/agreements/KalturaCommunity/platform-install-packages) the Kaltura CLA digitally using your GitHub account. 
You can also [download the Kaltura CLA in PDF format](http://knowledge.kaltura.com/node/1235/attachment/field_media), sign it and email to [community@kaltura.com](mailto:community@kaltura.com).

Which repo should I contribute to?
=================================
The main repos are:

* https://github.com/kaltura/platform-install-packages - The RPMs and install scripts
* https://github.com/kaltura/server - Core Backend
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

Contribution Guidelines
=======================
* Please do not file big Pull Requests. It makes reviewing and ensuring correctness difficult. If possible, break it down in smaller commits/pulls, each related to a specific issue or subject
* Every commit should have a meaningful subject
* If the code has tests, they must pass before submitting the pull request
* When submitting a new feature, unit tests must be submitted as well
* Whenever possible, implement features as plugins, not by modifying Core code
* Always keep performance in mind
* If you are unsure about submitting a Pull request, ask one of the repository owners for clarification

Submitting a contribution
=========================
1. Fork the default branch of the relevant repo
2. Create a branch with a meaningful name; i.e - some-feature-name-fix
3. Commit and make a pull request

Thank you for working with us to make Kaltura even more awesome :)
