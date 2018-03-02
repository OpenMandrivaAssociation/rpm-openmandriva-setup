# For transitioning from rpm5
%{!?_rpmconfigdir: %define _rpmconfigdir /usr/lib/rpm}

Name:		rpm-openmandriva-setup
Version:	0.2.3
Release:	1
Group:		System/Configuration/Packaging
Summary:	Macros and scripts for OpenMandriva specific rpm behavior
License:	MIT
URL:		https://github.com/OpenMandrivaSoftware/rpm-openmandriva-setup
Source0:	https://github.com/OpenMandrivaSoftware/rpm-openmandriva-setup/archive/%{version}/%{name}-%{version}.tar.gz
Requires:	rpm >= 2:4.14.0-0
BuildArch:	noarch

%description
Macros and scripts for OpenMandriva specific rpm behavior.

%package build
Summary:	Macros and scripts for OpenMandriva specific rpmbuild behavior
Group:		System/Configuration/Packaging
Requires:	rpm-build >= 2:4.14.0-0
Requires:	%{name} = %{EVRD}

%description build
Macros and scripts for OpenMandriva specific rpmbuild behavior.

%prep
%setup -q

%build
cd user
find . -type f -o -type l |sed -e 's,^\.,%%{_rpmconfigdir},' >../user.filelist
cd ../build
find . -type f -o -type l |sed -e 's,^\.,%%{_rpmconfigdir},' >../build.filelist

%install
mkdir -p %{buildroot}%{_rpmconfigdir}
cp -a user/* build/* %{buildroot}%{_rpmconfigdir}

%files -f user.filelist
# We should own this directory
%dir %{_rpmconfigdir}/openmandriva

%files build -f build.filelist
