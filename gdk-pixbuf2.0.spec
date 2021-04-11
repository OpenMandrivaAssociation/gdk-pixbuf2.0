# Wine uses gdk-pixbuf
%ifarch %{x86_64}
%bcond_without compat32
%endif

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
%define devname %mklibname -d %{oname} %{api}
%define girname %mklibname %{oname}-gir %{api}

%define lib32name %mklib32name %{oname} %{api} %{major}
%define dev32name %mklib32name -d %{oname} %{api}
%bcond_with bootstrap

Summary:	Image loading and manipulation library for GTK+
Name:		%{pkgname}%{api}
Version:	2.42.6
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
%if %{with compat32}
BuildRequires:	devel(libjpeg)
BuildRequires:	devel(libtiff)
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(libgobject-2.0)
BuildRequires:	devel(libgio-2.0)
BuildRequires:	devel(libgmodule-2.0)
BuildRequires:	devel(libz)
BuildRequires:	devel(libmount)
BuildRequires:	devel(libblkid)
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
%endif

%description
This package contains libraries used by GTK+ to load and handle
various image formats.

%package -n %{libname}
Summary:	Image loading and manipulation library for GTK+
Group:		System/Libraries

%description -n %{libname}
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
Requires: 	%{name} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
%if !%{with bootstrap}
Requires:	%{girname} = %{version}-%{release}
%endif
Obsoletes:	%{_lib}gdk_pixbuf2.0_0-devel < 2.26

%description -n %{devname}
This package contains the development files needed to compile programs
that uses GTK+ image loading/manipulation library.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Image loading and manipulation library for GTK+ (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This package contains libraries used by GTK+ to load and handle
various image formats.

%package -n %{dev32name}
Summary:	Development files for image handling library for GTK+ (32-bit)
Group:		Development/GNOME and GTK+
Requires: 	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
This package contains the development files needed to compile programs
that uses GTK+ image loading/manipulation library.
%endif

%prep
%autosetup -n %{pkgname}-%{version} -p1

%if %{with compat32}
%meson32 \
	-Dbuiltin_loaders=png \
	-Dgir=false \
	-Dintrospection=disabled \
	-Ddocs=false \
	-Dman=false \
	-Dinstalled_tests=false
%endif

# fix crash in nautilus (GNOME bug #596977)
export CFLAGS=$(echo %{optflags} | sed -e 's/-fomit-frame-pointer//g')

%meson \
	-Djasper=true \
	-Dbuiltin_loaders=png \
%if %{with bootstrap}
	-Dgir=false \
%endif
%if %{enable_gtkdoc}
	-Ddocs=true \
	-Dman=true \
%endif
	-Dinstalled_tests=false

%build
%if %{with compat32}
%ninja_build -C build32 -j2
%endif
%meson_build -j2

%if %enable_tests
%check
xvfb-run %meson_test
%endif

%install
%if %{with compat32}
%ninja_install -C build32
mv %{buildroot}%{_bindir}/gdk-pixbuf-query-loaders %{buildroot}%{_bindir}/gdk-pixbuf-query-loaders-32
touch %{buildroot}%{_prefix}/lib/%{pkgname}-%{api}/%{binver}/loaders.cache
%endif
%meson_install

touch %{buildroot}%{_libdir}/%{pkgname}-%{api}/%{binver}/loaders.cache

(cd %{buildroot}%{_bindir}
 mv gdk-pixbuf-query-loaders gdk-pixbuf-query-loaders-%{__isa_bits}
)

%find_lang %{pkgname}

%post
if [ "$1" = "2" ]; then
    if [ -f %{_libdir}/%{pkgname}-%{api}/%{binver}/loaders.cache ]; then
	rm -f %{_libdir}/%{pkgname}-%{api}/%{binver}/loaders.cache
    fi
fi
%{_bindir}/gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache

%transfiletriggerin -- %{_libdir}/gdk-pixbuf-%{api}/%{binver}/loaders/
%{_bindir}/gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache

%transfiletriggerpostun -- %{_libdir}/gdk-pixbuf-%{api}/%{binver}/loaders/
if [ -x %{_bindir}/gdk-pixbuf-query-loaders-%{__isa_bits} ]; then
    %{_bindir}/gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache
fi

%files -f %{pkgname}.lang
%{_bindir}/gdk-pixbuf-thumbnailer
%{_datadir}/thumbnailers/gdk-pixbuf-thumbnailer.thumbnailer
%if %enable_gtkdoc
%{_mandir}/man1/gdk-pixbuf-query-loaders.1*
%endif

%files -n %{libname}
%{_bindir}/gdk-pixbuf-query-loaders-%{__isa_bits}
%{_libdir}/libgdk_pixbuf-%{api}.so.%{major}*
%dir %{_libdir}/%{pkgname}-%{api}/%{binver}/loaders
%{_libdir}/%{pkgname}-%{api}/%{binver}/loaders/*.so
%ghost %verify (not md5 mtime size) %{_libdir}/%{pkgname}-%{api}/%{binver}/loaders.cache

%if !%{with bootstrap}
%files -n %{girname}
%{_libdir}/girepository-1.0/GdkPixbuf-%{api}.typelib
%{_libdir}/girepository-1.0/GdkPixdata-%{api}.typelib
%endif

%files -n %{devname}
%if %enable_gtkdoc
%doc %{_datadir}/gtk-doc/html/gdk-pixbuf
%{_mandir}/man1/gdk-pixbuf-csource.1*
%endif
%{_bindir}/gdk-pixbuf-csource
%{_bindir}/gdk-pixbuf-pixdata
%{_libdir}/libgdk_pixbuf-%{api}.so
%{_includedir}/%{pkgname}-%{api}/%{pkgname}/
%{_libdir}/pkgconfig/gdk-pixbuf-%{api}.pc
%if !%{with bootstrap}
%{_datadir}/gir-1.0/GdkPixbuf-%{api}.gir
%{_datadir}/gir-1.0/GdkPixdata-%{api}.gir
%endif

%if %{with compat32}
%files -n %{lib32name}
%{_bindir}/gdk-pixbuf-query-loaders-32
%{_prefix}/lib/libgdk_pixbuf-%{api}.so.%{major}*
%dir %{_prefix}/lib/%{pkgname}-%{api}/%{binver}/loaders
%{_prefix}/lib/%{pkgname}-%{api}/%{binver}/loaders/*.so
%ghost %verify (not md5 mtime size) %{_prefix}/lib/%{pkgname}-%{api}/%{binver}/loaders.cache

%files -n %{dev32name}
%{_prefix}/lib/libgdk_pixbuf-%{api}.so
%{_prefix}/lib/pkgconfig/gdk-pixbuf-%{api}.pc
%endif
