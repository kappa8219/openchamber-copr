%global debug_package %{nil}
%global __strip /bin/true
%global __provides_exclude_from ^/usr/lib/openchamber-web/node_modules/.*$
%global __requires_exclude_from ^/usr/lib/openchamber-web/node_modules/.*$
%global __requires_exclude ^/usr/bin/(node|pwsh|python3)$
%global node_version 24.14.0

Name:           openchamber-cli
Version:        2.5.0
Release:        1%{?dist}
Summary:        OpenChamber Web Server and CLI
License:        MIT
URL:            https://openchamber.dev/
Source0:        https://github.com/openchamber/openchamber/releases/download/v%{version}/openchamber-web-%{version}.tgz
Source1:        https://nodejs.org/dist/v%{node_version}/node-v%{node_version}-linux-x64.tar.xz
Source2:        LICENSE-%{version}
ExclusiveArch:  x86_64

BuildRequires:  tar
BuildRequires:  xz

%description
OpenChamber Web Server and CLI for running OpenChamber on a workstation or
server. This package provides the openchamber-cli command, including API-only and
LAN server modes.

%prep
echo "f08a1c3b222a09fa8bf019f3eeccec94d04ed83f8a4c4728120e2a7ef9efbd74  %{SOURCE0}" | sha256sum --check
echo "41cd79bb7877c81605a9e68ec4c91547774f46a40c67a17e34d7179ef11729df  %{SOURCE1}" | sha256sum --check
mkdir -p package
tar -xzf %{SOURCE0} --strip-components=1 -C package
tar -xJf %{SOURCE1}

%build
export PATH="$PWD/node-v%{node_version}-linux-x64/bin:$PATH"
cd package
npm install --omit=dev --ignore-scripts --no-audit --no-fund

%install
export QA_RPATHS=0x12
mkdir -p %{buildroot}%{_prefix}/lib/openchamber-web
mkdir -p %{buildroot}%{_bindir}
cp -a package/. %{buildroot}%{_prefix}/lib/openchamber-web/
mkdir -p %{buildroot}%{_prefix}/lib/openchamber-web/runtime
cp -a node-v%{node_version}-linux-x64 \
    %{buildroot}%{_prefix}/lib/openchamber-web/runtime/
install -Dpm 0644 %{SOURCE2} \
    %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

cat > %{buildroot}%{_bindir}/openchamber-cli <<'EOF'
#!/bin/sh
ROOT=/usr/lib/openchamber-web
export PATH="$ROOT/runtime/node-v%{node_version}-linux-x64/bin:$PATH"
exec node "$ROOT/bin/cli.js" "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/openchamber-cli

find %{buildroot} -mindepth 1 \( -type f -o -type l \) \
    ! -path '%{buildroot}%{_datadir}/licenses/%{name}/LICENSE' \
    -printf '/%%P\n' | sort -u > %{name}.files

%check
NODE=%{buildroot}%{_prefix}/lib/openchamber-web/runtime/node-v%{node_version}-linux-x64/bin/node
"$NODE" %{buildroot}%{_prefix}/lib/openchamber-web/bin/cli.js --version | grep -Fx '%{version}'
"$NODE" %{buildroot}%{_prefix}/lib/openchamber-web/bin/cli.js --help >/dev/null

%files -f %{name}.files
%license %{_datadir}/licenses/%{name}/LICENSE

%changelog
* Tue Oct 20 2026 OpenChamber COPR <noreply@github.com> - 2.5.0-1
- Update web CLI to v2.5.0

* Mon Oct 19 2026 OpenChamber COPR <noreply@github.com> - 2.4.0-1
- Update web CLI to v2.4.0

* Thu Oct 15 2026 OpenChamber COPR <noreply@github.com> - 2.3.3-1
- Update web CLI to v2.3.3

* Wed Oct 14 2026 OpenChamber COPR <noreply@github.com> - 2.3.2-2
- Exclude shared system directories from the package file list

* Wed Oct 14 2026 OpenChamber COPR <noreply@github.com> - 2.3.2-1
- Package the official OpenChamber web CLI tarball with its declared Node runtime
