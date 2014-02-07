#
# Cookbook Name:: kaltura
# Recipe:: default
#
# Copyright 2014, Kaltura, Ltd.
#
log "Installing Kaltura all in 1"
bash "setup Kaltura's repo" do
     user "root"
     code <<-EOH
	if ! rpm -q kaltura-release;then
		rpm -ihv "#{node[:kaltura][:KALTURA_RELEASE_RPM]}"
	else
		# if the package is already installed, maybe there's a new verison available.
		# in RPM, it try to update to the same version you have now - it stupidly returns RC 1 and hence the || true.
		rpm -Uhv "#{node[:kaltura][:KALTURA_RELEASE_RPM]}" || true
	fi
     EOH
end
package "kaltura-server" do
  action :install
 end
#%w{ apr apr-util lynx }.each do |pkg|
#  package pkg do
#    action :install
#  end
#end
template "/root/kaltura.ans" do
    source "kaltura.ans.erb"
    mode 0600
    owner "root"
    group "root"
end

bash "setup DWH " do
     user "root"
     code <<-EOH
	#{node[:kaltura][:BASE_DIR]}/bin/kaltura-config-all.sh /root/kaltura.ans
     EOH
end
