%global commit 30e87664829782811a765b0ca9eea3a878a7ff29
%global date 20250627
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global debug_package %{nil}

Name:           ipu6-camera-bins
Summary:        Proprietary image processing libraries for MIPI cameras through the Intel IPU6
Version:        0
Release:        5.%{date}git%{shortcommit}%{?dist}
License:        Proprietary
URL:            https://github.com/intel/ipu6-camera-bins
ExclusiveArch:  x86_64

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  chrpath

Requires:       intel-vsc-firmware

%description
This provides the necessary binaries for Intel IPU6, including library and
firmware. It supports MIPI cameras through the IPU6 on Intel Tiger Lake, Alder
Lake, Raptor Lake and Meteor Lake platforms.

%package devel
Summary:        IPU6 header files for development.
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This provides the necessary header files for IPU6 development.

%prep
%autosetup -n %{name}-%{commit}
chrpath --delete lib/*.so.*
sed -i \
    -e "s|libdir=\${exec_prefix}/lib|libdir=\${prefix}/%{_lib}|g" \
    lib/pkgconfig/*.pc

%install
mkdir -p %{buildroot}%{_includedir}/
mkdir -p %{buildroot}%{_libdir}/
cp -pr include/* %{buildroot}%{_includedir}/
cp -pr lib/lib* lib/pkgconfig %{buildroot}%{_libdir}/
chmod 755 %{buildroot}%{_libdir}/$target/*.so*

for lib in %{buildroot}%{_libdir}/lib*.so.*; do \
  lib=${lib##*/}; \
  ln -s $lib %{buildroot}%{_libdir}/${lib%.*}; \
done

%files
%license LICENSE
%doc README.md SECURITY.md
%{_libdir}/*.so*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
* Fri Jun 27 2025 Simone Caronni <negativo17@gmail.com> - 0-5.20250627git30e8766
- Update to latest snapshot.

* Sun Oct 27 2024 Simone Caronni <negativo17@gmail.com> - 0-4.20240929git98ca6f2
- Update to latest snapshot. Unified build.

* Tue Aug 06 2024 Simone Caronni <negativo17@gmail.com> - 0-3.20240719git532cb2b
- Update to latest snapshot.

* Mon May 13 2024 Simone Caronni <negativo17@gmail.com> - 0-2.20240507git987b09a
- Update to latest snapshot.

* Mon May 06 2024 Simone Caronni <negativo17@gmail.com> - 0.0-1.20240411gitf073cb6
- First build.
