log "Installing Kaltura batch"
package "kaltura-batch" do
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

bash "setup batchMgr daemon" do
     user "root"
     code <<-EOH
	"#{node[:kaltura][:install_root]}"/bin/kaltura-batch-config.sh /root/kaltura.ans
     EOH
end
