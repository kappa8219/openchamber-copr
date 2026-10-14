%global debug_package %{nil}
%global __requires_exclude_from ^/opt/OpenChamber/resources/app\.asar\.unpacked/.*$
%global __strip /bin/true

Name:           openchamber
Version:        2.3.2
Release:        5%{?dist}
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
echo "9173183b2c7d2b83568255879f6952866607c5befe93a9c2f9102f30cb931f43  %{SOURCE0}" | sha256sum --check

%install
rpm2cpio %{SOURCE0} | cpio --extract --make-directories --quiet --directory %{buildroot}
find %{buildroot} -mindepth 1 -printf '/%%P\n' | sort > %{name}.files

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/openchamber.desktop

%files -f %{name}.files

%changelog
