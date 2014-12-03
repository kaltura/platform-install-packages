### Using Vagrant to install Kaltura Server

[Vagrant](https://www.vagrantup.com/) is a tool to create portable development environments. We provide a Vagrantfile and some shell scripts that allow to leverage that tool to easily create a virtual machine with a fully working Kaltura Server.

Please note that the created server is only meant for development / testing purposes and is **_NOT SECURED_** or performant enough to use for production.

#### Installation / Usage guide

* [Install Vagrant](https://www.vagrantup.com/downloads.html)
* [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads) (Other virtual machine providers such as VMWare should work as well but we only tested it with VirtualBox)
* Copy the vagrant directory from within the platform-install-packages
* You can modify the values in kaltura-install-config.sh if you wish
* See the [Vagrant documentation](https://docs.vagrantup.com/) on how to use and configure the vagrant machine.
* To setup the machine:
* $ cd vagrant
* $ vagrant up
* The setup of the machine will take a while - it will download around 1.6GB of packages.
* Once It's done you should add the following to your hosts file:
* 192.168.26.26 kaltura.local
* You can now access your server at http://kaltura.local/admin_console
* You can see the username/password in kaltura-install-config.sh
* The server's root user password is 'vagrant'
