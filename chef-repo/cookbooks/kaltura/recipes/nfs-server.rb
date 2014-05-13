group "kaltura" do
  gid 7373
end

user "kaltura" do
  uid 7373
  home "/opt/kaltura"
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

directory "/opt/kaltura" do
  owner "kaltura"
  group "apache"
  mode 00775
  action :create
end

directory "/opt/kaltura/web" do
  owner "kaltura"
  group "apache"
  mode 00775
  action :create
end

nfs_export "/opt/kaltura/web" do
  network '*'
  writeable true 
  sync true
  options ['no_root_squash']
end
