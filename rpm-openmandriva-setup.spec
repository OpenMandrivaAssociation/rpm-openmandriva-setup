Name:		rpm-openmandriva-setup
Version:	0.1.2
Release:	1
Group:		System/Configuration/Packaging
Summary:	Macros and scripts for OpenMandriva specific rpm behavior
License:	MIT
URL:		https://github.com/OpenMandrivaSoftware/rpm-openmandriva-setup
Source0:	https://github.com/OpenMandrivaSoftware/rpm-openmandriva-setup/archive/%{name}-%{version}.tar.gz
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
find . -type f -o -type l |sed -e 's,^\.,%%{_usrlibrpm},' >../user.filelist
cd ../build
find . -type f -o -type l |sed -e 's,^\.,%%{_usrlibrpm},' >../build.filelist

%install
mkdir -p %{buildroot}%{_usrlibrpm}
cp -a user/* build/* %{buildroot}%{_usrlibrpm}

%files -f user.filelist
%dir %{_usrlibrpm}/platform
%dir %{_usrlibrpm}/platform/*

%files build -f build.filelist
