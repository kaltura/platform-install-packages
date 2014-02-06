log "Installing Kaltura front"
package "kaltura-front" do
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

bash "setup frontMgr daemon" do
     user "root"
     code <<-EOH
	"#{node[:kaltura][:install_root]}"/bin/kaltura-front-config.sh /root/kaltura.ans
     EOH
end
