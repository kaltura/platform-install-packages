#
# Cookbook Name:: kaltura
# Recipe:: default
#
# Copyright 2014, Kaltura, Ltd.
#
template "/etc/yum.repos.d/kaltura.repo" do
    source "kaltura.repo.erb"
    mode 0600
    owner "root"
    group "root"
end
log "Installing Kaltura all in 1"
%w{ mysql-server kaltura-server }.each do |pkg|
  package pkg do
    action :install
  end
end


template "/root/kaltura.ans" do
    source "kaltura.ans.erb"
    mode 0600
    owner "root"
    group "root"
end

bash "setup All in 1" do
     user "root"
     code <<-EOH
	#{node[:kaltura][:BASE_DIR]}/bin/kaltura-mysql-settings.sh
	#{node[:kaltura][:BASE_DIR]}/bin/kaltura-config-all.sh /root/kaltura.ans
     EOH
end
