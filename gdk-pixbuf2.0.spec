%define enable_gtkdoc 0
%define enable_tests 0
%define _disable_ld_as_needed	1

%define oname		gdk_pixbuf
%define pkgname		gdk-pixbuf
%define api_version	2.0
%define binary_version	2.10.0
%define major		0
%define girmajor	2.0

%define libname		%mklibname %{oname} %{api_version} %{major}
%define xlibname	%mklibname %{oname}_xlib %{api_version} %{major}
%define develname	%mklibname -d %{oname} %{api_version}
%define develxlib	%mklibname -d %{oname}_xlib %{api_version}
%define girname		%mklibname %{oname}-gir %{girmajor}

Summary:	Image loading and manipulation library for GTK+
Name:		%{pkgname}%{api_version}
Version:	2.26.5
Release:	1
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.gtk.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gdk-pixbuf/2.26/%{pkgname}-%{version}.tar.xz

BuildRequires:	gettext-devel
BuildRequires:	jasper-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(x11)
%if %enable_tests
BuildRequires:	x11-server-xvfb
# gw tests will fail without this
BuildRequires:	fonts-ttf-dejavu
%endif
%if %enable_gtkdoc
BuildRequires:	gtk-doc >= 0.9
BuildRequires:	sgml-tools
BuildRequires:	texinfo
%endif
Requires:	common-licenses
Conflicts:	gtk+2.0 < 2.21.3
Conflicts:	%{_lib}gdk_pixbuf2.0_0 < 2.24.0-6

%description
This package contains libraries used by GTK+ to load and handle
various image formats.

%package -n %{libname}
Summary:	Image loading and manipulation library for GTK+
Group:		System/Libraries
Provides:	lib%{oname}%{api_version} = %{version}-%{release}

%description -n %{libname}
This package contains libraries used by GTK+ to load and handle
various image formats.

%package -n %{xlibname}
Summary:	Image loading and manipulation library for GTK+
Group:		System/Libraries

%description -n %{xlibname}
This package contains libraries used by GTK+ to load and handle
various image formats.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	gir-repository < 0.6.5-4

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{develname}
Summary:	Development files for image handling library for GTK+
Group:		Development/GNOME and GTK+
Provides:	lib%{oname}%{api_version}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires: 	%{name} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Obsoletes:	%{_lib}gdk_pixbuf2.0_0-devel < 2.26

%description -n %{develname}
This package contains the development files needed to compile programs
that uses GTK+ image loading/manipulation library.

%package -n %{develxlib}
Summary:	Development files for image handling library for GTK+ - Xlib
Group:		Development/GNOME and GTK+
Provides:	lib%{oname}_xlib%{api_version}-devel = %{version}-%{release}
Requires:	%{xlibname} = %{version}-%{release}

%description -n %{develxlib}
This package contains the development files needed to compile programs
that uses GTK+ image loading/manipulation Xlib library.

%prep
%setup -qn %{pkgname}-%{version}

%build
# fix crash in nautilus (GNOME bug #596977)
export CFLAGS=`echo %{optflags} | sed -e 's/-fomit-frame-pointer//g'`

#CONFIGURE_TOP=..
export CPPFLAGS="-DGTK_COMPILATION"
%configure2_5x \
	--with-libjasper --with-x11 \
%if !%{enable_gtkdoc}
	--enable-gtk-doc=no
%endif

%make

%if %enable_tests
%check
xvfb-run make check
%endif

%install
rm -rf %{buildroot} %{pkgname}.lang
%makeinstall_std RUN_QUERY_LOADER_TEST=false

touch %{buildroot}%{_libdir}/%{pkgname}-%{api_version}/%{binary_version}/loaders.cache

# handle biarch packages
progs="gdk-pixbuf-query-loaders"
mkdir -p %{buildroot}%{_libdir}/%{pkgname}-%{api_version}/bin
for f in $progs; do
  mv -f %{buildroot}%{_bindir}/$f %{buildroot}%{_libdir}/%{pkgname}-%{api_version}/bin/
  cat > %{buildroot}%{_bindir}/$f << EOF
#!/bin/sh
lib=%{_lib}
case ":\$1:" in
:lib*:) lib="\$1"; shift 1;;
esac
exec %{_prefix}/\$lib/%{pkgname}-%{api_version}/bin/$f \${1+"\$@"}
EOF
  chmod +x %{buildroot}%{_bindir}/$f
done

#remove not packaged files
find %{buildroot} -name *.la | xargs rm

%find_lang %{pkgname}

%post
if [ "$1" = "2" ]; then
  if [ -f %{_libdir}/%{pkgname}-%{api_version}/%{binary_version}/loaders.cache ]; then
    rm -f %{_libdir}/%{pkgname}-%{api_version}/%{binary_version}/loaders.cache
  fi
fi
%{_libdir}/%{pkgname}-%{api_version}/bin/gdk-pixbuf-query-loaders --update-cache

%triggerin -- %{_libdir}/gdk-pixbuf-%{api_version}/%{binary_version}/loaders/*.so
%{_libdir}/%{pkgname}-%{api_version}/bin/gdk-pixbuf-query-loaders --update-cache

%triggerpostun -- %{_libdir}/gdk-pixbuf-%{api_version}/%{binary_version}/loaders/*.so
if [ -x %{_bindir}/gdk-pixbuf-query-loaders ]; then
%{_libdir}/%{pkgname}-%{api_version}/bin/gdk-pixbuf-query-loaders --update-cache
fi

%files -f %{pkgname}.lang
%doc README
%{_bindir}/gdk-pixbuf-query-loaders
%dir %{_libdir}/%{pkgname}-%{api_version}/%{binary_version}/loaders
%{_libdir}/%{pkgname}-%{api_version}/%{binary_version}/loaders/*.so
%{_libdir}/%{pkgname}-%{api_version}/bin/gdk-pixbuf-query-loaders
%ghost %verify (not md5 mtime size) %{_libdir}/%{pkgname}-%{api_version}/%{binary_version}/loaders.cache
%{_mandir}/man1/gdk-pixbuf-query-loaders.1*

%files -n %{libname}
%{_libdir}/libgdk_pixbuf-%{api_version}.so.%{major}*

%files -n %{xlibname}
%{_libdir}/libgdk_pixbuf_xlib-%{api_version}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/GdkPixbuf-%{girmajor}.typelib

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/gdk-pixbuf
%{_bindir}/gdk-pixbuf-csource
%{_bindir}/gdk-pixbuf-pixdata
%{_libdir}/libgdk_pixbuf-%{api_version}.so
%{_includedir}/%{pkgname}-%{api_version}/%{pkgname}/
%{_libdir}/pkgconfig/gdk-pixbuf-%{api_version}.pc
%{_datadir}/gir-1.0/GdkPixbuf-%{api_version}.gir
%{_mandir}/man1/gdk-pixbuf-csource.1*

%files -n %{develxlib}
%{_libdir}/libgdk_pixbuf_xlib-%{api_version}.so
%{_includedir}/%{pkgname}-%{api_version}/%{pkgname}-xlib/
%{_libdir}/pkgconfig/gdk-pixbuf-xlib-%{api_version}.pc

