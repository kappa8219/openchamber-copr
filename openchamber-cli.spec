%global debug_package %{nil}
%global __strip /bin/true
%global __provides_exclude_from ^/usr/lib/openchamber-web/node_modules/.*$
%global __requires_exclude_from ^/usr/lib/openchamber-web/node_modules/.*$
%global __requires_exclude ^/usr/bin/(pwsh|python3)$

Name:           openchamber-cli
Version:        2.8.1
Release:        1%{?dist}
Summary:        OpenChamber Web Server and CLI
License:        MIT
URL:            https://openchamber.dev/
Source0:        https://github.com/openchamber/openchamber/releases/download/v%{version}/openchamber-web-%{version}.tgz
Source1:        LICENSE-%{version}
ExclusiveArch:  x86_64

Requires:       nodejs24

BuildRequires:  tar
BuildRequires:  nodejs24
BuildRequires:  nodejs24-npm

%description
OpenChamber Web Server and CLI for running OpenChamber on a workstation or
server. This package provides the openchamber-cli command, including API-only and
LAN server modes. It runs on the system Node.js 24 (nodejs24 package); since
OpenChamber 2.8.1 the web package bundles its own OpenCode server, so no
separate OpenCode installation is required.

%prep
echo "07c248f9779dbf02cd91b9ed2728291a3885e02af7eacfa8303ed80c131398ae  %{SOURCE0}" | sha256sum --check
mkdir -p package
tar -xzf %{SOURCE0} --strip-components=1 -C package

%build
cd package
npm install --omit=dev --ignore-scripts --no-audit --no-fund

%install
export QA_RPATHS=0x12
mkdir -p %{buildroot}%{_prefix}/lib/openchamber-web
mkdir -p %{buildroot}%{_bindir}
cp -a package/. %{buildroot}%{_prefix}/lib/openchamber-web/
install -Dpm 0644 %{SOURCE1} \
    %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

cat > %{buildroot}%{_bindir}/openchamber-cli <<'EOF'
#!/bin/sh
exec /usr/bin/node-24 /usr/lib/openchamber-web/build/bin/cli.js "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/openchamber-cli

find %{buildroot} -mindepth 1 \( -type f -o -type l \) \
    ! -path '%{buildroot}%{_datadir}/licenses/%{name}/LICENSE' \
    -printf '/%%P\n' | sort -u > %{name}.files

%check
node-24 --version
node-24 %{buildroot}%{_prefix}/lib/openchamber-web/build/bin/cli.js --version | grep -Fx '%{version}'
node-24 %{buildroot}%{_prefix}/lib/openchamber-web/build/bin/cli.js --help >/dev/null

%files -f %{name}.files
%license %{_datadir}/licenses/%{name}/LICENSE

%changelog
* Fri Nov 27 2026 OpenChamber COPR <noreply@github.com> - 2.8.1-1
- Update web CLI to v2.8.1
- Drop the bundled Node.js tarball; require Fedora's nodejs24 (Node.js 24.14+)
- The web tarball bundles its own OpenCode server since 2.8.1, so no
  separate OpenCode installation is needed

* Sun Nov 22 2026 OpenChamber COPR <noreply@github.com> - 2.8.0-1
- Update web CLI to v2.8.0; keep bundled Node.js 24.22.3

* Fri Nov 20 2026 OpenChamber COPR <noreply@github.com> - 2.7.3-1
- Update web CLI to v2.7.3, use build/bin/cli.js, and keep bundled Node.js 24.22.3

* Mon Nov 16 2026 OpenChamber COPR <noreply@github.com> - 2.7.2-1
- Update web CLI to v2.7.2; keep bundled Node.js 24.22.3

* Fri Nov 13 2026 OpenChamber COPR <noreply@github.com> - 2.7.1-1
- Update web CLI to v2.7.1; keep bundled Node.js 24.22.3
+
 * Thu Nov 12 2026 OpenChamber COPR <noreply@github.com> - 2.7.0-2
- Bundle Node.js 24.22.3 security release
+
 * Mon Nov 09 2026 OpenChamber COPR <noreply@github.com> - 2.7.0-1
- Update web CLI to v2.7.0

* Wed Nov 04 2026 OpenChamber COPR <noreply@github.com> - 2.6.1-1
- Update web CLI to v2.6.1

* Mon Nov 02 2026 OpenChamber COPR <noreply@github.com> - 2.6.0-1
- Update web CLI to v2.6.0

* Mon Oct 26 2026 OpenChamber COPR <noreply@github.com> - 2.5.2-1
- Update web CLI to v2.5.2

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
