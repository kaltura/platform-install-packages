# Frequently Asked Questions

### Before You Get Started Notes
* If you see a `#` at the beginning of a line, this line should be run as `root`.

### Changing Apache configurations post install.

Sometimes, you may want to change deployment settings post installation, for example: replacing the domain, port or protocol, or changing the system to use SSL or stop using SSL.   
You can run `/opt/kaltura/bin/kaltura-front-config.sh` as many times as you'd like with different values. The script will re-configure the system accordingly.   
For instance, you may want to change the service URL, port or protocol.

Edit the answers file you've used to install Kaltura, then run:   
`# /opt/kaltura/bin/kaltura-front-config.sh /path/to/updated/ans/file`

If you've lost your installation answers file, you can recreate one using the [Kaltura Install Answers File Example](https://github.com/kaltura/platform-install-packages/blob/master/doc/kaltura.template.ans).

### Deploy Local Repository for Offline Install

On rare ocaasions, you may encounter the need to deploy Kaltura on an offline environment where internet connection is not available, and thus you can't reach the Kaltura packages install repository (http://installrepo.kaltura.org/releases/).

On such cases, the solution is to download the packages, deploy a local repository and install from it instead of the online repository.   
**Note** that when following this path, you will need to re-deploy your local repository for every new version upgrade.

To perform an offline install, follow the [Deploy Local Repository for Offline Install guide](https://github.com/kaltura/platform-install-packages/blob/master/doc/deploy-local-rpm-repo-offline-install.md).

### Fresh Database Installation

On occasions where you'd like to drop the database and content and re-install Kaltura. Follor the below commands:    
```bash
# /opt/kaltura/bin/kaltura-drop-db.sh
# /opt/kaltura/bin/kaltura-config-all.sh [answers-file-path]
```

### Troubleshooting Help

If you ever come across issues with your deployment, increase log verbosity to 7 using the following method.        
Run the following command:    
```bash
# sed -i 's@^writers.\(.*\).filters.priority.priority\s*=\s*7@writers.\1.filters.priority.priority=4@g' /opt/kaltura/app/configurations/logger.ini
```
Then restart your Apache.    

Run `# kaltlog`, which will continuously track (using `tail`) an error grep from all Kaltura log files.

You can also use: `# allkaltlog` (using root), which will dump all the error lines from the Kaltura logs once. Note that this can result in a lot of output, so the best way to use it will be to redirect to a file: `# allkaltlog > errors.txt`.
This output can be used to analyze past failures but for active debugging use the kaltlog alias.   
