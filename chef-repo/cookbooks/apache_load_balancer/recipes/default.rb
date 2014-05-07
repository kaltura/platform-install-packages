#
# Cookbook Name:: loadbal
# Recipe:: default
#
# Copyright 2014, Kaltura, inc. 
#
case node['platform_family']
		when 'rhel'
			package "httpd" do
		  		action :install
		 end
			template "/etc/httpd/conf.d/load_balancer.conf" do
			    source "load_balancer.conf.erb"
			    mode 0644
			    owner "root"
			    group "root"
			end

			service "httpd" do
		  		service_name "httpd"
		  		action [ :restart, :enable ]
		  		supports :status => true
			end
		when 'debian'
			package "apache2" do
				action :install
			end

			template "/etc/apache2/sites-available/load_balancer.conf" do
				source "load_balancer.conf.erb"
				mode 0644
				owner "root"
				group "root"
			end
			bash "Enable site load_balancer" do
			     user "root"
			     code <<-EOH
				a2ensite load_balancer.conf
			     EOH
			end
			service "apache2" do
				service_name "apache2"
				action [ :restart, :enable ]
				supports :status => true
			end
end

