%global npm_name request
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 2.81.0
Release: 1
Summary: Simplified HTTP request client
License: Apache-2.0
URL: http://github.com/request/request/issues
Source0: http://registry.npmjs.org/request/-/request-2.81.0.tgz
Source1: http://registry.npmjs.org/caseless/-/caseless-0.12.0.tgz
Source2: http://registry.npmjs.org/aws-sign2/-/aws-sign2-0.6.0.tgz
Source3: http://registry.npmjs.org/combined-stream/-/combined-stream-1.0.5.tgz
Source4: http://registry.npmjs.org/aws4/-/aws4-1.6.0.tgz
Source5: http://registry.npmjs.org/form-data/-/form-data-2.1.4.tgz
Source6: http://registry.npmjs.org/har-validator/-/har-validator-4.2.1.tgz
Source7: http://registry.npmjs.org/forever-agent/-/forever-agent-0.6.1.tgz
Source8: http://registry.npmjs.org/extend/-/extend-3.0.0.tgz
Source9: http://registry.npmjs.org/hawk/-/hawk-3.1.3.tgz
Source10: http://registry.npmjs.org/http-signature/-/http-signature-1.1.1.tgz
Source11: http://registry.npmjs.org/is-typedarray/-/is-typedarray-1.0.0.tgz
Source12: http://registry.npmjs.org/isstream/-/isstream-0.1.2.tgz
Source13: http://registry.npmjs.org/json-stringify-safe/-/json-stringify-safe-5.0.1.tgz
Source14: http://registry.npmjs.org/performance-now/-/performance-now-0.2.0.tgz
Source15: http://registry.npmjs.org/oauth-sign/-/oauth-sign-0.8.2.tgz
Source16: http://registry.npmjs.org/mime-types/-/mime-types-2.1.15.tgz
Source17: http://registry.npmjs.org/qs/-/qs-6.4.0.tgz
Source18: http://registry.npmjs.org/safe-buffer/-/safe-buffer-5.0.1.tgz
Source19: http://registry.npmjs.org/stringstream/-/stringstream-0.0.5.tgz
Source20: http://registry.npmjs.org/tough-cookie/-/tough-cookie-2.3.2.tgz
Source21: http://registry.npmjs.org/tunnel-agent/-/tunnel-agent-0.6.0.tgz
Source22: http://registry.npmjs.org/uuid/-/uuid-3.0.1.tgz
Source23: http://registry.npmjs.org/delayed-stream/-/delayed-stream-1.0.0.tgz
Source24: http://registry.npmjs.org/asynckit/-/asynckit-0.4.0.tgz
Source25: http://registry.npmjs.org/har-schema/-/har-schema-1.0.5.tgz
Source26: http://registry.npmjs.org/ajv/-/ajv-4.11.7.tgz
Source27: http://registry.npmjs.org/hoek/-/hoek-2.16.3.tgz
Source28: http://registry.npmjs.org/sntp/-/sntp-1.0.9.tgz
Source29: http://registry.npmjs.org/boom/-/boom-2.10.1.tgz
Source30: http://registry.npmjs.org/cryptiles/-/cryptiles-2.0.5.tgz
Source31: http://registry.npmjs.org/assert-plus/-/assert-plus-0.2.0.tgz
Source32: http://registry.npmjs.org/jsprim/-/jsprim-1.4.0.tgz
Source33: http://registry.npmjs.org/sshpk/-/sshpk-1.13.0.tgz
Source34: http://registry.npmjs.org/mime-db/-/mime-db-1.27.0.tgz
Source35: http://registry.npmjs.org/punycode/-/punycode-1.4.1.tgz
Source36: http://registry.npmjs.org/co/-/co-4.6.0.tgz
Source37: http://registry.npmjs.org/json-stable-stringify/-/json-stable-stringify-1.0.1.tgz
Source38: http://registry.npmjs.org/assert-plus/-/assert-plus-1.0.0.tgz
Source39: http://registry.npmjs.org/json-schema/-/json-schema-0.2.3.tgz
Source40: http://registry.npmjs.org/extsprintf/-/extsprintf-1.0.2.tgz
Source41: http://registry.npmjs.org/asn1/-/asn1-0.2.3.tgz
Source42: http://registry.npmjs.org/verror/-/verror-1.3.6.tgz
Source43: http://registry.npmjs.org/getpass/-/getpass-0.1.7.tgz
Source44: http://registry.npmjs.org/dashdash/-/dashdash-1.14.1.tgz
Source45: http://registry.npmjs.org/jsbn/-/jsbn-0.1.1.tgz
Source46: http://registry.npmjs.org/tweetnacl/-/tweetnacl-0.14.5.tgz
Source47: http://registry.npmjs.org/jodid25519/-/jodid25519-1.0.2.tgz
Source48: http://registry.npmjs.org/ecc-jsbn/-/ecc-jsbn-0.1.1.tgz
Source49: http://registry.npmjs.org/bcrypt-pbkdf/-/bcrypt-pbkdf-1.0.1.tgz
Source50: http://registry.npmjs.org/jsonify/-/jsonify-0.0.0.tgz
Source51: request-2.81.0-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(request) = 2.81.0
Provides: bundled-npm(caseless) = 0.12.0
Provides: bundled-npm(aws-sign2) = 0.6.0
Provides: bundled-npm(combined-stream) = 1.0.5
Provides: bundled-npm(aws4) = 1.6.0
Provides: bundled-npm(form-data) = 2.1.4
Provides: bundled-npm(har-validator) = 4.2.1
Provides: bundled-npm(forever-agent) = 0.6.1
Provides: bundled-npm(extend) = 3.0.0
Provides: bundled-npm(hawk) = 3.1.3
Provides: bundled-npm(http-signature) = 1.1.1
Provides: bundled-npm(is-typedarray) = 1.0.0
Provides: bundled-npm(isstream) = 0.1.2
Provides: bundled-npm(json-stringify-safe) = 5.0.1
Provides: bundled-npm(performance-now) = 0.2.0
Provides: bundled-npm(oauth-sign) = 0.8.2
Provides: bundled-npm(mime-types) = 2.1.15
Provides: bundled-npm(qs) = 6.4.0
Provides: bundled-npm(safe-buffer) = 5.0.1
Provides: bundled-npm(stringstream) = 0.0.5
Provides: bundled-npm(tough-cookie) = 2.3.2
Provides: bundled-npm(tunnel-agent) = 0.6.0
Provides: bundled-npm(uuid) = 3.0.1
Provides: bundled-npm(delayed-stream) = 1.0.0
Provides: bundled-npm(asynckit) = 0.4.0
Provides: bundled-npm(har-schema) = 1.0.5
Provides: bundled-npm(ajv) = 4.11.7
Provides: bundled-npm(hoek) = 2.16.3
Provides: bundled-npm(sntp) = 1.0.9
Provides: bundled-npm(boom) = 2.10.1
Provides: bundled-npm(cryptiles) = 2.0.5
Provides: bundled-npm(assert-plus) = 0.2.0
Provides: bundled-npm(jsprim) = 1.4.0
Provides: bundled-npm(sshpk) = 1.13.0
Provides: bundled-npm(mime-db) = 1.27.0
Provides: bundled-npm(punycode) = 1.4.1
Provides: bundled-npm(co) = 4.6.0
Provides: bundled-npm(json-stable-stringify) = 1.0.1
Provides: bundled-npm(assert-plus) = 1.0.0
Provides: bundled-npm(json-schema) = 0.2.3
Provides: bundled-npm(extsprintf) = 1.0.2
Provides: bundled-npm(asn1) = 0.2.3
Provides: bundled-npm(verror) = 1.3.6
Provides: bundled-npm(getpass) = 0.1.7
Provides: bundled-npm(dashdash) = 1.14.1
Provides: bundled-npm(jsbn) = 0.1.1
Provides: bundled-npm(tweetnacl) = 0.14.5
Provides: bundled-npm(jodid25519) = 1.0.2
Provides: bundled-npm(ecc-jsbn) = 0.1.1
Provides: bundled-npm(bcrypt-pbkdf) = 1.0.1
Provides: bundled-npm(jsonify) = 0.0.0
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

%setup -T -q -a 51 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd node_modules/request
cp -pfr CHANGELOG.md LICENSE README.md index.js lib package.json request.js node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf CHANGELOG.md README.md LICENSE ../../
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
%doc CHANGELOG.md
%doc README.md

%changelog
* Thu Apr 27 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 2.81.0-1
- First release 
