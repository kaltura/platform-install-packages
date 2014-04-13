log "Configuring Kaltura DB"
template "/etc/yum.repos.d/kaltura.repo" do
    source "kaltura.repo.erb"
    mode 0600
    owner "root"
    group "root"
end
package "kaltura-base" do
  action :install
 end
package "kaltura-postinst" do
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

bash "setup Kaltura DB" do
     user "root"
     code <<-EOH
	#{node[:kaltura][:BASE_DIR]}/bin/kaltura-base-config.sh /root/kaltura.ans
	"#{node[:kaltura][:BASE_DIR]}"/bin/kaltura-db-config.sh #{node[:kaltura][:DB1_HOST]} #{node[:kaltura][:SUPER_USER]} #{node[:kaltura][:SUPER_USER_PASSWD]} #{node[:kaltura][:DB1_PORT]}
     EOH
end
