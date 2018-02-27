# For transitioning from rpm5
%if "%_rpmconfigdir" == "%%_rpmconfigdir"
%define _rpmconfigdir /usr/lib/rpm
%endif

Name:		rpm-openmandriva-setup
Version:	0.1.99a
Release:	1
Group:		System/Configuration/Packaging
Summary:	Macros and scripts for OpenMandriva specific rpm behavior
License:	MIT
URL:		https://github.com/OpenMandrivaSoftware/rpm-openmandriva-setup
Source0:	https://github.com/OpenMandrivaSoftware/rpm-openmandriva-setup/archive/%{version}.tar.gz
Requires:	rpm
BuildArch:	noarch

%description
Macros and scripts for OpenMandriva specific rpm behavior.

%package build
Summary:	Macros and scripts for OpenMandriva specific rpmbuild behavior
Group:		System/Configuration/Packaging
Requires:	rpm-build
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
install -D -m 644 macros.openmandriva %{buildroot}%{_rpmconfigdir}/openmandriva/macros

%files -f user.filelist
%dir %{_rpmconfigdir}/platform
%dir %{_rpmconfigdir}/platform/*
%{_rpmconfigdir}/openmandriva/macros

%files build -f build.filelist
