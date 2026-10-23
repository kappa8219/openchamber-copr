%global debug_package %{nil}
%global __strip /bin/true
%global __provides_exclude_from ^/usr/lib/openchamber-web/node_modules/.*$
%global __requires_exclude_from ^/usr/lib/openchamber-web/node_modules/.*$
%global __requires_exclude ^/usr/bin/(node|pwsh|python3)$
%global node_version 24.22.1

Name:           openchamber-cli
Version:        2.5.1
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
echo "94505b2432fbde74e3b05c5da75441bbd4f45edd6b1843f7e418f7e51578c274  %{SOURCE0}" | sha256sum --check
echo "6c172a9ab6718f7b801fb5a7bd486af2ee5e32758086a04b84fcce2aa77095e6  %{SOURCE1}" | sha256sum --check
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
* Fri Oct 23 2026 OpenChamber COPR <noreply@github.com> - 2.5.1-1
- Update web CLI to v2.5.1 and bundle Node.js 24.22.1 security release

* Fri Oct 23 2026 OpenChamber COPR <noreply@github.com> - 2.5.0-2
- Bundle Node.js 24.22.1 security release

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
