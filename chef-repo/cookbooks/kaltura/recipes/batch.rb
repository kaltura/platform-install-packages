log "Installing Kaltura batch"
#if platform?("redhat", "centos", "fedora")
#	bash "setup Kaltura's repo" do
#	     user "root"
#	     code <<-EOH
#	     echo Platform is #{node['platform']}
#		if ! rpm -q kaltura-release;then
#			rpm -ihv "#{node[:kaltura][:KALTURA_RELEASE_RPM]}"
#		else
#			# if the package is already installed, maybe there's a new verison available.
#			# in RPM, it try to update to the same version you have now - it stupidly returns RC 1 and hence the || true.
#			rpm -Uhv "#{node[:kaltura][:KALTURA_RELEASE_RPM]}" || true
#		fi
#		yum clean all
#	     EOH
#	end
#end
template "/etc/yum.repos.d/kaltura.repo" do
    source "kaltura.repo.erb"
    mode 0600
    owner "root"
    group "root"
end
package "kaltura-batch" do
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

bash "setup batchMgr daemon" do
     user "root"
     code <<-EOH
	#{node[:kaltura][:BASE_DIR]}/bin/kaltura-base-config.sh /root/kaltura.ans
	#{node[:kaltura][:BASE_DIR]}/bin/kaltura-batch-config.sh /root/kaltura.ans
     EOH
end
