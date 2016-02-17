# Recipe contributed by Dudy Kohen <admin@panda-os.com>
# Creates needed users [kaltura and apache] on the NFS server.
#
group "kaltura" do
  gid 7373
end

user "kaltura" do
  uid 7373
  home "#{node[:kaltura][:BASE_DIR]}"
  supports :manage_home => false
  shell "/bin/bash"
  gid "kaltura"
  comment "Kaltura Server"
end

group "apache" do
  gid 48
  members "kaltura"
end

user "apache" do
  uid 48
  shell "/sbin/nologin"
  home "/var/www"
  system true
  gid "apache"
  supports :manage_home => false
  comment "Apache"
end

directory "#{node[:kaltura][:BASE_DIR]}" do
  owner "kaltura"
  group "apache"
  mode 0775
  action :create
end

directory "#{node[:kaltura][:BASE_DIR]}/web" do
  owner "kaltura"
  group "apache"
  mode 0775
  action :create
end

nfs_export "#{node[:kaltura][:BASE_DIR]}/web" do
  network '*'
  writeable true 
  sync true
  options ['no_root_squash']
end
