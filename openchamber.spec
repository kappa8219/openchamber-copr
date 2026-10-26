%global debug_package %{nil}
%global __requires_exclude_from ^/opt/OpenChamber/resources/app\.asar\.unpacked/.*$
%global __strip /bin/true

Name:           openchamber
Version:        2.5.2
Release:        1%{?dist}
Summary:        Desktop runtime for OpenChamber
License:        MIT
URL:            https://openchamber.dev/
Source0:        https://github.com/openchamber/openchamber/releases/download/v%{version}/OpenChamber-%{version}-linux-x86_64.rpm
ExclusiveArch:  x86_64

BuildRequires:  cpio
BuildRequires:  desktop-file-utils
BuildRequires:  rpm

%description
OpenChamber desktop application, repackaged from the official upstream RPM.

%prep
echo "beb15dabf04e0d4a88c5a6bc725b6056e8748e6ecaf89ae893272f32a6bd99a8  %{SOURCE0}" | sha256sum --check

%install
export QA_RPATHS=0x12
rpm2cpio %{SOURCE0} | cpio --extract --make-directories --quiet --directory %{buildroot}
find %{buildroot} -mindepth 1 \( -type f -o -type l \) -printf '/%%P\n' | sort > %{name}.files

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/openchamber.desktop

%files -f %{name}.files

%changelog
* Mon Oct 26 2026 OpenChamber COPR <noreply@github.com> - 2.5.2-1
- Update to OpenChamber 2.5.2

* Fri Oct 23 2026 OpenChamber COPR <noreply@github.com> - 2.5.1-1
- Update to OpenChamber 2.5.1

* Tue Oct 20 2026 OpenChamber COPR <noreply@github.com> - 2.5.0-1
- Update to OpenChamber 2.5.0

* Mon Oct 19 2026 OpenChamber COPR <noreply@github.com> - 2.4.0-1
- Update to OpenChamber 2.4.0

* Thu Oct 15 2026 OpenChamber COPR <noreply@github.com> - 2.3.3-1
- Repackage the official upstream desktop RPM

* Wed Oct 14 2026 OpenChamber COPR <noreply@github.com> - 2.3.2-2
- Exclude shared system directories from the package file list

* Wed Oct 14 2026 OpenChamber COPR <noreply@github.com> - 2.3.2-1
- Repackage the official upstream desktop RPM

* Tue Oct 13 2026 OK <o.kraievyi@gmail.com> - 2.3.1-1
- Update to 2.3.1
- Mobile: start a session from Shortcuts and Siri on iOS 18
- Antigravity card with 5-hour and weekly limits
- "View repository on GitHub/GitLab" in repository menu
- Configure panels: drag to reorder in the rail
- Fix mobile connect/drop/reconnect loop on slow servers
- Fix GitHub PR actions in unlinked repositories
- Many other fixes and improvements
