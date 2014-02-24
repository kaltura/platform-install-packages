log "Installing Kaltura DWH"
if platform?("redhat", "centos", "fedora")
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
		yum clean all
	     EOH
	end
end
package "kaltura-dwh" do
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
	#{node[:kaltura][:BASE_DIR]}/bin/kaltura-base-config.sh /root/kaltura.ans
	#{node[:kaltura][:BASE_DIR]}/bin/kaltura-dwh-config.sh /root/kaltura.ans
     EOH
end
