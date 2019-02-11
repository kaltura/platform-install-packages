%global npm_name gulp
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 2.0.1
Release: 1
Summary: The streaming build system
License: FIXME
URL: http://github.com/wearefractal/gulp
Source0: http://registry.npmjs.org/gulp/-/gulp-2.0.1.tgz
Source1: http://registry.npmjs.org/glob-stream/-/glob-stream-0.1.0.tgz
Source2: http://registry.npmjs.org/mkdirp/-/mkdirp-0.3.5.tgz
Source3: http://registry.npmjs.org/optimist/-/optimist-0.6.0.tgz
Source4: http://registry.npmjs.org/event-stream/-/event-stream-3.0.16.tgz
Source5: http://registry.npmjs.org/gaze/-/gaze-0.4.2.tgz
Source6: http://registry.npmjs.org/gulp-util/-/gulp-util-1.0.0.tgz
Source7: http://registry.npmjs.org/orchestrator/-/orchestrator-0.0.6.tgz
Source8: http://registry.npmjs.org/chalk/-/chalk-0.3.0.tgz
Source9: http://registry.npmjs.org/wordwrap/-/wordwrap-0.0.3.tgz
Source10: http://registry.npmjs.org/glob/-/glob-7.1.3.tgz
Source11: http://registry.npmjs.org/event-stream/-/event-stream-4.0.1.tgz
Source12: http://registry.npmjs.org/resolve/-/resolve-0.5.1.tgz
Source13: http://registry.npmjs.org/minimist/-/minimist-0.0.10.tgz
Source14: http://registry.npmjs.org/from/-/from-0.1.7.tgz
Source15: http://registry.npmjs.org/duplexer/-/duplexer-0.0.4.tgz
Source16: http://registry.npmjs.org/through/-/through-2.3.8.tgz
Source17: http://registry.npmjs.org/map-stream/-/map-stream-0.0.2.tgz
Source18: http://registry.npmjs.org/stream-combiner/-/stream-combiner-0.0.0.tgz
Source19: http://registry.npmjs.org/pause-stream/-/pause-stream-0.0.10.tgz
Source20: http://registry.npmjs.org/split/-/split-0.2.10.tgz
Source21: http://registry.npmjs.org/globule/-/globule-0.1.0.tgz
Source22: http://registry.npmjs.org/ansi-styles/-/ansi-styles-0.2.0.tgz
Source23: http://registry.npmjs.org/has-color/-/has-color-0.1.7.tgz
Source24: http://registry.npmjs.org/events/-/events-0.5.0.tgz
Source25: http://registry.npmjs.org/sequencify/-/sequencify-0.0.7.tgz
Source26: http://registry.npmjs.org/fs.realpath/-/fs.realpath-1.0.0.tgz
Source27: http://registry.npmjs.org/inflight/-/inflight-1.0.6.tgz
Source28: http://registry.npmjs.org/inherits/-/inherits-2.0.3.tgz
Source29: http://registry.npmjs.org/minimatch/-/minimatch-3.0.4.tgz
Source30: http://registry.npmjs.org/once/-/once-1.4.0.tgz
Source31: http://registry.npmjs.org/duplexer/-/duplexer-0.1.1.tgz
Source32: http://registry.npmjs.org/path-is-absolute/-/path-is-absolute-1.0.1.tgz
Source33: http://registry.npmjs.org/map-stream/-/map-stream-0.0.7.tgz
Source34: http://registry.npmjs.org/pause-stream/-/pause-stream-0.0.11.tgz
Source35: http://registry.npmjs.org/split/-/split-1.0.1.tgz
Source36: http://registry.npmjs.org/stream-combiner/-/stream-combiner-0.2.2.tgz
Source37: http://registry.npmjs.org/duplexer/-/duplexer-0.0.2.tgz
Source38: http://registry.npmjs.org/lodash/-/lodash-1.0.2.tgz
Source39: http://registry.npmjs.org/minimatch/-/minimatch-0.2.14.tgz
Source40: http://registry.npmjs.org/glob/-/glob-3.1.21.tgz
Source41: http://registry.npmjs.org/wrappy/-/wrappy-1.0.2.tgz
Source42: http://registry.npmjs.org/brace-expansion/-/brace-expansion-1.1.11.tgz
Source43: http://registry.npmjs.org/lru-cache/-/lru-cache-2.7.3.tgz
Source44: http://registry.npmjs.org/sigmund/-/sigmund-1.0.1.tgz
Source45: http://registry.npmjs.org/graceful-fs/-/graceful-fs-1.2.3.tgz
Source46: http://registry.npmjs.org/balanced-match/-/balanced-match-1.0.0.tgz
Source47: http://registry.npmjs.org/inherits/-/inherits-1.0.2.tgz
Source48: http://registry.npmjs.org/concat-map/-/concat-map-0.0.1.tgz
Source49: gulp-2.0.1-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(gulp) = 2.0.1
Provides: bundled-npm(glob-stream) = 0.1.0
Provides: bundled-npm(mkdirp) = 0.3.5
Provides: bundled-npm(optimist) = 0.6.0
Provides: bundled-npm(event-stream) = 3.0.16
Provides: bundled-npm(gaze) = 0.4.2
Provides: bundled-npm(gulp-util) = 1.0.0
Provides: bundled-npm(orchestrator) = 0.0.6
Provides: bundled-npm(chalk) = 0.3.0
Provides: bundled-npm(wordwrap) = 0.0.3
Provides: bundled-npm(glob) = 7.1.3
Provides: bundled-npm(event-stream) = 4.0.1
Provides: bundled-npm(resolve) = 0.5.1
Provides: bundled-npm(minimist) = 0.0.10
Provides: bundled-npm(from) = 0.1.7
Provides: bundled-npm(duplexer) = 0.0.4
Provides: bundled-npm(through) = 2.3.8
Provides: bundled-npm(map-stream) = 0.0.2
Provides: bundled-npm(stream-combiner) = 0.0.0
Provides: bundled-npm(pause-stream) = 0.0.10
Provides: bundled-npm(split) = 0.2.10
Provides: bundled-npm(globule) = 0.1.0
Provides: bundled-npm(ansi-styles) = 0.2.0
Provides: bundled-npm(has-color) = 0.1.7
Provides: bundled-npm(events) = 0.5.0
Provides: bundled-npm(sequencify) = 0.0.7
Provides: bundled-npm(fs.realpath) = 1.0.0
Provides: bundled-npm(inflight) = 1.0.6
Provides: bundled-npm(inherits) = 2.0.3
Provides: bundled-npm(minimatch) = 3.0.4
Provides: bundled-npm(once) = 1.4.0
Provides: bundled-npm(duplexer) = 0.1.1
Provides: bundled-npm(path-is-absolute) = 1.0.1
Provides: bundled-npm(map-stream) = 0.0.7
Provides: bundled-npm(pause-stream) = 0.0.11
Provides: bundled-npm(split) = 1.0.1
Provides: bundled-npm(stream-combiner) = 0.2.2
Provides: bundled-npm(duplexer) = 0.0.2
Provides: bundled-npm(lodash) = 1.0.2
Provides: bundled-npm(minimatch) = 0.2.14
Provides: bundled-npm(glob) = 3.1.21
Provides: bundled-npm(wrappy) = 1.0.2
Provides: bundled-npm(brace-expansion) = 1.1.11
Provides: bundled-npm(lru-cache) = 2.7.3
Provides: bundled-npm(sigmund) = 1.0.1
Provides: bundled-npm(graceful-fs) = 1.2.3
Provides: bundled-npm(balanced-match) = 1.0.0
Provides: bundled-npm(inherits) = 1.0.2
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

%setup -T -q -a 49 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
pwd
cd /tmp/node_modules/gulp
cp -pfr .npmignore .travis.yml CHANGELOG.md LICENSE README.md bin index.js lib package.json test node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf CHANGELOG.md README.md LICENSE ../../
# If any binaries are included, symlink them to bindir here
mkdir -p %{buildroot}%{nodejs_sitelib}/${npm_name}/bin 
mkdir -p %{buildroot}%{_bindir}/ 
install -p -D -m0755 bin/gulp %{buildroot}%{nodejs_sitelib}/%{npm_name}/bin/gulp
ln -sf %{nodejs_sitelib}/%{npm_name}/bin/gulp %{buildroot}%{_bindir}/gulp


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}
%{_bindir}/gulp

#%doc LICENSE
#%doc CHANGELOG.md
#%doc README.md

%changelog
* Mon Feb 11 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 2.0.1-1
- First release 
