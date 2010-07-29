# enable_gtkdoc: Toggle if gtk-doc files should be rebuilt.
#      0 = no
#      1 = yes
%define enable_gtkdoc 1

# enable_tests: Run test suite in build
#      0 = no
#      1 = yes
%define enable_tests 0

%{?_without_gtkdoc: %{expand: %%define enable_gtkdoc 0}}
%{?_without_tests: %{expand: %%define enable_tests 0}}

%{?_with_gtkdoc: %{expand: %%define enable_gtkdoc 1}}
%{?_with_tests: %{expand: %%define enable_tests 1}}


# required version of various libraries
%define req_glib_version		2.25.9

%define pkgname			gdk-pixbuf
%define api_version		2.0
%define binary_version	2.10
%define lib_major		0

%define libname  %mklibname gdk_pixbuf %{api_version} %{lib_major}
%define develname	%mklibname -d gdk_pixbuf %api_version

Summary:	Image loading and manipulation library for GTK+
Name:		%{pkgname}%{api_version}
Version:	2.21.6
Release:        %mkrel 2
License:	LGPLv2+
Group:		System/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%pkgname/%{pkgname}-%{version}.tar.bz2
Patch0:		0001-Fix-linking-when-libpng-loader-is-builtin.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

URL:		http://www.gtk.org
Requires:	common-licenses
BuildRequires:	gettext-devel
BuildRequires:  libglib2.0-devel >= %{req_glib_version}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:  gobject-introspection-devel >= 0.9.0
BuildRequires:  jasper-devel
%if %enable_tests
BuildRequires:  x11-server-xvfb
%endif
%if %enable_gtkdoc
BuildRequires: gtk-doc >= 0.9 
BuildRequires: sgml-tools
BuildRequires: texinfo
%endif
# gw tests will fail without this
BuildRequires: fonts-ttf-dejavu
Requires: %{libname} = %{version}
Conflicts: gtk+2.0 < 2.21.3

%description
This package contains libraries used by GTK+ to load and handle
various image formats.

%package -n %{libname}
Summary:	Image loading and manipulation library for GTK+
Group:		System/Libraries
Provides:	libgdk_pixbuf%{api_version} = %{version}-%{release}
Requires(post):		libtiff >= 3.6.1
Conflicts: gir-repository < 0.6.5-4
Requires(post): %name >= %version
Requires: %name >= %version

%description -n %{libname}
This package contains libraries used by GTK+ to load and handle
various image formats.

%package -n %{develname}
Summary:	Development files for image handling library for GTK+
Group:		Development/GNOME and GTK+
Provides:	libgdk_pixbuf%{api_version}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Requires:	libglib2.0-devel >= %{req_glib_version}
Obsoletes:	%mklibname -d gdk_pixbuf %api_version %lib_major

%description -n %{develname}
This package contains the development files needed to compile programs
that uses GTK+ image loading/manipulation library.


%prep
%setup -n %{pkgname}-%{version} -q
%patch0 -p1

%build
autoreconf -fi
%ifarch ppc64
export CFLAGS="$RPM_OPT_FLAGS -mminimal-toc"
%endif

# fix crash in nautilus (GNOME bug #596977)
export CFLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-fomit-frame-pointer//g'`

#CONFIGURE_TOP=.. 
export CPPFLAGS="-DGTK_COMPILATION"
%configure2_5x --with-included-loaders=png \
%if !%enable_gtkdoc
	--enable-gtk-doc=no
%endif

%make

%check
%if %enable_tests
xvfb-run make check
%endif

%install
rm -rf $RPM_BUILD_ROOT %pkgname.lang
%makeinstall_std RUN_QUERY_LOADER_TEST=false

touch $RPM_BUILD_ROOT%_libdir/%pkgname-%{api_version}/%{binary_version}.0/loaders.cache

# handle biarch packages
progs="gdk-pixbuf-query-loaders"
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%pkgname-%{api_version}/bin
for f in $progs; do
  mv -f $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_libdir}/%pkgname-%{api_version}/bin/
  cat > $RPM_BUILD_ROOT%{_bindir}/$f << EOF
#!/bin/sh
lib=%{_lib}
case ":\$1:" in
:lib*:) lib="\$1"; shift 1;;
esac
exec %{_prefix}/\$lib/%pkgname-%{api_version}/bin/$f \${1+"\$@"}
EOF
  chmod +x $RPM_BUILD_ROOT%{_bindir}/$f
done

#remove not packaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/%pkgname-%{api_version}/*/loaders/*.la

%find_lang %pkgname

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname}

if [ "$1" = "2" ]; then
  if [ -f %_libdir/%pkgname-%api_version/2.10.0/loaders.cache ]; then
    rm -f %_libdir/%pkgname-%api_version/2.10.0/loaders.cache
  fi
fi

%{_libdir}/%pkgname-%{api_version}/bin/gdk-pixbuf-query-loaders --update-cache


%files -f %pkgname.lang
%defattr(-, root, root)
%doc README
%{_bindir}/gdk-pixbuf-query-loaders
%_mandir/man1/gdk-pixbuf-query-loaders.1*

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/libgdk_pixbuf*.so.*
%_libdir/girepository-1.0/GdkPixbuf-2.0.typelib
%dir %{_libdir}/%pkgname-%{api_version}/%{binary_version}.*/loaders
%{_libdir}/%pkgname-%{api_version}/%{binary_version}.*/loaders/*.so
%{_libdir}/%pkgname-%{api_version}/bin/gdk-pixbuf-query-loaders
%ghost %verify (not md5 mtime size) %{_libdir}/%pkgname-%{api_version}/%{binary_version}.*/loaders.cache

%files -n %{develname}
%defattr(-, root, root)
%doc %{_datadir}/gtk-doc/html/gdk-pixbuf
%_bindir/gdk-pixbuf-csource
%{_includedir}/%pkgname-%api_version
%_datadir/gir-1.0/GdkPixbuf-2.0.gir
%{_libdir}/libgdk_pixbuf*.so
%attr(644,root,root) %{_libdir}/libgdk_pixbuf*.la
%{_libdir}/pkgconfig/gdk-pixbuf*.pc
%_mandir/man1/gdk-pixbuf-csource.1*
