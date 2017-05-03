%global npm_name forever
%global enable_tests 0

%{?nodejs_find_provides_and_requires}
%define cache_dir /tmp/npm_cache_%{name}-%{version}-%{release}

Name: nodejs-%{npm_name}
Version: 0.15.3
Release: 1
Summary: A simple CLI tool for ensuring that a given node script runs continuously
License: MIT
URL: https://github.com/foreverjs/forever.git
Source0: http://registry.npmjs.org/forever/-/forever-0.15.3.tgz
Source1: http://registry.npmjs.org/object-assign/-/object-assign-3.0.0.tgz
Source2: http://registry.npmjs.org/cliff/-/cliff-0.1.10.tgz
Source3: http://registry.npmjs.org/colors/-/colors-0.6.2.tgz
Source4: http://registry.npmjs.org/forever-monitor/-/forever-monitor-1.7.1.tgz
Source5: http://registry.npmjs.org/nconf/-/nconf-0.6.9.tgz
Source6: http://registry.npmjs.org/flatiron/-/flatiron-0.4.3.tgz
Source7: http://registry.npmjs.org/clone/-/clone-1.0.2.tgz
Source8: http://registry.npmjs.org/nssocket/-/nssocket-0.5.3.tgz
Source9: http://registry.npmjs.org/path-is-absolute/-/path-is-absolute-1.0.1.tgz
Source10: http://registry.npmjs.org/optimist/-/optimist-0.6.1.tgz
Source11: http://registry.npmjs.org/prettyjson/-/prettyjson-1.2.1.tgz
Source12: http://registry.npmjs.org/shush/-/shush-1.0.0.tgz
Source13: http://registry.npmjs.org/colors/-/colors-1.0.3.tgz
Source14: http://registry.npmjs.org/timespan/-/timespan-2.3.0.tgz
Source15: http://registry.npmjs.org/winston/-/winston-0.8.3.tgz
Source16: http://registry.npmjs.org/eyes/-/eyes-0.1.8.tgz
Source17: http://registry.npmjs.org/minimatch/-/minimatch-3.0.3.tgz
Source18: http://registry.npmjs.org/broadway/-/broadway-0.3.6.tgz
Source19: http://registry.npmjs.org/utile/-/utile-0.2.1.tgz
Source20: http://registry.npmjs.org/chokidar/-/chokidar-1.6.1.tgz
Source21: http://registry.npmjs.org/ini/-/ini-1.3.4.tgz
Source22: http://registry.npmjs.org/ps-tree/-/ps-tree-0.0.3.tgz
Source23: http://registry.npmjs.org/optimist/-/optimist-0.6.0.tgz
Source24: http://registry.npmjs.org/prompt/-/prompt-0.2.14.tgz
Source25: http://registry.npmjs.org/async/-/async-0.2.9.tgz
Source26: http://registry.npmjs.org/director/-/director-1.2.7.tgz
Source27: http://registry.npmjs.org/eventemitter2/-/eventemitter2-0.4.14.tgz
Source28: http://registry.npmjs.org/wordwrap/-/wordwrap-0.0.3.tgz
Source29: http://registry.npmjs.org/colors/-/colors-1.1.2.tgz
Source30: http://registry.npmjs.org/minimist/-/minimist-1.2.0.tgz
Source31: http://registry.npmjs.org/caller/-/caller-0.0.1.tgz
Source32: http://registry.npmjs.org/strip-json-comments/-/strip-json-comments-0.1.3.tgz
Source33: http://registry.npmjs.org/minimist/-/minimist-0.0.10.tgz
Source34: http://registry.npmjs.org/lazy/-/lazy-1.0.11.tgz
Source35: http://registry.npmjs.org/async/-/async-0.2.10.tgz
Source36: http://registry.npmjs.org/pkginfo/-/pkginfo-0.3.1.tgz
Source37: http://registry.npmjs.org/isstream/-/isstream-0.1.2.tgz
Source38: http://registry.npmjs.org/cycle/-/cycle-1.0.3.tgz
Source39: http://registry.npmjs.org/stack-trace/-/stack-trace-0.0.9.tgz
Source40: http://registry.npmjs.org/brace-expansion/-/brace-expansion-1.1.7.tgz
Source41: http://registry.npmjs.org/cliff/-/cliff-0.1.9.tgz
Source42: http://registry.npmjs.org/deep-equal/-/deep-equal-1.0.1.tgz
Source43: http://registry.npmjs.org/winston/-/winston-0.8.0.tgz
Source44: http://registry.npmjs.org/async-each/-/async-each-1.0.1.tgz
Source45: http://registry.npmjs.org/anymatch/-/anymatch-1.3.0.tgz
Source46: http://registry.npmjs.org/mkdirp/-/mkdirp-0.5.1.tgz
Source47: http://registry.npmjs.org/ncp/-/ncp-0.4.2.tgz
Source48: http://registry.npmjs.org/rimraf/-/rimraf-2.6.1.tgz
Source49: http://registry.npmjs.org/inherits/-/inherits-2.0.3.tgz
Source50: http://registry.npmjs.org/glob-parent/-/glob-parent-2.0.0.tgz
Source51: http://registry.npmjs.org/i/-/i-0.3.5.tgz
Source52: http://registry.npmjs.org/is-binary-path/-/is-binary-path-1.0.1.tgz
Source53: http://registry.npmjs.org/is-glob/-/is-glob-2.0.1.tgz
Source54: http://registry.npmjs.org/readdirp/-/readdirp-2.1.0.tgz
Source55: http://registry.npmjs.org/fsevents/-/fsevents-1.1.1.tgz
Source56: http://registry.npmjs.org/event-stream/-/event-stream-0.5.3.tgz
Source57: http://registry.npmjs.org/pkginfo/-/pkginfo-0.4.0.tgz
Source58: http://registry.npmjs.org/balanced-match/-/balanced-match-0.4.2.tgz
Source59: http://registry.npmjs.org/read/-/read-1.0.7.tgz
Source60: http://registry.npmjs.org/concat-map/-/concat-map-0.0.1.tgz
Source61: http://registry.npmjs.org/revalidator/-/revalidator-0.1.8.tgz
Source62: http://registry.npmjs.org/tape/-/tape-2.3.3.tgz
Source63: http://registry.npmjs.org/minimist/-/minimist-0.0.8.tgz
Source64: http://registry.npmjs.org/arrify/-/arrify-1.0.1.tgz
Source65: http://registry.npmjs.org/is-extglob/-/is-extglob-1.0.0.tgz
Source66: http://registry.npmjs.org/micromatch/-/micromatch-2.3.11.tgz
Source67: http://registry.npmjs.org/glob/-/glob-7.1.1.tgz
Source68: http://registry.npmjs.org/binary-extensions/-/binary-extensions-1.8.0.tgz
Source69: http://registry.npmjs.org/set-immediate-shim/-/set-immediate-shim-1.0.1.tgz
Source70: http://registry.npmjs.org/graceful-fs/-/graceful-fs-4.1.11.tgz
Source71: http://registry.npmjs.org/readable-stream/-/readable-stream-2.2.9.tgz
Source72: http://registry.npmjs.org/deep-equal/-/deep-equal-0.1.2.tgz
Source73: http://registry.npmjs.org/defined/-/defined-0.0.0.tgz
Source74: http://registry.npmjs.org/through/-/through-2.3.8.tgz
Source75: http://registry.npmjs.org/optimist/-/optimist-0.2.8.tgz
Source76: http://registry.npmjs.org/mute-stream/-/mute-stream-0.0.7.tgz
Source77: http://registry.npmjs.org/jsonify/-/jsonify-0.0.0.tgz
Source78: http://registry.npmjs.org/nan/-/nan-2.6.2.tgz
Source79: http://registry.npmjs.org/array-unique/-/array-unique-0.2.1.tgz
Source80: http://registry.npmjs.org/arr-diff/-/arr-diff-2.0.0.tgz
Source81: http://registry.npmjs.org/resumer/-/resumer-0.0.0.tgz
Source82: http://registry.npmjs.org/expand-brackets/-/expand-brackets-0.1.5.tgz
Source83: http://registry.npmjs.org/extglob/-/extglob-0.3.2.tgz
Source84: http://registry.npmjs.org/node-pre-gyp/-/node-pre-gyp-0.6.34.tgz
Source85: http://registry.npmjs.org/braces/-/braces-1.8.5.tgz
Source86: http://registry.npmjs.org/filename-regex/-/filename-regex-2.0.0.tgz
Source87: http://registry.npmjs.org/kind-of/-/kind-of-3.2.0.tgz
Source88: http://registry.npmjs.org/regex-cache/-/regex-cache-0.4.3.tgz
Source89: http://registry.npmjs.org/object.omit/-/object.omit-2.0.1.tgz
Source90: http://registry.npmjs.org/parse-glob/-/parse-glob-3.0.4.tgz
Source91: http://registry.npmjs.org/normalize-path/-/normalize-path-2.1.1.tgz
Source92: http://registry.npmjs.org/once/-/once-1.4.0.tgz
Source93: http://registry.npmjs.org/buffer-shims/-/buffer-shims-1.0.0.tgz
Source94: http://registry.npmjs.org/inflight/-/inflight-1.0.6.tgz
Source95: http://registry.npmjs.org/fs.realpath/-/fs.realpath-1.0.0.tgz
Source96: http://registry.npmjs.org/core-util-is/-/core-util-is-1.0.2.tgz
Source97: http://registry.npmjs.org/isarray/-/isarray-1.0.0.tgz
Source98: http://registry.npmjs.org/process-nextick-args/-/process-nextick-args-1.0.7.tgz
Source99: http://registry.npmjs.org/string_decoder/-/string_decoder-1.0.0.tgz
Source100: http://registry.npmjs.org/util-deprecate/-/util-deprecate-1.0.2.tgz
Source101: http://registry.npmjs.org/arr-flatten/-/arr-flatten-1.0.3.tgz
Source102: http://registry.npmjs.org/is-posix-bracket/-/is-posix-bracket-0.1.1.tgz
Source103: http://registry.npmjs.org/nopt/-/nopt-4.0.1.tgz
Source104: http://registry.npmjs.org/npmlog/-/npmlog-4.0.2.tgz
Source105: http://registry.npmjs.org/rc/-/rc-1.2.1.tgz
Source106: http://registry.npmjs.org/request/-/request-2.81.0.tgz
Source107: http://registry.npmjs.org/preserve/-/preserve-0.2.0.tgz
Source108: http://registry.npmjs.org/is-buffer/-/is-buffer-1.1.5.tgz
Source109: http://registry.npmjs.org/repeat-element/-/repeat-element-1.1.2.tgz
Source110: http://registry.npmjs.org/tar-pack/-/tar-pack-3.4.0.tgz
Source111: http://registry.npmjs.org/is-equal-shallow/-/is-equal-shallow-0.1.3.tgz
Source112: http://registry.npmjs.org/tar/-/tar-2.2.1.tgz
Source113: http://registry.npmjs.org/expand-range/-/expand-range-1.8.2.tgz
Source114: http://registry.npmjs.org/semver/-/semver-5.3.0.tgz
Source115: http://registry.npmjs.org/is-primitive/-/is-primitive-2.0.0.tgz
Source116: http://registry.npmjs.org/for-own/-/for-own-0.1.5.tgz
Source117: http://registry.npmjs.org/is-extendable/-/is-extendable-0.1.1.tgz
Source118: http://registry.npmjs.org/glob-base/-/glob-base-0.3.0.tgz
Source119: http://registry.npmjs.org/is-dotfile/-/is-dotfile-1.0.2.tgz
Source120: http://registry.npmjs.org/remove-trailing-separator/-/remove-trailing-separator-1.0.1.tgz
Source121: http://registry.npmjs.org/wrappy/-/wrappy-1.0.2.tgz
Source122: http://registry.npmjs.org/abbrev/-/abbrev-1.1.0.tgz
Source123: http://registry.npmjs.org/osenv/-/osenv-0.1.4.tgz
Source124: http://registry.npmjs.org/are-we-there-yet/-/are-we-there-yet-1.1.4.tgz
Source125: http://registry.npmjs.org/console-control-strings/-/console-control-strings-1.1.0.tgz
Source126: http://registry.npmjs.org/set-blocking/-/set-blocking-2.0.0.tgz
Source127: http://registry.npmjs.org/strip-json-comments/-/strip-json-comments-2.0.1.tgz
Source128: http://registry.npmjs.org/gauge/-/gauge-2.7.4.tgz
Source129: http://registry.npmjs.org/deep-extend/-/deep-extend-0.4.1.tgz
Source130: http://registry.npmjs.org/aws-sign2/-/aws-sign2-0.6.0.tgz
Source131: http://registry.npmjs.org/aws4/-/aws4-1.6.0.tgz
Source132: http://registry.npmjs.org/extend/-/extend-3.0.0.tgz
Source133: http://registry.npmjs.org/combined-stream/-/combined-stream-1.0.5.tgz
Source134: http://registry.npmjs.org/caseless/-/caseless-0.12.0.tgz
Source135: http://registry.npmjs.org/forever-agent/-/forever-agent-0.6.1.tgz
Source136: http://registry.npmjs.org/form-data/-/form-data-2.1.4.tgz
Source137: http://registry.npmjs.org/http-signature/-/http-signature-1.1.1.tgz
Source138: http://registry.npmjs.org/har-validator/-/har-validator-4.2.1.tgz
Source139: http://registry.npmjs.org/hawk/-/hawk-3.1.3.tgz
Source140: http://registry.npmjs.org/is-typedarray/-/is-typedarray-1.0.0.tgz
Source141: http://registry.npmjs.org/oauth-sign/-/oauth-sign-0.8.2.tgz
Source142: http://registry.npmjs.org/json-stringify-safe/-/json-stringify-safe-5.0.1.tgz
Source143: http://registry.npmjs.org/performance-now/-/performance-now-0.2.0.tgz
Source144: http://registry.npmjs.org/mime-types/-/mime-types-2.1.15.tgz
Source145: http://registry.npmjs.org/qs/-/qs-6.4.0.tgz
Source146: http://registry.npmjs.org/stringstream/-/stringstream-0.0.5.tgz
Source147: http://registry.npmjs.org/tunnel-agent/-/tunnel-agent-0.6.0.tgz
Source148: http://registry.npmjs.org/safe-buffer/-/safe-buffer-5.0.1.tgz
Source149: http://registry.npmjs.org/uuid/-/uuid-3.0.1.tgz
Source150: http://registry.npmjs.org/tough-cookie/-/tough-cookie-2.3.2.tgz
Source151: http://registry.npmjs.org/debug/-/debug-2.6.4.tgz
Source152: http://registry.npmjs.org/fstream/-/fstream-1.0.11.tgz
Source153: http://registry.npmjs.org/fstream-ignore/-/fstream-ignore-1.0.5.tgz
Source154: http://registry.npmjs.org/uid-number/-/uid-number-0.0.6.tgz
Source155: http://registry.npmjs.org/block-stream/-/block-stream-0.0.9.tgz
Source156: http://registry.npmjs.org/os-homedir/-/os-homedir-1.0.2.tgz
Source157: http://registry.npmjs.org/for-in/-/for-in-1.0.2.tgz
Source158: http://registry.npmjs.org/os-tmpdir/-/os-tmpdir-1.0.2.tgz
Source159: http://registry.npmjs.org/delegates/-/delegates-1.0.0.tgz
Source160: http://registry.npmjs.org/fill-range/-/fill-range-2.2.3.tgz
Source161: http://registry.npmjs.org/aproba/-/aproba-1.1.1.tgz
Source162: http://registry.npmjs.org/has-unicode/-/has-unicode-2.0.1.tgz
Source163: http://registry.npmjs.org/object-assign/-/object-assign-4.1.1.tgz
Source164: http://registry.npmjs.org/string-width/-/string-width-1.0.2.tgz
Source165: http://registry.npmjs.org/strip-ansi/-/strip-ansi-3.0.1.tgz
Source166: http://registry.npmjs.org/signal-exit/-/signal-exit-3.0.2.tgz
Source167: http://registry.npmjs.org/wide-align/-/wide-align-1.1.0.tgz
Source168: http://registry.npmjs.org/assert-plus/-/assert-plus-0.2.0.tgz
Source169: http://registry.npmjs.org/jsprim/-/jsprim-1.4.0.tgz
Source170: http://registry.npmjs.org/sshpk/-/sshpk-1.13.0.tgz
Source171: http://registry.npmjs.org/asynckit/-/asynckit-0.4.0.tgz
Source172: http://registry.npmjs.org/delayed-stream/-/delayed-stream-1.0.0.tgz
Source173: http://registry.npmjs.org/har-schema/-/har-schema-1.0.5.tgz
Source174: http://registry.npmjs.org/cryptiles/-/cryptiles-2.0.5.tgz
Source175: http://registry.npmjs.org/sntp/-/sntp-1.0.9.tgz
Source176: http://registry.npmjs.org/hoek/-/hoek-2.16.3.tgz
Source177: http://registry.npmjs.org/boom/-/boom-2.10.1.tgz
Source178: http://registry.npmjs.org/mime-db/-/mime-db-1.27.0.tgz
Source179: http://registry.npmjs.org/punycode/-/punycode-1.4.1.tgz
Source180: http://registry.npmjs.org/ms/-/ms-0.7.3.tgz
Source181: http://registry.npmjs.org/ajv/-/ajv-4.11.7.tgz
Source182: http://registry.npmjs.org/is-number/-/is-number-2.1.0.tgz
Source183: http://registry.npmjs.org/randomatic/-/randomatic-1.1.6.tgz
Source184: http://registry.npmjs.org/isobject/-/isobject-2.1.0.tgz
Source185: http://registry.npmjs.org/repeat-string/-/repeat-string-1.6.1.tgz
Source186: http://registry.npmjs.org/assert-plus/-/assert-plus-1.0.0.tgz
Source187: http://registry.npmjs.org/ansi-regex/-/ansi-regex-2.1.1.tgz
Source188: http://registry.npmjs.org/code-point-at/-/code-point-at-1.1.0.tgz
Source189: http://registry.npmjs.org/is-fullwidth-code-point/-/is-fullwidth-code-point-1.0.0.tgz
Source190: http://registry.npmjs.org/json-schema/-/json-schema-0.2.3.tgz
Source191: http://registry.npmjs.org/extsprintf/-/extsprintf-1.0.2.tgz
Source192: http://registry.npmjs.org/dashdash/-/dashdash-1.14.1.tgz
Source193: http://registry.npmjs.org/verror/-/verror-1.3.6.tgz
Source194: http://registry.npmjs.org/asn1/-/asn1-0.2.3.tgz
Source195: http://registry.npmjs.org/getpass/-/getpass-0.1.7.tgz
Source196: http://registry.npmjs.org/jsbn/-/jsbn-0.1.1.tgz
Source197: http://registry.npmjs.org/jodid25519/-/jodid25519-1.0.2.tgz
Source198: http://registry.npmjs.org/tweetnacl/-/tweetnacl-0.14.5.tgz
Source199: http://registry.npmjs.org/ecc-jsbn/-/ecc-jsbn-0.1.1.tgz
Source200: http://registry.npmjs.org/bcrypt-pbkdf/-/bcrypt-pbkdf-1.0.1.tgz
Source201: http://registry.npmjs.org/json-stable-stringify/-/json-stable-stringify-1.0.1.tgz
Source202: http://registry.npmjs.org/co/-/co-4.6.0.tgz
Source203: http://registry.npmjs.org/number-is-nan/-/number-is-nan-1.0.1.tgz
Source204: forever-0.15.3-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(forever) = 0.15.3
Provides: bundled-npm(object-assign) = 3.0.0
Provides: bundled-npm(cliff) = 0.1.10
Provides: bundled-npm(colors) = 0.6.2
Provides: bundled-npm(forever-monitor) = 1.7.1
Provides: bundled-npm(nconf) = 0.6.9
Provides: bundled-npm(flatiron) = 0.4.3
Provides: bundled-npm(clone) = 1.0.2
Provides: bundled-npm(nssocket) = 0.5.3
Provides: bundled-npm(path-is-absolute) = 1.0.1
Provides: bundled-npm(optimist) = 0.6.1
Provides: bundled-npm(prettyjson) = 1.2.1
Provides: bundled-npm(shush) = 1.0.0
Provides: bundled-npm(colors) = 1.0.3
Provides: bundled-npm(timespan) = 2.3.0
Provides: bundled-npm(winston) = 0.8.3
Provides: bundled-npm(eyes) = 0.1.8
Provides: bundled-npm(minimatch) = 3.0.3
Provides: bundled-npm(broadway) = 0.3.6
Provides: bundled-npm(utile) = 0.2.1
Provides: bundled-npm(chokidar) = 1.6.1
Provides: bundled-npm(ini) = 1.3.4
Provides: bundled-npm(ps-tree) = 0.0.3
Provides: bundled-npm(optimist) = 0.6.0
Provides: bundled-npm(prompt) = 0.2.14
Provides: bundled-npm(async) = 0.2.9
Provides: bundled-npm(director) = 1.2.7
Provides: bundled-npm(eventemitter2) = 0.4.14
Provides: bundled-npm(wordwrap) = 0.0.3
Provides: bundled-npm(colors) = 1.1.2
Provides: bundled-npm(minimist) = 1.2.0
Provides: bundled-npm(caller) = 0.0.1
Provides: bundled-npm(strip-json-comments) = 0.1.3
Provides: bundled-npm(minimist) = 0.0.10
Provides: bundled-npm(lazy) = 1.0.11
Provides: bundled-npm(async) = 0.2.10
Provides: bundled-npm(pkginfo) = 0.3.1
Provides: bundled-npm(isstream) = 0.1.2
Provides: bundled-npm(cycle) = 1.0.3
Provides: bundled-npm(stack-trace) = 0.0.9
Provides: bundled-npm(brace-expansion) = 1.1.7
Provides: bundled-npm(cliff) = 0.1.9
Provides: bundled-npm(deep-equal) = 1.0.1
Provides: bundled-npm(winston) = 0.8.0
Provides: bundled-npm(async-each) = 1.0.1
Provides: bundled-npm(anymatch) = 1.3.0
Provides: bundled-npm(mkdirp) = 0.5.1
Provides: bundled-npm(ncp) = 0.4.2
Provides: bundled-npm(rimraf) = 2.6.1
Provides: bundled-npm(inherits) = 2.0.3
Provides: bundled-npm(glob-parent) = 2.0.0
Provides: bundled-npm(i) = 0.3.5
Provides: bundled-npm(is-binary-path) = 1.0.1
Provides: bundled-npm(is-glob) = 2.0.1
Provides: bundled-npm(readdirp) = 2.1.0
Provides: bundled-npm(fsevents) = 1.1.1
Provides: bundled-npm(event-stream) = 0.5.3
Provides: bundled-npm(pkginfo) = 0.4.0
Provides: bundled-npm(balanced-match) = 0.4.2
Provides: bundled-npm(read) = 1.0.7
Provides: bundled-npm(concat-map) = 0.0.1
Provides: bundled-npm(revalidator) = 0.1.8
Provides: bundled-npm(tape) = 2.3.3
Provides: bundled-npm(minimist) = 0.0.8
Provides: bundled-npm(arrify) = 1.0.1
Provides: bundled-npm(is-extglob) = 1.0.0
Provides: bundled-npm(micromatch) = 2.3.11
Provides: bundled-npm(glob) = 7.1.1
Provides: bundled-npm(binary-extensions) = 1.8.0
Provides: bundled-npm(set-immediate-shim) = 1.0.1
Provides: bundled-npm(graceful-fs) = 4.1.11
Provides: bundled-npm(readable-stream) = 2.2.9
Provides: bundled-npm(deep-equal) = 0.1.2
Provides: bundled-npm(defined) = 0.0.0
Provides: bundled-npm(through) = 2.3.8
Provides: bundled-npm(optimist) = 0.2.8
Provides: bundled-npm(mute-stream) = 0.0.7
Provides: bundled-npm(jsonify) = 0.0.0
Provides: bundled-npm(nan) = 2.6.2
Provides: bundled-npm(array-unique) = 0.2.1
Provides: bundled-npm(arr-diff) = 2.0.0
Provides: bundled-npm(resumer) = 0.0.0
Provides: bundled-npm(expand-brackets) = 0.1.5
Provides: bundled-npm(extglob) = 0.3.2
Provides: bundled-npm(node-pre-gyp) = 0.6.34
Provides: bundled-npm(braces) = 1.8.5
Provides: bundled-npm(filename-regex) = 2.0.0
Provides: bundled-npm(kind-of) = 3.2.0
Provides: bundled-npm(regex-cache) = 0.4.3
Provides: bundled-npm(object.omit) = 2.0.1
Provides: bundled-npm(parse-glob) = 3.0.4
Provides: bundled-npm(normalize-path) = 2.1.1
Provides: bundled-npm(once) = 1.4.0
Provides: bundled-npm(buffer-shims) = 1.0.0
Provides: bundled-npm(inflight) = 1.0.6
Provides: bundled-npm(fs.realpath) = 1.0.0
Provides: bundled-npm(core-util-is) = 1.0.2
Provides: bundled-npm(isarray) = 1.0.0
Provides: bundled-npm(process-nextick-args) = 1.0.7
Provides: bundled-npm(string_decoder) = 1.0.0
Provides: bundled-npm(util-deprecate) = 1.0.2
Provides: bundled-npm(arr-flatten) = 1.0.3
Provides: bundled-npm(is-posix-bracket) = 0.1.1
Provides: bundled-npm(nopt) = 4.0.1
Provides: bundled-npm(npmlog) = 4.0.2
Provides: bundled-npm(rc) = 1.2.1
Provides: bundled-npm(request) = 2.81.0
Provides: bundled-npm(preserve) = 0.2.0
Provides: bundled-npm(is-buffer) = 1.1.5
Provides: bundled-npm(repeat-element) = 1.1.2
Provides: bundled-npm(tar-pack) = 3.4.0
Provides: bundled-npm(is-equal-shallow) = 0.1.3
Provides: bundled-npm(tar) = 2.2.1
Provides: bundled-npm(expand-range) = 1.8.2
Provides: bundled-npm(semver) = 5.3.0
Provides: bundled-npm(is-primitive) = 2.0.0
Provides: bundled-npm(for-own) = 0.1.5
Provides: bundled-npm(is-extendable) = 0.1.1
Provides: bundled-npm(glob-base) = 0.3.0
Provides: bundled-npm(is-dotfile) = 1.0.2
Provides: bundled-npm(remove-trailing-separator) = 1.0.1
Provides: bundled-npm(wrappy) = 1.0.2
Provides: bundled-npm(abbrev) = 1.1.0
Provides: bundled-npm(osenv) = 0.1.4
Provides: bundled-npm(are-we-there-yet) = 1.1.4
Provides: bundled-npm(console-control-strings) = 1.1.0
Provides: bundled-npm(set-blocking) = 2.0.0
Provides: bundled-npm(strip-json-comments) = 2.0.1
Provides: bundled-npm(gauge) = 2.7.4
Provides: bundled-npm(deep-extend) = 0.4.1
Provides: bundled-npm(aws-sign2) = 0.6.0
Provides: bundled-npm(aws4) = 1.6.0
Provides: bundled-npm(extend) = 3.0.0
Provides: bundled-npm(combined-stream) = 1.0.5
Provides: bundled-npm(caseless) = 0.12.0
Provides: bundled-npm(forever-agent) = 0.6.1
Provides: bundled-npm(form-data) = 2.1.4
Provides: bundled-npm(http-signature) = 1.1.1
Provides: bundled-npm(har-validator) = 4.2.1
Provides: bundled-npm(hawk) = 3.1.3
Provides: bundled-npm(is-typedarray) = 1.0.0
Provides: bundled-npm(oauth-sign) = 0.8.2
Provides: bundled-npm(json-stringify-safe) = 5.0.1
Provides: bundled-npm(performance-now) = 0.2.0
Provides: bundled-npm(mime-types) = 2.1.15
Provides: bundled-npm(qs) = 6.4.0
Provides: bundled-npm(stringstream) = 0.0.5
Provides: bundled-npm(tunnel-agent) = 0.6.0
Provides: bundled-npm(safe-buffer) = 5.0.1
Provides: bundled-npm(uuid) = 3.0.1
Provides: bundled-npm(tough-cookie) = 2.3.2
Provides: bundled-npm(debug) = 2.6.4
Provides: bundled-npm(fstream) = 1.0.11
Provides: bundled-npm(fstream-ignore) = 1.0.5
Provides: bundled-npm(uid-number) = 0.0.6
Provides: bundled-npm(block-stream) = 0.0.9
Provides: bundled-npm(os-homedir) = 1.0.2
Provides: bundled-npm(for-in) = 1.0.2
Provides: bundled-npm(os-tmpdir) = 1.0.2
Provides: bundled-npm(delegates) = 1.0.0
Provides: bundled-npm(fill-range) = 2.2.3
Provides: bundled-npm(aproba) = 1.1.1
Provides: bundled-npm(has-unicode) = 2.0.1
Provides: bundled-npm(object-assign) = 4.1.1
Provides: bundled-npm(string-width) = 1.0.2
Provides: bundled-npm(strip-ansi) = 3.0.1
Provides: bundled-npm(signal-exit) = 3.0.2
Provides: bundled-npm(wide-align) = 1.1.0
Provides: bundled-npm(assert-plus) = 0.2.0
Provides: bundled-npm(jsprim) = 1.4.0
Provides: bundled-npm(sshpk) = 1.13.0
Provides: bundled-npm(asynckit) = 0.4.0
Provides: bundled-npm(delayed-stream) = 1.0.0
Provides: bundled-npm(har-schema) = 1.0.5
Provides: bundled-npm(cryptiles) = 2.0.5
Provides: bundled-npm(sntp) = 1.0.9
Provides: bundled-npm(hoek) = 2.16.3
Provides: bundled-npm(boom) = 2.10.1
Provides: bundled-npm(mime-db) = 1.27.0
Provides: bundled-npm(punycode) = 1.4.1
Provides: bundled-npm(ms) = 0.7.3
Provides: bundled-npm(ajv) = 4.11.7
Provides: bundled-npm(is-number) = 2.1.0
Provides: bundled-npm(randomatic) = 1.1.6
Provides: bundled-npm(isobject) = 2.1.0
Provides: bundled-npm(repeat-string) = 1.6.1
Provides: bundled-npm(assert-plus) = 1.0.0
Provides: bundled-npm(ansi-regex) = 2.1.1
Provides: bundled-npm(code-point-at) = 1.1.0
Provides: bundled-npm(is-fullwidth-code-point) = 1.0.0
Provides: bundled-npm(json-schema) = 0.2.3
Provides: bundled-npm(extsprintf) = 1.0.2
Provides: bundled-npm(dashdash) = 1.14.1
Provides: bundled-npm(verror) = 1.3.6
Provides: bundled-npm(asn1) = 0.2.3
Provides: bundled-npm(getpass) = 0.1.7
Provides: bundled-npm(jsbn) = 0.1.1
Provides: bundled-npm(jodid25519) = 1.0.2
Provides: bundled-npm(tweetnacl) = 0.14.5
Provides: bundled-npm(ecc-jsbn) = 0.1.1
Provides: bundled-npm(bcrypt-pbkdf) = 1.0.1
Provides: bundled-npm(json-stable-stringify) = 1.0.1
Provides: bundled-npm(co) = 4.6.0
Provides: bundled-npm(number-is-nan) = 1.0.1
AutoReq: no 
AutoProv: no 


%description
%{summary}

%prep
mkdir -p %{cache_dir}
for tgz in %{sources}; do
  echo $tgz | grep -q registry.npmjs.org || npm cache add --cache %{cache_dir} $tgz
done

%setup -T -q -a 204 -D -n %{cache_dir}

%build
npm install --cache-min Infinity --cache %{cache_dir} --no-optional --global-style true %{npm_name}@%{version}

%clean
rm -rf %{buildroot} %{cache_dir}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd node_modules/forever
for i in .editorconfig .jshintrc .npmignore .travis.yml CHANGELOG.md LICENSE README.md bin lib package.json test node_modules;do
	if [ -r $i ];then
		cp -pfr $i %{buildroot}%{nodejs_sitelib}/%{npm_name}
	fi
done
cp -pf CHANGELOG.md README.md ../../
# If any binaries are included, symlink them to bindir here
mkdir -p %{buildroot}%{nodejs_sitelib}/${npm_name}/bin 
mkdir -p %{buildroot}%{_bindir}/ 
install -p -D -m0755 bin/forever %{buildroot}%{nodejs_sitelib}/%{npm_name}/bin/forever
ln -sf %{nodejs_sitelib}/%{npm_name}/bin/forever %{buildroot}%{_bindir}/forever


#%nodejs_symlink_deps

%if 0%{?enable_tests}
%check
%{nodejs_symlink_deps} --check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}
%{_bindir}/forever

%doc CHANGELOG.md
%doc README.md

%changelog
* Wed Apr 26 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 0.15.3-1
- First release
