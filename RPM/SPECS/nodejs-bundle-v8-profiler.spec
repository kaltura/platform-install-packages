%global npm_name v8-profiler
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 5.7.0
Release: 1
Summary: node bindings for the v8 profiler
License: BSD-2-Clause
URL: http://github.com/node-inspector/v8-profiler
Source0: http://registry.npmjs.org/v8-profiler/-/v8-profiler-5.7.0.tgz
Source1: http://registry.npmjs.org/node-pre-gyp/-/node-pre-gyp-0.6.39.tgz
Source2: http://registry.npmjs.org/nan/-/nan-2.7.0.tgz
Source3: http://registry.npmjs.org/nopt/-/nopt-4.0.1.tgz
Source4: http://registry.npmjs.org/mkdirp/-/mkdirp-0.5.1.tgz
Source5: http://registry.npmjs.org/npmlog/-/npmlog-4.1.2.tgz
Source6: http://registry.npmjs.org/rc/-/rc-1.2.2.tgz
Source7: http://registry.npmjs.org/request/-/request-2.81.0.tgz
Source8: http://registry.npmjs.org/rimraf/-/rimraf-2.6.2.tgz
Source9: http://registry.npmjs.org/hawk/-/hawk-3.1.3.tgz
Source10: http://registry.npmjs.org/semver/-/semver-5.4.1.tgz
Source11: http://registry.npmjs.org/tar/-/tar-2.2.1.tgz
Source12: http://registry.npmjs.org/tar-pack/-/tar-pack-3.4.1.tgz
Source13: http://registry.npmjs.org/detect-libc/-/detect-libc-1.0.2.tgz
Source14: http://registry.npmjs.org/abbrev/-/abbrev-1.1.1.tgz
Source15: http://registry.npmjs.org/osenv/-/osenv-0.1.4.tgz
Source16: http://registry.npmjs.org/minimist/-/minimist-0.0.8.tgz
Source17: http://registry.npmjs.org/are-we-there-yet/-/are-we-there-yet-1.1.4.tgz
Source18: http://registry.npmjs.org/console-control-strings/-/console-control-strings-1.1.0.tgz
Source19: http://registry.npmjs.org/set-blocking/-/set-blocking-2.0.0.tgz
Source20: http://registry.npmjs.org/gauge/-/gauge-2.7.4.tgz
Source21: http://registry.npmjs.org/deep-extend/-/deep-extend-0.4.2.tgz
Source22: http://registry.npmjs.org/ini/-/ini-1.3.4.tgz
Source23: http://registry.npmjs.org/minimist/-/minimist-1.2.0.tgz
Source24: http://registry.npmjs.org/strip-json-comments/-/strip-json-comments-2.0.1.tgz
Source25: http://registry.npmjs.org/aws-sign2/-/aws-sign2-0.6.0.tgz
Source26: http://registry.npmjs.org/aws4/-/aws4-1.6.0.tgz
Source27: http://registry.npmjs.org/caseless/-/caseless-0.12.0.tgz
Source28: http://registry.npmjs.org/extend/-/extend-3.0.1.tgz
Source29: http://registry.npmjs.org/combined-stream/-/combined-stream-1.0.5.tgz
Source30: http://registry.npmjs.org/forever-agent/-/forever-agent-0.6.1.tgz
Source31: http://registry.npmjs.org/har-validator/-/har-validator-4.2.1.tgz
Source32: http://registry.npmjs.org/form-data/-/form-data-2.1.4.tgz
Source33: http://registry.npmjs.org/http-signature/-/http-signature-1.1.1.tgz
Source34: http://registry.npmjs.org/json-stringify-safe/-/json-stringify-safe-5.0.1.tgz
Source35: http://registry.npmjs.org/isstream/-/isstream-0.1.2.tgz
Source36: http://registry.npmjs.org/is-typedarray/-/is-typedarray-1.0.0.tgz
Source37: http://registry.npmjs.org/mime-types/-/mime-types-2.1.17.tgz
Source38: http://registry.npmjs.org/oauth-sign/-/oauth-sign-0.8.2.tgz
Source39: http://registry.npmjs.org/performance-now/-/performance-now-0.2.0.tgz
Source40: http://registry.npmjs.org/qs/-/qs-6.4.0.tgz
Source41: http://registry.npmjs.org/safe-buffer/-/safe-buffer-5.1.1.tgz
Source42: http://registry.npmjs.org/stringstream/-/stringstream-0.0.5.tgz
Source43: http://registry.npmjs.org/tunnel-agent/-/tunnel-agent-0.6.0.tgz
Source44: http://registry.npmjs.org/tough-cookie/-/tough-cookie-2.3.3.tgz
Source45: http://registry.npmjs.org/uuid/-/uuid-3.1.0.tgz
Source46: http://registry.npmjs.org/boom/-/boom-2.10.1.tgz
Source47: http://registry.npmjs.org/hoek/-/hoek-2.16.3.tgz
Source48: http://registry.npmjs.org/glob/-/glob-7.1.2.tgz
Source49: http://registry.npmjs.org/cryptiles/-/cryptiles-2.0.5.tgz
Source50: http://registry.npmjs.org/sntp/-/sntp-1.0.9.tgz
Source51: http://registry.npmjs.org/block-stream/-/block-stream-0.0.9.tgz
Source52: http://registry.npmjs.org/fstream/-/fstream-1.0.11.tgz
Source53: http://registry.npmjs.org/inherits/-/inherits-2.0.3.tgz
Source54: http://registry.npmjs.org/debug/-/debug-2.6.9.tgz
Source55: http://registry.npmjs.org/fstream-ignore/-/fstream-ignore-1.0.5.tgz
Source56: http://registry.npmjs.org/once/-/once-1.4.0.tgz
Source57: http://registry.npmjs.org/delegates/-/delegates-1.0.0.tgz
Source58: http://registry.npmjs.org/readable-stream/-/readable-stream-2.3.3.tgz
Source59: http://registry.npmjs.org/uid-number/-/uid-number-0.0.6.tgz
Source60: http://registry.npmjs.org/os-homedir/-/os-homedir-1.0.2.tgz
Source61: http://registry.npmjs.org/os-tmpdir/-/os-tmpdir-1.0.2.tgz
Source62: http://registry.npmjs.org/aproba/-/aproba-1.2.0.tgz
Source63: http://registry.npmjs.org/has-unicode/-/has-unicode-2.0.1.tgz
Source64: http://registry.npmjs.org/object-assign/-/object-assign-4.1.1.tgz
Source65: http://registry.npmjs.org/signal-exit/-/signal-exit-3.0.2.tgz
Source66: http://registry.npmjs.org/string-width/-/string-width-1.0.2.tgz
Source67: http://registry.npmjs.org/strip-ansi/-/strip-ansi-3.0.1.tgz
Source68: http://registry.npmjs.org/wide-align/-/wide-align-1.1.2.tgz
Source69: http://registry.npmjs.org/delayed-stream/-/delayed-stream-1.0.0.tgz
Source70: http://registry.npmjs.org/ajv/-/ajv-4.11.8.tgz
Source71: http://registry.npmjs.org/asynckit/-/asynckit-0.4.0.tgz
Source72: http://registry.npmjs.org/har-schema/-/har-schema-1.0.5.tgz
Source73: http://registry.npmjs.org/assert-plus/-/assert-plus-0.2.0.tgz
Source74: http://registry.npmjs.org/jsprim/-/jsprim-1.4.1.tgz
Source75: http://registry.npmjs.org/sshpk/-/sshpk-1.13.1.tgz
Source76: http://registry.npmjs.org/mime-db/-/mime-db-1.30.0.tgz
Source77: http://registry.npmjs.org/punycode/-/punycode-1.4.1.tgz
Source78: http://registry.npmjs.org/fs.realpath/-/fs.realpath-1.0.0.tgz
Source79: http://registry.npmjs.org/inflight/-/inflight-1.0.6.tgz
Source80: http://registry.npmjs.org/minimatch/-/minimatch-3.0.4.tgz
Source81: http://registry.npmjs.org/path-is-absolute/-/path-is-absolute-1.0.1.tgz
Source82: http://registry.npmjs.org/graceful-fs/-/graceful-fs-4.1.11.tgz
Source83: http://registry.npmjs.org/ms/-/ms-2.0.0.tgz
Source84: http://registry.npmjs.org/wrappy/-/wrappy-1.0.2.tgz
Source85: http://registry.npmjs.org/core-util-is/-/core-util-is-1.0.2.tgz
Source86: http://registry.npmjs.org/isarray/-/isarray-1.0.0.tgz
Source87: http://registry.npmjs.org/process-nextick-args/-/process-nextick-args-1.0.7.tgz
Source88: http://registry.npmjs.org/string_decoder/-/string_decoder-1.0.3.tgz
Source89: http://registry.npmjs.org/util-deprecate/-/util-deprecate-1.0.2.tgz
Source90: http://registry.npmjs.org/code-point-at/-/code-point-at-1.1.0.tgz
Source91: http://registry.npmjs.org/is-fullwidth-code-point/-/is-fullwidth-code-point-1.0.0.tgz
Source92: http://registry.npmjs.org/ansi-regex/-/ansi-regex-2.1.1.tgz
Source93: http://registry.npmjs.org/json-stable-stringify/-/json-stable-stringify-1.0.1.tgz
Source94: http://registry.npmjs.org/co/-/co-4.6.0.tgz
Source95: http://registry.npmjs.org/assert-plus/-/assert-plus-1.0.0.tgz
Source96: http://registry.npmjs.org/verror/-/verror-1.10.0.tgz
Source97: http://registry.npmjs.org/extsprintf/-/extsprintf-1.3.0.tgz
Source98: http://registry.npmjs.org/json-schema/-/json-schema-0.2.3.tgz
Source99: http://registry.npmjs.org/asn1/-/asn1-0.2.3.tgz
Source100: http://registry.npmjs.org/dashdash/-/dashdash-1.14.1.tgz
Source101: http://registry.npmjs.org/getpass/-/getpass-0.1.7.tgz
Source102: http://registry.npmjs.org/jsbn/-/jsbn-0.1.1.tgz
Source103: http://registry.npmjs.org/ecc-jsbn/-/ecc-jsbn-0.1.1.tgz
Source104: http://registry.npmjs.org/tweetnacl/-/tweetnacl-0.14.5.tgz
Source105: http://registry.npmjs.org/bcrypt-pbkdf/-/bcrypt-pbkdf-1.0.1.tgz
Source106: http://registry.npmjs.org/brace-expansion/-/brace-expansion-1.1.8.tgz
Source107: http://registry.npmjs.org/number-is-nan/-/number-is-nan-1.0.1.tgz
Source108: http://registry.npmjs.org/jsonify/-/jsonify-0.0.0.tgz
Source109: http://registry.npmjs.org/balanced-match/-/balanced-match-1.0.0.tgz
Source110: http://registry.npmjs.org/concat-map/-/concat-map-0.0.1.tgz
Source111: v8-profiler-5.7.0-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(v8-profiler) = 5.7.0
Provides: bundled-npm(node-pre-gyp) = 0.6.39
Provides: bundled-npm(nan) = 2.7.0
Provides: bundled-npm(nopt) = 4.0.1
Provides: bundled-npm(mkdirp) = 0.5.1
Provides: bundled-npm(npmlog) = 4.1.2
Provides: bundled-npm(rc) = 1.2.2
Provides: bundled-npm(request) = 2.81.0
Provides: bundled-npm(rimraf) = 2.6.2
Provides: bundled-npm(hawk) = 3.1.3
Provides: bundled-npm(semver) = 5.4.1
Provides: bundled-npm(tar) = 2.2.1
Provides: bundled-npm(tar-pack) = 3.4.1
Provides: bundled-npm(detect-libc) = 1.0.2
Provides: bundled-npm(abbrev) = 1.1.1
Provides: bundled-npm(osenv) = 0.1.4
Provides: bundled-npm(minimist) = 0.0.8
Provides: bundled-npm(are-we-there-yet) = 1.1.4
Provides: bundled-npm(console-control-strings) = 1.1.0
Provides: bundled-npm(set-blocking) = 2.0.0
Provides: bundled-npm(gauge) = 2.7.4
Provides: bundled-npm(deep-extend) = 0.4.2
Provides: bundled-npm(ini) = 1.3.4
Provides: bundled-npm(minimist) = 1.2.0
Provides: bundled-npm(strip-json-comments) = 2.0.1
Provides: bundled-npm(aws-sign2) = 0.6.0
Provides: bundled-npm(aws4) = 1.6.0
Provides: bundled-npm(caseless) = 0.12.0
Provides: bundled-npm(extend) = 3.0.1
Provides: bundled-npm(combined-stream) = 1.0.5
Provides: bundled-npm(forever-agent) = 0.6.1
Provides: bundled-npm(har-validator) = 4.2.1
Provides: bundled-npm(form-data) = 2.1.4
Provides: bundled-npm(http-signature) = 1.1.1
Provides: bundled-npm(json-stringify-safe) = 5.0.1
Provides: bundled-npm(isstream) = 0.1.2
Provides: bundled-npm(is-typedarray) = 1.0.0
Provides: bundled-npm(mime-types) = 2.1.17
Provides: bundled-npm(oauth-sign) = 0.8.2
Provides: bundled-npm(performance-now) = 0.2.0
Provides: bundled-npm(qs) = 6.4.0
Provides: bundled-npm(safe-buffer) = 5.1.1
Provides: bundled-npm(stringstream) = 0.0.5
Provides: bundled-npm(tunnel-agent) = 0.6.0
Provides: bundled-npm(tough-cookie) = 2.3.3
Provides: bundled-npm(uuid) = 3.1.0
Provides: bundled-npm(boom) = 2.10.1
Provides: bundled-npm(hoek) = 2.16.3
Provides: bundled-npm(glob) = 7.1.2
Provides: bundled-npm(cryptiles) = 2.0.5
Provides: bundled-npm(sntp) = 1.0.9
Provides: bundled-npm(block-stream) = 0.0.9
Provides: bundled-npm(fstream) = 1.0.11
Provides: bundled-npm(inherits) = 2.0.3
Provides: bundled-npm(debug) = 2.6.9
Provides: bundled-npm(fstream-ignore) = 1.0.5
Provides: bundled-npm(once) = 1.4.0
Provides: bundled-npm(delegates) = 1.0.0
Provides: bundled-npm(readable-stream) = 2.3.3
Provides: bundled-npm(uid-number) = 0.0.6
Provides: bundled-npm(os-homedir) = 1.0.2
Provides: bundled-npm(os-tmpdir) = 1.0.2
Provides: bundled-npm(aproba) = 1.2.0
Provides: bundled-npm(has-unicode) = 2.0.1
Provides: bundled-npm(object-assign) = 4.1.1
Provides: bundled-npm(signal-exit) = 3.0.2
Provides: bundled-npm(string-width) = 1.0.2
Provides: bundled-npm(strip-ansi) = 3.0.1
Provides: bundled-npm(wide-align) = 1.1.2
Provides: bundled-npm(delayed-stream) = 1.0.0
Provides: bundled-npm(ajv) = 4.11.8
Provides: bundled-npm(asynckit) = 0.4.0
Provides: bundled-npm(har-schema) = 1.0.5
Provides: bundled-npm(assert-plus) = 0.2.0
Provides: bundled-npm(jsprim) = 1.4.1
Provides: bundled-npm(sshpk) = 1.13.1
Provides: bundled-npm(mime-db) = 1.30.0
Provides: bundled-npm(punycode) = 1.4.1
Provides: bundled-npm(fs.realpath) = 1.0.0
Provides: bundled-npm(inflight) = 1.0.6
Provides: bundled-npm(minimatch) = 3.0.4
Provides: bundled-npm(path-is-absolute) = 1.0.1
Provides: bundled-npm(graceful-fs) = 4.1.11
Provides: bundled-npm(ms) = 2.0.0
Provides: bundled-npm(wrappy) = 1.0.2
Provides: bundled-npm(core-util-is) = 1.0.2
Provides: bundled-npm(isarray) = 1.0.0
Provides: bundled-npm(process-nextick-args) = 1.0.7
Provides: bundled-npm(string_decoder) = 1.0.3
Provides: bundled-npm(util-deprecate) = 1.0.2
Provides: bundled-npm(code-point-at) = 1.1.0
Provides: bundled-npm(is-fullwidth-code-point) = 1.0.0
Provides: bundled-npm(ansi-regex) = 2.1.1
Provides: bundled-npm(json-stable-stringify) = 1.0.1
Provides: bundled-npm(co) = 4.6.0
Provides: bundled-npm(assert-plus) = 1.0.0
Provides: bundled-npm(verror) = 1.10.0
Provides: bundled-npm(extsprintf) = 1.3.0
Provides: bundled-npm(json-schema) = 0.2.3
Provides: bundled-npm(asn1) = 0.2.3
Provides: bundled-npm(dashdash) = 1.14.1
Provides: bundled-npm(getpass) = 0.1.7
Provides: bundled-npm(jsbn) = 0.1.1
Provides: bundled-npm(ecc-jsbn) = 0.1.1
Provides: bundled-npm(tweetnacl) = 0.14.5
Provides: bundled-npm(bcrypt-pbkdf) = 1.0.1
Provides: bundled-npm(brace-expansion) = 1.1.8
Provides: bundled-npm(number-is-nan) = 1.0.1
Provides: bundled-npm(jsonify) = 0.0.0
Provides: bundled-npm(balanced-match) = 1.0.0
Provides: bundled-npm(concat-map) = 0.0.1
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

%setup -T -q -a 111 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd /tmp/node_modules/v8-profiler
cp -pfr LICENSE binding.gyp package.json readme.md src tools v8-profiler.js node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf readme.md LICENSE ../../
# If any binaries are included, symlink them to bindir here


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}

%doc %{nodejs_sitelib}/%{npm_name}/LICENSE
%doc %{nodejs_sitelib}/%{npm_name}/readme.md

%changelog
* Fri Nov 3 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 5.7.0-1
- First release 
