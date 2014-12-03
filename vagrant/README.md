### Using Vagrant to install Kaltura Server

[Vagrant](https://www.vagrantup.com/) is a tool to create portable development environments. We provide a Vagrantfile and some shell scripts that allow to leverage that tool to easily create a virtual machine with a fully working Kaltura Server.

Please note that the created server is only meant for development / testing purposes and is **_NOT SECURED_** or performant enough to use for production.
In order to better secure it: 
* Please edit vagrant/kaltura-install.sh: comment out the iptables flushing, stopping and disable from init and replace with proper rules
* Edit vagrant/kaltura-install-config.sh: set proper passwds for MySQL root user and the Kaltura admin user 

#### Installation / Usage guide

* [Install Vagrant](https://www.vagrantup.com/downloads.html)
* [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads) (Other virtual machine providers such as VMWare should work as well but we only tested it with VirtualBox)
* Copy the vagrant directory from within the platform-install-packages
* Edit vagrant/Vagrantfile and replace:
```
  config.vm.network "private_network", ip: ""
```
with the IP you wish to set for the host.
* Modify the values in kaltura-install-config.sh according to your needs
* See the [Vagrant documentation](https://docs.vagrantup.com/) on how to use and configure the vagrant machine.
* To setup the machine:
* $ cd vagrant
* $ vagrant up
* The setup of the machine will take a while - it will download around 1.6GB of packages.
* If the hostname you wish to use is not resolved by DNS, you should add the following to your hosts file:
* $IP_SET_IN_CONF $DOMAIN_SET_IN_VAGRANT_CONF
* You can now access your server at http://$DOMAIN_SET_IN_VAGRANT_CONF/admin_console
* You can see the username/password in kaltura-install-config.sh
* The server's root user password is 'vagrant', make sure to change it once logged in.
