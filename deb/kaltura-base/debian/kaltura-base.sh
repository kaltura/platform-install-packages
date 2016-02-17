PATH=$PATH:/opt/kaltura/bin
export PATH
alias allkaltlog='grep --color "ERR:\|PHP \|Stack trace:\|CRIT\|\[error\]" /opt/kaltura/log/*.log /opt/kaltura/log/batch/*.log'
alias kaltlog='tail -f /opt/kaltura/log/*.log /opt/kaltura/log/batch/*.log | grep -A 1 -B 1 --color "ERR:\|PHP\|trace\|CRIT\|\[error\]"'
if [ -r /etc/kaltura.d/system.ini ];then
        . /etc/kaltura.d/system.ini
fi
