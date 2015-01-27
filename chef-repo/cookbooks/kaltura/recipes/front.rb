template "/etc/yum.repos.d/kaltura.repo" do
    source "kaltura.repo.erb"
    mode 0600
    owner "root"
    group "root"
end

log "Installing Kaltura front"
package "kaltura-front" do
  action :install
  Chef::Config[:yum_timeout] = 3600
 end
%w{ kaltura-front kaltura-widgets kaltura-html5lib kaltura-html5-studio }.each do |pkg|
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

bash "setup front node" do
     user "root"
     code <<-EOH
	#{node[:kaltura][:BASE_DIR]}/bin/kaltura-base-config.sh /root/kaltura.ans
	"#{node[:kaltura][:BASE_DIR]}"/bin/kaltura-front-config.sh /root/kaltura.ans
     EOH
end
