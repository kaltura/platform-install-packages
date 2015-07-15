echo kaltura-base    kaltura-base/admin_console_email        string  @ADMIN_CONSOLE_ADMIN_MAIL@ | debconf-set-selections
echo kaltura-base    kaltura-base/admin_console_passwd_again password        @ADMIN_CONSOLE_PASSWORD@ | debconf-set-selections
echo kaltura-base    kaltura-base/admin_console_passwd_dont_match    note | debconf-set-selections
echo kaltura-base    kaltura-base/admin_console_passwd_invalid_char  note | debconf-set-selections
echo kaltura-base    kaltura-base/admin_console_passwd       password        @ADMIN_CONSOLE_PASSWORD@ | debconf-set-selections
echo kaltura-base    kaltura-base/apache_hostname    string  @KALTURA_VIRTUAL_HOST_NAME@ | debconf-set-selections
echo kaltura-base    kaltura-base/bad_time_zone      note | debconf-set-selections
echo kaltura-base    kaltura-base/cdn_hostname       string  @CDN_HOST@ | debconf-set-selections
echo kaltura-base    kaltura-base/contact_phone      string  +1 800 871 5224 | debconf-set-selections
echo kaltura-base    kaltura-base/contact_url        string  http://corp.kaltura.com/company/contact-us | debconf-set-selections
echo kaltura-base    kaltura-base/db_hostname        string  @DB1_HOST@ | debconf-set-selections
echo kaltura-base    kaltura-base/db_port    string  @DB1_PORT@ | debconf-set-selections
echo kaltura-base    kaltura-base/dwh_db_hostname    string  @DB1_HOST@ | debconf-set-selections
echo kaltura-base    kaltura-base/dwh_db_port        string  @DB1_PORT@ | debconf-set-selections
echo kaltura-base    kaltura-base/env_name   string  Kaltura Video Platform | debconf-set-selections
echo kaltura-base    kaltura-base/install_analytics_consent  Boolean false | debconf-set-selections
echo kaltura-base    kaltura-base/install_analytics_email    string @YOUR_EMAIL@ | debconf-set-selections
echo kaltura-base    kaltura-base/ip_range   string  @IP_RANGE@ | debconf-set-selections
echo kaltura-base    kaltura-base/media_server_hostname      string | debconf-set-selections
echo kaltura-base    kaltura-base/mysql_super_passwd password        @MYSQL_ROOT_PASSWD@ | debconf-set-selections
echo kaltura-base    kaltura-base/mysql_super_user   string  root | debconf-set-selections
echo kaltura-base    kaltura-base/second_sphinx_hostname     string  @SPHINX_SERVER1@ | debconf-set-selections
echo kaltura-base    kaltura-base/service_url        string  @SERVICE_URL@ | debconf-set-selections
echo kaltura-base    kaltura-base/sphinx_hostname    string  @SPHINX_SERVER2@ | debconf-set-selections
echo kaltura-base    kaltura-base/time_zone  string @TIME_ZONE@| debconf-set-selections
echo kaltura-base    kaltura-base/vhost_port string  @KALTURA_VIRTUAL_HOST_PORT@ | debconf-set-selections
echo kaltura-base    kaltura-base/vod_packager_hostname      string  @VOD_PACKAGER_HOST@ | debconf-set-selections
echo kaltura-base    kaltura-base/vod_packager_port  string  @VOD_PACKAGER_PORT@ | debconf-set-selections

echo kaltura-db      kaltura-db/db_already_installed boolean false | debconf-set-selections
echo kaltura-db      kaltura-db/db_hostname  string  @DB1_HOST@ | debconf-set-selections
echo kaltura-db      kaltura-db/db_port      string  3306 | debconf-set-selections
echo kaltura-db      kaltura-db/fix_mysql_settings   boolean true | debconf-set-selections
echo kaltura-db      kaltura-db/mysql_super_passwd   password        @MYSQL_ROOT_PASSWD@ | debconf-set-selections
echo kaltura-db      kaltura-db/mysql_super_user     string  root | debconf-set-selections
echo kaltura-db      kaltura-db/remove_db    boolean false | debconf-set-selections


echo kaltura-front   kaltura-front/apache_ssl_cert   string  /etc/ssl/certs/ssl-cert-snakeoil.pem | debconf-set-selections
echo kaltura-front   kaltura-front/apache_ssl_chain  string | debconf-set-selections
echo kaltura-front   kaltura-front/apache_ssl_key    string  /etc/ssl/private/ssl-cert-snakeoil.key | debconf-set-selections
echo kaltura-front   kaltura-front/is_apache_ssl     boolean false | debconf-set-selections
echo kaltura-front   kaltura-front/self_signed_cert  note | debconf-set-selections
echo kaltura-front   kaltura-front/service_url       string  @SERVICE_URL@ | debconf-set-selections
echo kaltura-front   kaltura-front/vhost_port        string  @KALTURA_VIRTUAL_HOST_PORT@ | debconf-set-selections
echo kaltura-front   kaltura-front/web_interfaces    multiselect | debconf-set-selections

echo kaltura-nginx   kaltura-nginx/kaltura_service_url       string  @SERVICE_URL@ | debconf-set-selections
echo kaltura-nginx   kaltura-nginx/nginx_hostname    string  @VOD_PACKAGER_HOST@ | debconf-set-selections
echo kaltura-nginx   kaltura-nginx/nginx_port        string  @VOD_PACKAGER_PORT@ | debconf-set-selections

echo mysql-server-5.5        mysql-server/root_password_again        password @MYSQL_ROOT_PASSWD@ | debconf-set-selections
echo mysql-server-5.5        mysql-server/root_password      password @MYSQL_ROOT_PASSWD@ | debconf-set-selections
