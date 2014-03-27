# Deploying Kaltura using Opscode Chef

This guide is intended for users of Chef that would like to deploy Kaltura clusters using [Chef recipes](http://docs.opscode.com/essentials_cookbook_recipes.html).   

### Before You Get Strated Notes

* Please review the [frequently answered questions](https://github.com/kaltura/platform-install-packages/blob/master/doc/kaltura-packages-faq.md) document for general help before posting to the forums or issue queue.
* If you don't know what Chef is, start by reading [An Overview of Chef](http://docs.opscode.com/chef_overview.html).
* If you're looking to install Kaltura on a signle machine, see: [Installing Kaltura on a Single All-In-One Server (RPM)](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md)
* If you're looking to deploy a cluster manually or using other automation tools, see [Deploying Kaltura Clusters](https://github.com/kaltura/platform-install-packages/blob/master/doc/rpm-cluster-deployment-instructions.md).
* [Kaltura Inc.](http://corp.kaltura.com) also provides commercial editions including pro-active platform monitoring, applications, SLA, 24/7 support and professional services. If you're looking for a commercially supported version with integrations to commercial encoders, streaming servers, eCDN, DRM and more - Start a [Free Trial on Kaltura.com Hosted Platform](http://corp.kaltura.com/free-trial) or [Kaltura' Commercial OnPrem Edition™](http://corp.kaltura.com/Deployment-Options/Kaltura-On-Prem-Edition). For existing RPM based users, Kaltura offers commercial upgrade options.

## Installing the Chef server

1. Request this page: http://www.getchef.com/chef/install/
1. Select the 'Chef Server' tab
1. Select your distribution, version and arch and download
    1. Download the RPM or deb package depending on your distribution.   
    1. The post install will provide instructions as to what else needs to be done to set the instance up.   
1. Obtain chef-repo from https://github.com/kaltura/platform-install-packages.git  
1. Upload the Kaltura recipes to your Chef server using: `# knife cookbook upload kaltura`
1. We also recommend you use the ready made recipes for MySQL and NFS which can be taken from here:
    1. http://community.opscode.com/cookbooks/mysql
    1. http://community.opscode.com/cookbooks/nfs

## Bootstrapping clients
Run the following:
```
# curl -L https://www.opscode.com/chef/install.sh|sh
# mkdir -p /etc/chef
# knife configure client /etc/chef
```

Copy `/etc/chef/validation.pem` from your Chef server onto `/etc/chef`     

Create `/etc/chef/client.rb` and paste the following lines into it.   
**Make sure to modify your Chef server url**
```
log_level :info
log_location STDOUT
chef_server_url 'http://yourchefserver.com:4000'
validation_client_name 'chef-validator'
```
The run: `# chef-client -i 3600`   

**Repeat this action for each node in your Kaltura cluster.**

To test it, on the Chef server, run: 
```
# knife node list
```
You should see your new nodes when running:
```
[root@chef-server ~]# knife node list
kalturadev
front.kaltura.dev
batch.kaltura.dev
dwh.kaltura.dev
nfs
```

Alternatively, log in to Chef's web with https://chef-server/   
You should see your added nodes under the "Nodes" tab as well as the "Clients" tab.

## Loading the NTP and MySQL recipes to your Chef server
Download NTP and MySQL recipes:

1. http://community.opscode.com/cookbooks/ntp
1. http://community.opscode.com/cookbooks/mysql

**These recipes have dependencies you will need as well. Please follow documentation on the above URLs.**

## Loading the Kaltura recipes to your Chef server
```
# git clone https://github.com/kaltura/platform-install-packages.git
# cp -r sources/platform-install-packages/chef-repo/cookbooks/kaltura  /var/chef/cookbooks/kaltura/
# knife cookbook upload --all
```
Then to verify use `# knife cookbook list`.    
You should see output along the lines of:
```
[root@chef ~]# knife cookbook list
build-essential   1.4.2
kaltura           0.1.0
line              0.5.1
mysql             4.0.20
nfs               0.5.0
ntp               1.5.5
openssl           1.1.0
```

## Editing attributes.rb
The properties of your cluster should be set here: `cookbooks/kaltura/attributes/default.rb`   
When done editing, run:
```
# knife cookbook upload kaltura
```

## Defining recipe run lists
Now that we have our cluster nodes registered, and our recipe uploaded to the Chef server, we need to assign a recipe[s] for each node type.
The syntax for it is:
```
# knife node run_list add $NODE_NAME $RECIPE
```
An example cluster deployment will be:
```
# knife node run_list add mynfs nfs::server
# knife node run_list add my-mysql-machine mysql::server 
# knife node run_list add my-mysql-machine mysql::_server_rhel 
# knife node run_list add my-batch-machine nfs 
# knife node run_list add my-batch-machine kaltura::batch 
# knife node run_list add my-sphinx-machine kaltura::sphinx
# knife node run_list add my-sphinx-machine kaltura::db_config
# knife node run_list add my-front-machine  nfs 
# knife node run_list add my-front-machine  kaltura::batch 
# knife node run_list add my-dwh-machine  kaltura::dwh 
# knife node run_list add my-dwh-machine  kaltura::nfs
```

Alternatively, log in to Chef's web I/F with https://chef-server    
And deploy the cluster from the "Nodes"->"Edit" menu.

### Notes 

1. The db_config runs from sphinx because it requires Kaltura's code which there is no reason to deploy on the DB machine.
1. The above run lists are a recommedation, you can of course run more than one role per node.


## Running the Chef client
Installing on a node is done using the chef-client utility.  
Note that the order in which you install the nodes matters!   

It should be as following:
```
$ ssh my-mysql-machine
root@my-mysql-machine:~# chef-client

$ ssh my-front-machine
root@my-front-machine:~# chef-client

$ ssh my-sphinx-machine
root@my-sphinx-machine:~# chef-client

$ ssh my-batch-machine
root@my-batch-machine:~# chef-client

$ ssh my-dwh-machine
root@my-dwh-machine:~# chef-client
```
