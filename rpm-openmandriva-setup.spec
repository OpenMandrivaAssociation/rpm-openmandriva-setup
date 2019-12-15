# For transitioning from rpm5
%{!?_rpmconfigdir: %define _rpmconfigdir /usr/lib/rpm}

Name:		rpm-openmandriva-setup
Version:	0.4.0
Release:	2
Group:		System/Configuration/Packaging
Summary:	Macros and scripts for OpenMandriva specific rpm behavior
License:	MIT
URL:		https://github.com/OpenMandrivaSoftware/rpm-openmandriva-setup
Source0:	https://github.com/OpenMandrivaSoftware/rpm-openmandriva-setup/archive/%{version}/%{name}-%{version}.tar.gz
# need to disable lto due to mess with autotools
Patch0:		disable_lto-riscv64.patch
Requires:	rpm >= 2:4.14.2-0
Recommends:	systemd-macros
BuildArch:	noarch
# Forge handling macros
# (From: https://src.fedoraproject.org/rpms/redhat-rpm-config/tree):
Source8:	forge.lua
Source9:	macros.forge
Source10:	common.lua

%description
Macros and scripts for OpenMandriva specific rpm behavior.

%package build
Summary:	Macros and scripts for OpenMandriva specific rpmbuild behavior
Group:		System/Configuration/Packaging
Requires:	rpm-build >= 2:4.14.0-0
# (tpg) do not use %%EVRD here, as it does not exist yet
Requires:	%{name} = %{version}-%{release}
# Required for package builds to work
Requires:	dwz
Requires:	rpmlint
Requires:	rpmlint-openmandriva-policy
Requires:	spec-helper >= 0.31.12
Requires:	binutils
Requires:	systemd-macros
Requires:	go-srpm-macros
Requires:	rpm-helper
# Ensure this exists in the build environment
Requires:	/usr/bin/gdb-add-index

%description build
Macros and scripts for OpenMandriva specific rpmbuild behavior.

%prep
%setup -q
%ifarch riscv64
%patch0 -p1
%endif

%build
cd user
find . -type f -o -type l |sed -e 's,^\.,%%{_rpmconfigdir},' >../user.filelist
cd ../build
find . -type f -o -type l |sed -e 's,^\.,%%{_rpmconfigdir},' >../build.filelist

%install
mkdir -p %{buildroot}%{_rpmconfigdir}
cp -a user/* build/* %{buildroot}%{_rpmconfigdir}

install -D %{S:9} -m 0644 %{buildroot}%{_rpmconfigdir}/macros.d/
mkdir -p %{buildroot}%{_rpmluadir}/fedora/srpm
install -D %{S:10} %{buildroot}%{_rpmluadir}/fedora
install -D %{S:8} %{buildroot}%{_rpmluadir}/fedora/srpm


%files -f user.filelist
# We should own this directory
%dir %{_rpmconfigdir}/openmandriva

%files build -f build.filelist
%{_rpmluadir}/fedora/common.lua
%{_rpmluadir}/fedora/srpm/forge.lua
%{_rpmconfigdir}/macros.d/macros.forge
