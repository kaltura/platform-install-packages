%global npm_name socket.io
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 1.3.5
Release: 1
Summary: node
License: FIXME
URL: git://github.com/Automattic/socket.io
Source0: http://registry.npmjs.org/socket.io/-/socket.io-1.3.5.tgz
Source1: http://registry.npmjs.org/socket.io-adapter/-/socket.io-adapter-0.3.1.tgz
Source2: http://registry.npmjs.org/socket.io-parser/-/socket.io-parser-2.2.4.tgz
Source3: http://registry.npmjs.org/engine.io/-/engine.io-1.5.1.tgz
Source4: http://registry.npmjs.org/socket.io-client/-/socket.io-client-1.3.5.tgz
Source5: http://registry.npmjs.org/debug/-/debug-2.1.0.tgz
Source6: http://registry.npmjs.org/has-binary-data/-/has-binary-data-0.1.3.tgz
Source7: http://registry.npmjs.org/socket.io-parser/-/socket.io-parser-2.2.2.tgz
Source8: http://registry.npmjs.org/debug/-/debug-1.0.2.tgz
Source9: http://registry.npmjs.org/debug/-/debug-0.7.4.tgz
Source10: http://registry.npmjs.org/object-keys/-/object-keys-1.0.1.tgz
Source11: http://registry.npmjs.org/json3/-/json3-3.2.6.tgz
Source12: http://registry.npmjs.org/component-emitter/-/component-emitter-1.1.2.tgz
Source13: http://registry.npmjs.org/isarray/-/isarray-0.0.1.tgz
Source14: http://registry.npmjs.org/debug/-/debug-1.0.3.tgz
Source15: http://registry.npmjs.org/benchmark/-/benchmark-1.0.0.tgz
Source16: http://registry.npmjs.org/ws/-/ws-0.5.0.tgz
Source17: http://registry.npmjs.org/engine.io-parser/-/engine.io-parser-1.2.1.tgz
Source18: http://registry.npmjs.org/base64id/-/base64id-0.1.0.tgz
Source19: http://registry.npmjs.org/engine.io-client/-/engine.io-client-1.5.1.tgz
Source20: http://registry.npmjs.org/component-bind/-/component-bind-1.0.0.tgz
Source21: http://registry.npmjs.org/object-component/-/object-component-0.0.3.tgz
Source22: http://registry.npmjs.org/has-binary/-/has-binary-0.1.6.tgz
Source23: http://registry.npmjs.org/indexof/-/indexof-0.0.1.tgz
Source24: http://registry.npmjs.org/parseuri/-/parseuri-0.0.2.tgz
Source25: http://registry.npmjs.org/to-array/-/to-array-0.1.3.tgz
Source26: http://registry.npmjs.org/backo2/-/backo2-1.0.2.tgz
Source27: http://registry.npmjs.org/ms/-/ms-0.6.2.tgz
Source28: http://registry.npmjs.org/nan/-/nan-1.4.3.tgz
Source29: http://registry.npmjs.org/options/-/options-0.0.6.tgz
Source30: http://registry.npmjs.org/after/-/after-0.8.1.tgz
Source31: http://registry.npmjs.org/ultron/-/ultron-1.0.2.tgz
Source32: http://registry.npmjs.org/base64-arraybuffer/-/base64-arraybuffer-0.1.2.tgz
Source33: http://registry.npmjs.org/arraybuffer.slice/-/arraybuffer.slice-0.0.6.tgz
Source34: http://registry.npmjs.org/has-binary/-/has-binary-0.1.5.tgz
Source35: http://registry.npmjs.org/has-cors/-/has-cors-1.0.3.tgz
Source36: http://registry.npmjs.org/utf8/-/utf8-2.0.0.tgz
Source37: http://registry.npmjs.org/blob/-/blob-0.0.2.tgz
Source38: http://registry.npmjs.org/ws/-/ws-0.4.31.tgz
Source39: http://registry.npmjs.org/debug/-/debug-1.0.4.tgz
Source40: http://registry.npmjs.org/parseuri/-/parseuri-0.0.4.tgz
Source41: http://registry.npmjs.org/parsejson/-/parsejson-0.0.1.tgz
Source42: http://registry.npmjs.org/parseqs/-/parseqs-0.0.2.tgz
Source43: http://registry.npmjs.org/component-inherit/-/component-inherit-0.0.3.tgz
Source44: http://registry.npmjs.org/better-assert/-/better-assert-1.0.2.tgz
Source45: http://registry.npmjs.org/commander/-/commander-0.6.1.tgz
Source46: http://registry.npmjs.org/nan/-/nan-0.3.2.tgz
Source47: http://registry.npmjs.org/tinycolor/-/tinycolor-0.0.1.tgz
Source48: http://registry.npmjs.org/callsite/-/callsite-1.0.0.tgz
Source49: socket.io-1.3.5-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(socket.io) = 1.3.5
Provides: bundled-npm(socket.io-adapter) = 0.3.1
Provides: bundled-npm(socket.io-parser) = 2.2.4
Provides: bundled-npm(engine.io) = 1.5.1
Provides: bundled-npm(socket.io-client) = 1.3.5
Provides: bundled-npm(debug) = 2.1.0
Provides: bundled-npm(has-binary-data) = 0.1.3
Provides: bundled-npm(socket.io-parser) = 2.2.2
Provides: bundled-npm(debug) = 1.0.2
Provides: bundled-npm(debug) = 0.7.4
Provides: bundled-npm(object-keys) = 1.0.1
Provides: bundled-npm(json3) = 3.2.6
Provides: bundled-npm(component-emitter) = 1.1.2
Provides: bundled-npm(isarray) = 0.0.1
Provides: bundled-npm(debug) = 1.0.3
Provides: bundled-npm(benchmark) = 1.0.0
Provides: bundled-npm(ws) = 0.5.0
Provides: bundled-npm(engine.io-parser) = 1.2.1
Provides: bundled-npm(base64id) = 0.1.0
Provides: bundled-npm(engine.io-client) = 1.5.1
Provides: bundled-npm(component-bind) = 1.0.0
Provides: bundled-npm(object-component) = 0.0.3
Provides: bundled-npm(has-binary) = 0.1.6
Provides: bundled-npm(indexof) = 0.0.1
Provides: bundled-npm(parseuri) = 0.0.2
Provides: bundled-npm(to-array) = 0.1.3
Provides: bundled-npm(backo2) = 1.0.2
Provides: bundled-npm(ms) = 0.6.2
Provides: bundled-npm(nan) = 1.4.3
Provides: bundled-npm(options) = 0.0.6
Provides: bundled-npm(after) = 0.8.1
Provides: bundled-npm(ultron) = 1.0.2
Provides: bundled-npm(base64-arraybuffer) = 0.1.2
Provides: bundled-npm(arraybuffer.slice) = 0.0.6
Provides: bundled-npm(has-binary) = 0.1.5
Provides: bundled-npm(has-cors) = 1.0.3
Provides: bundled-npm(utf8) = 2.0.0
Provides: bundled-npm(blob) = 0.0.2
Provides: bundled-npm(ws) = 0.4.31
Provides: bundled-npm(debug) = 1.0.4
Provides: bundled-npm(parseuri) = 0.0.4
Provides: bundled-npm(parsejson) = 0.0.1
Provides: bundled-npm(parseqs) = 0.0.2
Provides: bundled-npm(component-inherit) = 0.0.3
Provides: bundled-npm(better-assert) = 1.0.2
Provides: bundled-npm(commander) = 0.6.1
Provides: bundled-npm(nan) = 0.3.2
Provides: bundled-npm(tinycolor) = 0.0.1
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

%setup -T -q -a 49 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd node_modules/socket.io
cp -pfr .npmignore .travis.yml History.md LICENSE Makefile Readme.md index.js lib package.json node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf History.md Readme.md LICENSE ../../
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
%doc History.md
%doc Readme.md

%changelog
* Tue Jul 11 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 1.3.5-1
- First release 
