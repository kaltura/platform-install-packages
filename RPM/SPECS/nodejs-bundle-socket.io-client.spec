%global npm_name socket.io-client
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 2.1.1
Release: 1
Summary: FIXME
License: MIT
URL: https://github.com/Automattic/socket.io-client.git
Source0: http://registry.npmjs.org/socket.io-client/-/socket.io-client-2.1.1.tgz
Source1: http://registry.npmjs.org/base64-arraybuffer/-/base64-arraybuffer-0.1.5.tgz
Source2: http://registry.npmjs.org/component-bind/-/component-bind-1.0.0.tgz
Source3: http://registry.npmjs.org/component-emitter/-/component-emitter-1.2.1.tgz
Source4: http://registry.npmjs.org/backo2/-/backo2-1.0.2.tgz
Source5: http://registry.npmjs.org/has-cors/-/has-cors-1.1.0.tgz
Source6: http://registry.npmjs.org/has-binary2/-/has-binary2-1.0.3.tgz
Source7: http://registry.npmjs.org/engine.io-client/-/engine.io-client-3.2.1.tgz
Source8: http://registry.npmjs.org/debug/-/debug-3.1.0.tgz
Source9: http://registry.npmjs.org/indexof/-/indexof-0.0.1.tgz
Source10: http://registry.npmjs.org/parseqs/-/parseqs-0.0.5.tgz
Source11: http://registry.npmjs.org/parseuri/-/parseuri-0.0.5.tgz
Source12: http://registry.npmjs.org/object-component/-/object-component-0.0.3.tgz
Source13: http://registry.npmjs.org/to-array/-/to-array-0.1.4.tgz
Source14: http://registry.npmjs.org/socket.io-parser/-/socket.io-parser-3.2.0.tgz
Source15: http://registry.npmjs.org/isarray/-/isarray-2.0.1.tgz
Source16: http://registry.npmjs.org/engine.io-parser/-/engine.io-parser-2.1.3.tgz
Source17: http://registry.npmjs.org/component-inherit/-/component-inherit-0.0.3.tgz
Source18: http://registry.npmjs.org/ws/-/ws-3.3.3.tgz
Source19: http://registry.npmjs.org/yeast/-/yeast-0.1.2.tgz
Source20: http://registry.npmjs.org/ms/-/ms-2.0.0.tgz
Source21: http://registry.npmjs.org/xmlhttprequest-ssl/-/xmlhttprequest-ssl-1.5.5.tgz
Source22: http://registry.npmjs.org/better-assert/-/better-assert-1.0.2.tgz
Source23: http://registry.npmjs.org/after/-/after-0.8.2.tgz
Source24: http://registry.npmjs.org/arraybuffer.slice/-/arraybuffer.slice-0.0.7.tgz
Source25: http://registry.npmjs.org/blob/-/blob-0.0.5.tgz
Source26: http://registry.npmjs.org/async-limiter/-/async-limiter-1.0.0.tgz
Source27: http://registry.npmjs.org/safe-buffer/-/safe-buffer-5.1.2.tgz
Source28: http://registry.npmjs.org/ultron/-/ultron-1.1.1.tgz
Source29: http://registry.npmjs.org/callsite/-/callsite-1.0.0.tgz
Source30: socket.io-client-2.1.1-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(socket.io-client) = 2.1.1
Provides: bundled-npm(base64-arraybuffer) = 0.1.5
Provides: bundled-npm(component-bind) = 1.0.0
Provides: bundled-npm(component-emitter) = 1.2.1
Provides: bundled-npm(backo2) = 1.0.2
Provides: bundled-npm(has-cors) = 1.1.0
Provides: bundled-npm(has-binary2) = 1.0.3
Provides: bundled-npm(engine.io-client) = 3.2.1
Provides: bundled-npm(debug) = 3.1.0
Provides: bundled-npm(indexof) = 0.0.1
Provides: bundled-npm(parseqs) = 0.0.5
Provides: bundled-npm(parseuri) = 0.0.5
Provides: bundled-npm(object-component) = 0.0.3
Provides: bundled-npm(to-array) = 0.1.4
Provides: bundled-npm(socket.io-parser) = 3.2.0
Provides: bundled-npm(isarray) = 2.0.1
Provides: bundled-npm(engine.io-parser) = 2.1.3
Provides: bundled-npm(component-inherit) = 0.0.3
Provides: bundled-npm(ws) = 3.3.3
Provides: bundled-npm(yeast) = 0.1.2
Provides: bundled-npm(ms) = 2.0.0
Provides: bundled-npm(xmlhttprequest-ssl) = 1.5.5
Provides: bundled-npm(better-assert) = 1.0.2
Provides: bundled-npm(after) = 0.8.2
Provides: bundled-npm(arraybuffer.slice) = 0.0.7
Provides: bundled-npm(blob) = 0.0.5
Provides: bundled-npm(async-limiter) = 1.0.0
Provides: bundled-npm(safe-buffer) = 5.1.2
Provides: bundled-npm(ultron) = 1.1.1
Provides: bundled-npm(callsite) = 1.0.0
AutoReq: no 
AutoProv: no 


%define npm_cache_dir /tmp/npm_cache_%{name}-%{version}-%{release}

%description
%{summary}

%prep
mkdir -p %{npm_cache_dir}
for tgz in %{sources}; do
  echo $tgz | grep -q registry.npmjs.org || npm cache add --cache ./%{npm_cache_dir} $tgz
done

%setup -T -q -a 30 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
pwd
cd /tmp/node_modules/%{npm_name}
cp -pfr LICENSE README.md dist lib package.json node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf README.md LICENSE ../../
# If any binaries are included, symlink them to bindir here


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}


%changelog
* Tue Nov 27 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 2.1.1-1
- First release 
