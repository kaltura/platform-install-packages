# Contributing Code to the Kaltura Platform
Kaltura is a multi-project platform. It consists of various back-end and front-end projects, written in several programming languages using different FOSS frameworks/libraries/technologies.
This document was put together to guide you as a developer getting started with Kaltura, walk you through the different repos and the best practices when contributing code.

## Signing the Contributor License Agreement
When you merge new code to the Kaltura Platform, we require that you sign the Kaltura Contributor License Agreement (or "CLA"). The CLA license is for your protection as a Contributor as well as the protection of the Project and its community members. It does not change your rights to use your own Contributions for any other purpose, and does not require any IP assignment of any kind.
If you're working on a Kaltura project, or can clearly claim ownership of copyright in what you'll be contributing to the project, the CLA will ensure that your contributions are protected and that the project will forever remain free to be used and modified by the global community. 

As references, we encourage reviewing other known projects and their respective CLAs - 
* [The Apache Software Foundation](http://www.apache.org/licenses/#clas).
* [The Fedora Project](https://fedoraproject.org/wiki/Legal:Fedora_Project_Contributor_Agreement).
* [Ubuntu, Canonical Projects](http://www.canonical.com/contributors).
* [MongoDB](http://www.mongodb.com/legal/contributor-agreement).

Please [CLICK HERE TO SIGN](https://agentcontribs.kaltura.org) the Kaltura CLA digitally using your GitHub account. 
You can also [download the Kaltura CLA in PDF format](http://knowledge.kaltura.com/node/1235/attachment/field_media), sign it and email to [community@kaltura.com](mailto:community@kaltura.com).

## Which Repositories Should I Contribute To?
The main repos are:

* https://github.com/kaltura/platform-install-packages - The Platform Install Packages and Scripts
* https://github.com/kaltura/server - The Core Backend (The Kaltura Server)
* https://github.com/kaltura/nginx-vod-module - NGINX-based MP4 Repackager
* https://github.com/kaltura/mwEmbed - The Kaltura v2 Player Framework (AKA Universal or v2 Player)
* https://github.com/kaltura/playkit-js - The Kaltura v3 Player Framework (AKA PlayKit)
* https://github.com/kaltura/kmcng - The Kaltura Management Console (aka KMCng)
* https://github.com/kaltura/player-studio - The HTML5 Player Studio (aka Studio v2)

If you are uncertain as to which project a specific code belongs to, please run:

```
$ rpm -qf /path/to/file
$ rpm -qi package | grep URL
```

or, if using a deb based distro (Debian/Ubuntu):
```
$ dpkg -S /path/to/file
```

For example:

```bash
$ rpm -qf /opt/kaltura/app/batch/bootstrap.php 
kaltura-base-9.16.0-1.noarch

$ rpm -qi kaltura-base | grep URL
URL         : https://github.com/kaltura/server/tree/IX-9.16.0
```

In this case, the file belongs to Kaltura's Core at `https://github.com/kaltura/server`

## Reporting issues
When reporting an issue, please make sure you include the version used.
```
# You can get the version using:
$ rpm -q package
# or when using the deb packages:
$ dpkg -l package
# And you can get debug information (handy with reporting issues) using:
$ /opt/kaltura/bin/kaltura-sanity.sh
```

This can help you diagnose the issue by yourself, if it does not, include the resulting output in your report.
For questions, rather bug reports, please post at https://forum.kaltura.org.

## Contribution Guidelines
* Please submit separate pull requests per feature/bug (it makes reviewing and approving code contributions easier)
* Every commit should have a meaningful description
* If the code has unit tests, they must pass before the pull request can be merged
* When submitting a new feature, unit tests must be written and included in the pull
* Whenever possible, implement features as plugins, not by modifying Core code
* Always keep performance in mind

## Submitting Pull requests
1. Fork the default branch of the relevant repo
2. Create a branch with a meaningful name; i.e - some-feature-name-fix
3. Make a pull request

Thank you for helping make Kaltura even more awesome! :)
