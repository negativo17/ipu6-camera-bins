%global commit 814c869910fe8d794425385c5710650716cd24eb
%global date 20240411
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global debug_package %{nil}

Name:           ipu6-camera-bins
Summary:        Proprietary image processing libraries for MIPI cameras through the Intel IPU6
Version:        0
Release:        1.%{date}git%{shortcommit}%{?dist}
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
%setup -q -n %{name}-%{commit}
for target in ipu_tgl ipu_adl ipu_mtl; do
  chrpath --delete lib/$target/*.so
  sed -i \
    -e "s|libdir=\${prefix}/lib|libdir=\${prefix}/%{_lib}|g" \
    lib/$target/pkgconfig/*.pc
done

%install
mkdir -p %{buildroot}%{_includedir}
for target in ipu_tgl ipu_adl ipu_mtl; do
  mkdir -p %{buildroot}%{_libdir}/$target
  cp -pr include/$target %{buildroot}%{_includedir}
  cp -pr lib/$target/lib* lib/$target/pkgconfig %{buildroot}%{_libdir}/$target
  chmod 755 %{buildroot}%{_libdir}/$target/*.so*
done

%files
%dir %{_libdir}/ipu_tgl
%dir %{_libdir}/ipu_adl
%dir %{_libdir}/ipu_mtl
%{_libdir}/ipu_tgl/*.so*
%{_libdir}/ipu_adl/*.so*
%{_libdir}/ipu_mtl/*.so*

%files devel
%dir %{_includedir}/ipu_tgl
%dir %{_includedir}/ipu_adl
%dir %{_includedir}/ipu_mtl
%dir %{_libdir}/ipu_tgl/pkgconfig
%dir %{_libdir}/ipu_adl/pkgconfig
%dir %{_libdir}/ipu_mtl/pkgconfig
%{_includedir}/ipu_tgl/*
%{_includedir}/ipu_adl/*
%{_includedir}/ipu_mtl/*
%{_libdir}/ipu_tgl/pkgconfig/*
%{_libdir}/ipu_adl/pkgconfig/*
%{_libdir}/ipu_mtl/pkgconfig/*
%{_libdir}/ipu_tgl/*.a
%{_libdir}/ipu_adl/*.a
%{_libdir}/ipu_mtl/*.a

%changelog
* Mon May 06 2024 Simone Caronni <negativo17@gmail.com> - 0.0-1.20240411gitf073cb6
- First build.
