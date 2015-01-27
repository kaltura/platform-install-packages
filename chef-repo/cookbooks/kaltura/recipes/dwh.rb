log "Installing Kaltura DWH"
template "/etc/yum.repos.d/kaltura.repo" do
    source "kaltura.repo.erb"
    mode 0600
    owner "root"
    group "root"
end
package "kaltura-dwh" do
  action :install
  Chef::Config[:yum_timeout] = 3600
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
	echo "NO" | #{node[:kaltura][:BASE_DIR]}/bin/kaltura-base-config.sh /root/kaltura.ans
	#{node[:kaltura][:BASE_DIR]}/bin/kaltura-dwh-config.sh /root/kaltura.ans
     EOH
end
