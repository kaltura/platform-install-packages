template "/etc/yum.repos.d/kaltura.repo" do
    source "kaltura.repo.erb"
    mode 0600
    owner "root"
    group "root"
end
log "Installing Kaltura Sphinx"
package "kaltura-sphinx" do
  action :install
 end

template "/root/kaltura.ans" do
    source "kaltura.ans.erb"
    mode 0600
    owner "root"
    group "root"
end

bash "setup sphinx node" do
     user "root"
     code <<-EOH
	#{node[:kaltura][:BASE_DIR]}/bin/kaltura-mysql-settings.sh
        #{node[:kaltura][:BASE_DIR]}/bin/kaltura-base-config.sh /root/kaltura.ans
        #{node[:kaltura][:BASE_DIR]}/bin/kaltura-sphinx-config.sh /root/kaltura.ans
     EOH
end

