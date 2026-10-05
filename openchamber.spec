%global debug_package %{nil}
%global bun_version 1.4.2

Name:           openchamber
Version:        2.1.1
Release:        1%{?dist}
Summary:        Desktop runtime for OpenChamber
License:        MIT
URL:            https://openchamber.dev/
Source0:        https://github.com/openchamber/openchamber/archive/refs/tags/v%{version}.tar.gz
Source1:        https://github.com/oven-sh/bun/releases/download/bun-v%{bun_version}/bun-linux-x64.zip
ExclusiveArch:  x86_64

BuildRequires:  cpio
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  nodejs
BuildRequires:  npm
BuildRequires:  python3
BuildRequires:  rpm
BuildRequires:  unzip

%description
OpenChamber is an open-source desktop client for OpenCode.

%prep
%autosetup -n openchamber-%{version}

%build
export HOME="%{_builddir}/home"
export npm_config_cache="%{_builddir}/npm-cache"
export ELECTRON_BUILDER_CACHE="%{_builddir}/electron-builder-cache"
export NODE_OPTIONS="--max-old-space-size=4096"
mkdir -p "$HOME" "$npm_config_cache" "$ELECTRON_BUILDER_CACHE"
unzip -q %{SOURCE1}
export PATH="$PWD/bun-linux-x64:$PATH"
bun --version
bun install --frozen-lockfile
bun run build
bun run --cwd packages/electron package -- --linux rpm --x64

%install
mkdir -p "%{buildroot}"
rpm2cpio packages/electron/dist/OpenChamber-%{version}-x86_64.rpm | (
    cd "%{buildroot}"
    cpio -idm
)
find "%{buildroot}" -mindepth 1 -printf '/%%P\n' | sort > %{name}.files

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/openchamber.desktop

%files -f %{name}.files

%changelog
