%global npm_name express
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 4.15.2
Release: 1
Summary: Fast, unopinionated, minimalist web framework
License: MIT
URL: http://expressjs.com/
Source0: http://registry.npmjs.org/express/-/express-4.15.2.tgz
Source1: http://registry.npmjs.org/array-flatten/-/array-flatten-1.1.1.tgz
Source2: http://registry.npmjs.org/accepts/-/accepts-1.3.3.tgz
Source3: http://registry.npmjs.org/content-disposition/-/content-disposition-0.5.2.tgz
Source4: http://registry.npmjs.org/content-type/-/content-type-1.0.2.tgz
Source5: http://registry.npmjs.org/debug/-/debug-2.6.1.tgz
Source6: http://registry.npmjs.org/depd/-/depd-1.1.0.tgz
Source7: http://registry.npmjs.org/cookie-signature/-/cookie-signature-1.0.6.tgz
Source8: http://registry.npmjs.org/cookie/-/cookie-0.3.1.tgz
Source9: http://registry.npmjs.org/etag/-/etag-1.8.0.tgz
Source10: http://registry.npmjs.org/encodeurl/-/encodeurl-1.0.1.tgz
Source11: http://registry.npmjs.org/escape-html/-/escape-html-1.0.3.tgz
Source12: http://registry.npmjs.org/fresh/-/fresh-0.5.0.tgz
Source13: http://registry.npmjs.org/finalhandler/-/finalhandler-1.0.2.tgz
Source14: http://registry.npmjs.org/merge-descriptors/-/merge-descriptors-1.0.1.tgz
Source15: http://registry.npmjs.org/on-finished/-/on-finished-2.3.0.tgz
Source16: http://registry.npmjs.org/parseurl/-/parseurl-1.3.1.tgz
Source17: http://registry.npmjs.org/methods/-/methods-1.1.2.tgz
Source18: http://registry.npmjs.org/proxy-addr/-/proxy-addr-1.1.4.tgz
Source19: http://registry.npmjs.org/qs/-/qs-6.4.0.tgz
Source20: http://registry.npmjs.org/path-to-regexp/-/path-to-regexp-0.1.7.tgz
Source21: http://registry.npmjs.org/range-parser/-/range-parser-1.2.0.tgz
Source22: http://registry.npmjs.org/serve-static/-/serve-static-1.12.1.tgz
Source23: http://registry.npmjs.org/setprototypeof/-/setprototypeof-1.0.3.tgz
Source24: http://registry.npmjs.org/statuses/-/statuses-1.3.1.tgz
Source25: http://registry.npmjs.org/send/-/send-0.15.1.tgz
Source26: http://registry.npmjs.org/utils-merge/-/utils-merge-1.0.0.tgz
Source27: http://registry.npmjs.org/type-is/-/type-is-1.6.15.tgz
Source28: http://registry.npmjs.org/vary/-/vary-1.1.1.tgz
Source29: http://registry.npmjs.org/mime-types/-/mime-types-2.1.15.tgz
Source30: http://registry.npmjs.org/negotiator/-/negotiator-0.6.1.tgz
Source31: http://registry.npmjs.org/debug/-/debug-2.6.4.tgz
Source32: http://registry.npmjs.org/ms/-/ms-0.7.2.tgz
Source33: http://registry.npmjs.org/unpipe/-/unpipe-1.0.0.tgz
Source34: http://registry.npmjs.org/ee-first/-/ee-first-1.1.1.tgz
Source35: http://registry.npmjs.org/forwarded/-/forwarded-0.1.0.tgz
Source36: http://registry.npmjs.org/ipaddr.js/-/ipaddr.js-1.3.0.tgz
Source37: http://registry.npmjs.org/destroy/-/destroy-1.0.4.tgz
Source38: http://registry.npmjs.org/http-errors/-/http-errors-1.6.1.tgz
Source39: http://registry.npmjs.org/mime/-/mime-1.3.4.tgz
Source40: http://registry.npmjs.org/media-typer/-/media-typer-0.3.0.tgz
Source41: http://registry.npmjs.org/mime-db/-/mime-db-1.27.0.tgz
Source42: http://registry.npmjs.org/ms/-/ms-0.7.3.tgz
Source43: http://registry.npmjs.org/inherits/-/inherits-2.0.3.tgz
Source44: express-4.15.2-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(express) = 4.15.2
Provides: bundled-npm(array-flatten) = 1.1.1
Provides: bundled-npm(accepts) = 1.3.3
Provides: bundled-npm(content-disposition) = 0.5.2
Provides: bundled-npm(content-type) = 1.0.2
Provides: bundled-npm(debug) = 2.6.1
Provides: bundled-npm(depd) = 1.1.0
Provides: bundled-npm(cookie-signature) = 1.0.6
Provides: bundled-npm(cookie) = 0.3.1
Provides: bundled-npm(etag) = 1.8.0
Provides: bundled-npm(encodeurl) = 1.0.1
Provides: bundled-npm(escape-html) = 1.0.3
Provides: bundled-npm(fresh) = 0.5.0
Provides: bundled-npm(finalhandler) = 1.0.2
Provides: bundled-npm(merge-descriptors) = 1.0.1
Provides: bundled-npm(on-finished) = 2.3.0
Provides: bundled-npm(parseurl) = 1.3.1
Provides: bundled-npm(methods) = 1.1.2
Provides: bundled-npm(proxy-addr) = 1.1.4
Provides: bundled-npm(qs) = 6.4.0
Provides: bundled-npm(path-to-regexp) = 0.1.7
Provides: bundled-npm(range-parser) = 1.2.0
Provides: bundled-npm(serve-static) = 1.12.1
Provides: bundled-npm(setprototypeof) = 1.0.3
Provides: bundled-npm(statuses) = 1.3.1
Provides: bundled-npm(send) = 0.15.1
Provides: bundled-npm(utils-merge) = 1.0.0
Provides: bundled-npm(type-is) = 1.6.15
Provides: bundled-npm(vary) = 1.1.1
Provides: bundled-npm(mime-types) = 2.1.15
Provides: bundled-npm(negotiator) = 0.6.1
Provides: bundled-npm(debug) = 2.6.4
Provides: bundled-npm(ms) = 0.7.2
Provides: bundled-npm(unpipe) = 1.0.0
Provides: bundled-npm(ee-first) = 1.1.1
Provides: bundled-npm(forwarded) = 0.1.0
Provides: bundled-npm(ipaddr.js) = 1.3.0
Provides: bundled-npm(destroy) = 1.0.4
Provides: bundled-npm(http-errors) = 1.6.1
Provides: bundled-npm(mime) = 1.3.4
Provides: bundled-npm(media-typer) = 0.3.0
Provides: bundled-npm(mime-db) = 1.27.0
Provides: bundled-npm(ms) = 0.7.3
Provides: bundled-npm(inherits) = 2.0.3
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

%setup -T -q -a 44 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd node_modules/express
cp -pfr History.md LICENSE Readme.md index.js lib package.json node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
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
* Thu Apr 27 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 4.15.2-1
- First release 
