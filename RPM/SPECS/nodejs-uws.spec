%global npm_name uws
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 0.13.0
Release: 3
Summary: Highly efficient WebSocket & HTTP library
License: Zlib
URL: https://github.com/uWebSockets/uWebSockets
Source0: http://registry.npmjs.org/%{npm_name}/-/%{npm_name}-%{version}.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch
AutoReq: no
AutoProv: no

%{?nodejs_find_provides_and_requires}

%define npm_cache_dir /tmp/npm_cache_%{name}-%{version}-%{release}

%description
%{summary}

%prep
%setup -q -n package

%build
%nodejs_symlink_deps --build

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr LICENSE README.md binding.gyp package.json src uws.js uws_darwin_46.node uws_darwin_47.node uws_darwin_48.node uws_darwin_51.node uws_linux_46.node uws_linux_47.node uws_linux_48.node uws_linux_51.node uws_win32_48.node uws_win32_51.node %{buildroot}%{nodejs_sitelib}/%{npm_name}
# If any binaries are included, symlink them to bindir here


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}

%doc LICENSE
%doc README.md

%changelog
* Tue Jul 11 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 0.13.0-1
- First release 
