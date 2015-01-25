log "Installing Kaltura VOD Packager"
template "/etc/yum.repos.d/kaltura.repo" do
    source "kaltura.repo.erb"
    mode 0600
    owner "root"
    group "root"
end
package "kaltura-nginx" do
  action :install
 end


template "/root/kaltura.ans" do
    source "kaltura.ans.erb"
    mode 0600
    owner "root"
    group "root"
end

bash "setup Nginx daemon" do
     user "root"
     code <<-EOH
	#{node[:kaltura][:BASE_DIR]}/bin/kaltura-nginx-config.sh /root/kaltura.ans
     EOH
end
