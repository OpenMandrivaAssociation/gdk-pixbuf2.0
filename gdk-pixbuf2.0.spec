%define enable_gtkdoc 0
%define enable_tests 0
%define _disable_ld_as_needed	1
%define _disable_rebuild_configure 1

%define oname gdk_pixbuf
%define pkgname gdk-pixbuf
%define binver 2.10.0
%define api 2.0
%define major 0

%define libname %mklibname %{oname} %{api} %{major}
%define xlibname %mklibname %{oname}_xlib %{api} %{major}
%define devname %mklibname -d %{oname} %{api}
%define devxlib %mklibname -d %{oname}_xlib %{api}
%define girname %mklibname %{oname}-gir %{api}
%bcond_with bootstrap

Summary:	Image loading and manipulation library for GTK+
Name:		%{pkgname}%{api}
Version:	2.38.0
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gtk.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gdk-pixbuf/%(echo %{version} |cut -d. -f1-2)/%{pkgname}-%{version}.tar.xz
BuildRequires:	meson
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(shared-mime-info)
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
Requires:	shared-mime-info
Conflicts:	gtk+2.0 < 2.21.3
Conflicts:	%{_lib}gdk_pixbuf2.0_0 < 2.24.0-6

%description
This package contains libraries used by GTK+ to load and handle
various image formats.

%package -n %{libname}
Summary:	Image loading and manipulation library for GTK+
Group:		System/Libraries
Provides:	lib%{oname}%{api} = %{version}-%{release}

%description -n %{libname}
This package contains libraries used by GTK+ to load and handle
various image formats.

%package -n %{xlibname}
Summary:	Image loading and manipulation library for GTK+
Group:		System/Libraries

%description -n %{xlibname}
This package contains libraries used by GTK+ to load and handle
various image formats.

%if !%{with bootstrap}
%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.
%endif

%package -n %{devname}
Summary:	Development files for image handling library for GTK+
Group:		Development/GNOME and GTK+
Provides:	%{oname}%{api}-devel = %{version}-%{release}
Requires: 	%{name} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
%if !%{with bootstrap}
Requires:	%{girname} = %{version}-%{release}
%endif
Obsoletes:	%{_lib}gdk_pixbuf2.0_0-devel < 2.26

%description -n %{devname}
This package contains the development files needed to compile programs
that uses GTK+ image loading/manipulation library.

%package -n %{devxlib}
Summary:	Development files for image handling library for GTK+ - Xlib
Group:		Development/GNOME and GTK+
Provides:	%{oname}_xlib%{api}-devel = %{version}-%{release}
Requires:	%{xlibname} = %{version}-%{release}

%description -n %{devxlib}
This package contains the development files needed to compile programs
that uses GTK+ image loading/manipulation Xlib library.

%prep
%autosetup -n %{pkgname}-%{version} -p1

# fix crash in nautilus (GNOME bug #596977)
export CFLAGS=$(echo %{optflags} | sed -e 's/-fomit-frame-pointer//g')

%meson \
	-Djasper=true \
	-Dbuiltin_loaders=none \
%if %{with bootstrap}
	-Dman=false \
	-Dgir=false \
%endif
%if !%{enable_gtkdoc}
	-Ddocs=false \
%endif
	-Dinstalled_tests=false

%build
%meson_build

%if %enable_tests
%check
xvfb-run %meson_test
%endif

%install
%meson_install

touch %{buildroot}%{_libdir}/%{pkgname}-%{api}/%{binver}/loaders.cache

# handle biarch packages
progs="gdk-pixbuf-query-loaders"
mkdir -p %{buildroot}%{_libdir}/%{pkgname}-%{api}/bin
for f in $progs; do
  mv -f %{buildroot}%{_bindir}/$f %{buildroot}%{_libdir}/%{pkgname}-%{api}/bin/
  cat > %{buildroot}%{_bindir}/$f << EOF
#!/bin/sh
lib=%{_lib}
case ":\$1:" in
:lib*:) lib="\$1"; shift 1;;
esac
exec %{_prefix}/\$lib/%{pkgname}-%{api}/bin/$f \${1+"\$@"}
EOF
  chmod +x %{buildroot}%{_bindir}/$f
done

%find_lang %{pkgname}

%post
if [ "$1" = "2" ]; then
    if [ -f %{_libdir}/%{pkgname}-%{api}/%{binver}/loaders.cache ]; then
	rm -f %{_libdir}/%{pkgname}-%{api}/%{binver}/loaders.cache
    fi
fi
%{_libdir}/%{pkgname}-%{api}/bin/gdk-pixbuf-query-loaders --update-cache

%transfiletriggerin -- %{_libdir}/gdk-pixbuf-%{api}/%{binver}/loaders/
%{_libdir}/%{pkgname}-%{api}/bin/gdk-pixbuf-query-loaders --update-cache

%transfiletriggerpostun -- %{_libdir}/gdk-pixbuf-%{api}/%{binver}/loaders/
if [ -x %{_bindir}/gdk-pixbuf-query-loaders ]; then
    %{_libdir}/%{pkgname}-%{api}/bin/gdk-pixbuf-query-loaders --update-cache
fi

%files -f %{pkgname}.lang
%doc README
%{_bindir}/gdk-pixbuf-query-loaders
%{_bindir}/gdk-pixbuf-thumbnailer
%dir %{_libdir}/%{pkgname}-%{api}/%{binver}/loaders
%{_libdir}/%{pkgname}-%{api}/%{binver}/loaders/*.so
%{_libdir}/%{pkgname}-%{api}/bin/gdk-pixbuf-query-loaders
%ghost %verify (not md5 mtime size) %{_libdir}/%{pkgname}-%{api}/%{binver}/loaders.cache
%{_datadir}/thumbnailers/gdk-pixbuf-thumbnailer.thumbnailer
%{_mandir}/man1/gdk-pixbuf-query-loaders.1*

%files -n %{libname}
%{_libdir}/libgdk_pixbuf-%{api}.so.%{major}*

%files -n %{xlibname}
%{_libdir}/libgdk_pixbuf_xlib-%{api}.so.%{major}*

%if !%{with bootstrap}
%files -n %{girname}
%{_libdir}/girepository-1.0/GdkPixbuf-%{api}.typelib
%endif

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/gdk-pixbuf
%{_bindir}/gdk-pixbuf-csource
%{_bindir}/gdk-pixbuf-pixdata
%{_libdir}/libgdk_pixbuf-%{api}.so
%{_includedir}/%{pkgname}-%{api}/%{pkgname}/
%{_libdir}/pkgconfig/gdk-pixbuf-%{api}.pc
%if !%{with bootstrap}
%{_datadir}/gir-1.0/GdkPixbuf-%{api}.gir
%endif
%{_mandir}/man1/gdk-pixbuf-csource.1*

%files -n %{devxlib}
%{_libdir}/libgdk_pixbuf_xlib-%{api}.so
%{_includedir}/%{pkgname}-%{api}/%{pkgname}-xlib/
%{_libdir}/pkgconfig/gdk-pixbuf-xlib-%{api}.pc
