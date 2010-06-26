# build_fb: Build frame buffer backend 
#	0 = no
#	1 = yes
%define build_fb	0

# enable_gtkdoc: Toggle if gtk-doc files should be rebuilt.
#      0 = no
#      1 = yes
%define enable_gtkdoc 1

# enable_bootstrap: Toggle if bootstrapping package
#      0 = no
#      1 = yes
%define enable_bootstrap 0

# enable_tests: Run test suite in build
#      0 = no
#      1 = yes
%define enable_tests 0

%{?_without_gtkdoc: %{expand: %%define enable_gtkdoc 0}}
%{?_without_fb: %{expand: %%define build_fb 0}}
%{?_without_bootstrap: %{expand: %%define enable_bootstrap 0}}
%{?_without_tests: %{expand: %%define enable_tests 0}}

%{?_with_gtkdoc: %{expand: %%define enable_gtkdoc 1}}
%{?_with_fb: %{expand: %%define build_fb 1}}
%{?_with_bootstrap: %{expand: %%define enable_bootstrap 1}}
%{?_with_tests: %{expand: %%define enable_tests 1}}


# required version of various libraries
%define req_glib_version		2.21.3
%define req_pango_version		1.20.0
%define req_atk_version			1.29.4
%define req_cairo_version		1.6.0

%define pkgname			gtk+
%define api_version		2.0
%define binary_version	2.10
%define lib_major		0
%define libname			%mklibname %{pkgname} %{api_version} %{lib_major}
%define libname_x11		%mklibname %{pkgname}-x11- %{api_version} %{lib_major}
%define libname_linuxfb %mklibname %{pkgname}-linuxfb- %{api_version} %{lib_major}
%define libname_pixbuf  %mklibname gdk_pixbuf %{api_version} %{lib_major}

%define gail_major 18
%define gail_libname %mklibname gail %gail_major
%define gaildevelname %mklibname -d gail

%define git_url git://git.gnome.org/gtk+

Summary:	The GIMP ToolKit (GTK+), a library for creating GUIs
Name:		%{pkgname}%{api_version}
Version:	2.20.1
Release:        %mkrel 1
License:	LGPLv2+
Group:		System/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%pkgname/%{pkgname}-%{version}.tar.bz2
# extra IM modules (vietnamese and tamil) -- pablo
Patch4:		gtk+-2.13.1-extra_im.patch 
# (fc) 2.0.6-8mdk fix infinite loop and crash in file selector when / and $HOME are not readable (bug #90)
Patch5:		gtk+-2.6.9-fileselectorfallback.patch
# (fc) 2.4.0-2mdk use Ia Ora theme by default if available
Patch12:	gtk+-defaulttheme.patch
# (gb) 2.4.4-2mdk handle biarch
Patch13:	gtk+-2.2.4-lib64.patch
# (fc) 2.18.2-2mdv fix nautilus crash (GNOME bug #596977) (pterjan)
Patch15:	gtk+-2.18.1-fixnautiluscrash.patch
# (fc) 2.20.0-2mdv improve tooltip appareance (GNOME bug #599617) (Fedora)
Patch18:	gtk+-2.20.0-fresh-tooltips.patch
# (fc) 2.20.0-2mdv improve tooltip positioning (GNOME bug #599618) (Fedora)
Patch19:	gtk+-2.20.0-tooltip-positioning.patch
# (fc) 2.20.0-2mdv allow window dragging toolbars / menubar (GNOME bug #611313)
Patch20:	gtk+-2.20.0-window-dragging.patch
# (fc) 2.20.0-3mdv allow specifying icon padding for tray icon (GNOME bug #583273) (Fedora)
Patch21:	gtk+-2.20.0-icon-padding.patch
# (fc) 2.20.0-3mdv use proper screen for getshape (GNOME bug #615853) (GIT)
Patch22:	gtk+-2.20.0-proper-screen.patch

Conflicts:	perl-Gtk2 < 1.113

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

URL:		http://www.gtk.org
Requires:	common-licenses
BuildRequires:	gettext-devel
BuildRequires:  libglib2.0-devel >= %{req_glib_version}
BuildRequires:	libatk1.0-devel >= %{req_atk_version}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:  cairo-devel >= %{req_cairo_version}
BuildRequires:	pango-devel >= %{req_pango_version}
BuildRequires:  gobject-introspection-devel
BuildRequires:  X11-devel
BuildRequires:  cups-devel
BuildRequires:  fam-devel
BuildRequires:  jasper-devel
%if %enable_tests
%if %mdkversion <= 200600
BuildRequires:	XFree86-Xvfb
%else
BuildRequires:  x11-server-xvfb
%endif
%endif
%if %enable_gtkdoc
BuildRequires: gtk-doc >= 0.9 
BuildRequires: sgml-tools
BuildRequires: texinfo
%endif
# gw tests will fail without this
BuildRequires: fonts-ttf-dejavu
%if !%{enable_bootstrap}
Suggests: xdg-user-dirs-gtk
Suggests: ia_ora-gnome
%endif
Requires: %{libname} = %{version}
Provides:	%{pkgname}2 = %{version}-%{release}
Obsoletes:	%{pkgname}2
Provides:	gail = %version-%release
Obsoletes:	gail

%description
The gtk+ package contains the GIMP ToolKit (GTK+), a library for creating
graphical user interfaces for the X Window System.  GTK+ was originally
written for the GIMP (GNU Image Manipulation Program) image processing
program, but is now used by several other programs as well.  

If you are planning on using the GIMP or another program that uses GTK+,
you'll need to have the gtk+ package installed.

%package -n %{libname}
Summary: %{summary}
Group:	 %{group}
Obsoletes:	lib%{pkgname}2
Provides:	lib%{pkgname}2 = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}
Provides:   gtk2 = %{version}-%{release}
Requires:   libglib2.0 >= %{req_glib_version}
Requires:   libpango1.0 >= %{req_pango_version}
Requires:   libatk1.0 >= %{req_atk_version}
Conflicts:  libgnomeui2_0 <= 2.0.5
Conflicts:  gtk-engines2 <= 2.2.0-7mdk
Conflicts:  %{libname_x11} < 2.10.3-2mdv2007.0
Requires(post): 	%{libname_x11} = %{version}
%if !%{enable_bootstrap}
Suggests: %{_lib}ia_ora-gnome
%endif

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with gtk+.

%package -n %{libname}-devel
Summary:	Development files for GTK+ (GIMP ToolKit) applications
Group:		Development/GNOME and GTK+
Obsoletes:  %{libname_x11}-devel
Provides:   %{libname_x11}-devel = %{version}-%{release}
Provides:   gtk2-devel = %{version}-%{release}
Obsoletes:	%{pkgname}2-devel
Obsoletes:  lib%{pkgname}2-devel
Provides:	%{pkgname}2-devel = %{version}-%{release}
Provides:	lib%{pkgname}2-devel = %{version}-%{release}
Provides:	lib%{pkgname}%{api_version}-devel = %{version}-%{release}
Provides:	%{libname}-devel = %{version}-%{release}
Provides:	lib%{pkgname}-x11-%{api_version}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Requires:	%{libname_x11} = %{version}
Requires:	%{libname_pixbuf}-devel = %{version}
Requires:	libatk1.0-devel >= %{req_atk_version}
Requires:	libpango1.0-devel >= %{req_pango_version}


%description -n %{libname}-devel
The libgtk+-devel package contains the static libraries and header files
needed for developing GTK+ (GIMP ToolKit) applications. The libgtk+-devel
package contains GDK (the General Drawing Kit, which simplifies the interface
for writing GTK+ widgets and using GTK+ widgets in applications), and GTK+
(the widget set).


%package -n %{libname_pixbuf}
Summary:	Image loading and manipulation library for GTK+
Group:		System/Libraries
Provides:	libgdk_pixbuf%{api_version} = %{version}-%{release}
Requires(post):		libtiff >= 3.6.1
Conflicts: gir-repository < 0.6.5-4

%description -n %{libname_pixbuf}
This package contains libraries used by GTK+ to load and handle
various image formats.

%package -n %{libname_pixbuf}-devel
Summary:	Development files for image handling library for GTK+
Group:		Development/GNOME and GTK+
Provides:	libgdk_pixbuf%{api_version}-devel = %{version}-%{release}
Requires:	%{libname_pixbuf} = %{version}
Requires:	libglib2.0-devel >= %{req_glib_version}

%description -n %{libname_pixbuf}-devel
This package contains the development files needed to compile programs
that uses GTK+ image loading/manipulation library.

%package -n %{libname_x11}
Summary:	X11 backend of The GIMP ToolKit (GTK+)
Group:		System/Libraries
Provides:	lib%{pkgname}-x11-%{api_version} = %{version}-%{release}
Provides:	%{name}-backend = %{version}-%{release}
Requires(post):		%{libname_pixbuf} = %{version}
Requires: 	%{libname} = %{version}
Requires:	%{name} >= %{version}-%{release}
Conflicts:  libgtk+2-devel < 2.0.0
Conflicts: gir-repository < 0.6.5-4

%description -n %{libname_x11}
This package contains the X11 version of library needed to run
programs dynamically linked with gtk+.

%if 0
%package -n %{libname_linuxfb}
Summary:	Frame-Buffer backend of The GIMP ToolKit (GTK+)
Group:		System/Libraries
Obsoletes:	lib%{pkgname}2-linuxfb
Provides:	lib%{pkgname}2-linuxfb = %{version}-%{release}
Provides:	%{libname}-linuxfb-%{api_version} = %{version}-%{release}
Provides:	%{name}-backend = %{version}-%{release}
Requires(post):		%{libname_pixbuf} = %{version}
Requires(post):		%{libname} = %{version}
Requires:	%{name} >= %{version}-%{release}

%description -n %{libname_linuxfb}
This package contains the Frame Buffer version of library needed to run
programs dynamically linked with gtk+.

%package -n %{libname_linuxfb}-devel
Summary:	Development files for frame-buffer backend of GTK+
Group:		Development/GNOME and GTK+
Obsoletes:	lib%{pkgname}2-linuxfb-devel
Provides:	lib%{pkgname}2-linuxfb-devel = %{version}-%{release}
Provides:	lib%{pkgname}-linuxfb-%{api_version}-devel = %{version}-%{release}
Requires:   %{libname}-devel = %{version}
Requires:	%{libname_linuxfb} = %{version}
Requires:	%{libname_pixbuf}-devel = %{version}
Requires:	libatk1.0-devel >= %{req_atk_version}
Requires:	libpango1.0-devel >= %{req_pango_version}

%description -n %{libname_linuxfb}-devel
This package contains the development files needed to compile programs
with gtk+ Frame Buffer.
%endif

%package -n %{gail_libname}
Summary:	GNOME Accessibility Implementation Library
Group:		System/Libraries
Provides:	libgail = %{version}-%{release}
Conflicts:	gail < 1.9.4-2mdv


%description -n %{gail_libname}
Gail is the GNOME Accessibility Implementation Library

%package -n %gaildevelname
Summary:	Static libraries, include files for GAIL
Group:		Development/GNOME and GTK+
Provides:	gail-devel = %{version}-%{release}
Provides:	libgail-devel = %{version}-%{release}
Requires:	%{gail_libname} = %{version}
Conflicts:	%{_lib}gail17-devel
Obsoletes: %mklibname -d gail 18

%description -n %gaildevelname
Gail is the GNOME Accessibility Implementation Library

%prep
%setup -n %{pkgname}-%{version} -q
%patch4 -p1 -b .extra_im
%patch5 -p1 -b .fileselectorfallback
%patch12 -p1 -b .defaulttheme
%patch13 -p1 -b .lib64
#patch15 -p1 -b .fixnautiluscrash
%patch18 -p1 -b .fresh-tooltips
%patch19 -p1 -b .tooltip-positioning
%patch20 -p1 -b .window-dragging
%patch21 -p1 -b .icon-padding
%patch22 -p1 -b .proper-screen

#needed by patches 4 & 13
autoreconf -fi

%build
%ifarch ppc64
export CFLAGS="$RPM_OPT_FLAGS -mminimal-toc"
%endif

# Build X11 backend
#[ -d X11-build ] || mkdir X11-build
#cd X11-build

# fix crash in nautilus (GNOME bug #596977)
export CFLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-fomit-frame-pointer//g'`

#CONFIGURE_TOP=.. 
export CPPFLAGS="-DGTK_COMPILATION"
%define _disable_ld_no_undefined 1
%configure2_5x --enable-xinerama \
	--with-xinput=xfree \
%if !%enable_gtkdoc
	--enable-gtk-doc=no
%endif

#gw parallel make fails in 2.19.3-3mdv
make
cd gdk
make Gdk-2.0.typelib
cd ..

#cd ..
# Then build frame buffer counterpart
%if %build_fb
[ -d fb-build ] || mkdir fb-build
cd fb-build
CONFIGURE_TOP=.. %configure2_5x \
	--with-gdktarget=linux-fb \
	--enable-gtk-doc=no

%make
cd ..
%endif

%check
%if %enable_tests
#cd X11-build
XDISPLAY=$(i=1; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
%if %mdkversion <= 200600
%{_prefix}/X11R6/bin/Xvfb :$XDISPLAY &
%else
%{_bindir}/Xvfb :$XDISPLAY &
%endif
export DISPLAY=:$XDISPLAY
make check
kill $(cat /tmp/.X$XDISPLAY-lock) ||:
#cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

# Avoid conflict with different ChangeLogs
cp ./contrib/gdk-pixbuf-xlib/ChangeLog ./contrib/gdk-pixbuf-xlib/ChangeLog-gdk-pixbuf-xlib
cp ./gdk-pixbuf/ChangeLog ./gdk-pixbuf/ChangeLog-gdk-pixbuf

%if %build_fb
cd fb-build
%makeinstall_std RUN_QUERY_IMMODULES_TEST=false RUN_QUERY_LOADER_TEST=false
cd ..
%endif

#cd X11-build
%makeinstall_std mandir=%{_mandir} RUN_QUERY_IMMODULES_TEST=false RUN_QUERY_LOADER_TEST=false
cp gdk/Gdk-2.0.typelib %buildroot%_libdir/girepository-1.0/

#cd ..

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-%{api_version}
touch $RPM_BUILD_ROOT%{_sysconfdir}/gtk-%{api_version}/gtk.immodules.%{_lib}
touch $RPM_BUILD_ROOT%{_sysconfdir}/gtk-%{api_version}/gdk-pixbuf.loaders.%{_lib}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/modules

# handle biarch packages
progs="gtk-query-immodules-%{api_version} gdk-pixbuf-query-loaders"
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/bin
for f in $progs; do
  mv -f $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/bin/
  cat > $RPM_BUILD_ROOT%{_bindir}/$f << EOF
#!/bin/sh
lib=%{_lib}
case ":\$1:" in
:lib*:) lib="\$1"; shift 1;;
esac
exec %{_prefix}/\$lib/gtk-%{api_version}/bin/$f \${1+"\$@"}
EOF
  chmod +x $RPM_BUILD_ROOT%{_bindir}/$f
done

%{find_lang} gtk20
%find_lang gtk20-properties
cat gtk20-properties.lang >> gtk20.lang

#remove not packaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/*.la \
  $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/%{binary_version}.*/loaders/*.la \
  $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/%{binary_version}.*/engines/*.la \
  $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/%{binary_version}.*/printbackends/*.la \
  $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname_pixbuf}
%if %mdkversion < 200900
/sbin/ldconfig
%endif

if [ "$1" = "2" ]; then
  if [ -f %{_sysconfdir}/gtk-%{api_version}/gdk-pixbuf.loaders ]; then
    rm -f %{_sysconfdir}/gtk-%{api_version}/gdk-pixbuf.loaders
  fi
fi

%{_libdir}/gtk-%{api_version}/bin/gdk-pixbuf-query-loaders >  %{_sysconfdir}/gtk-%{api_version}/gdk-pixbuf.loaders.%{_lib}

%if %mdkversion < 200900
%postun -n %{libname_pixbuf} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libname_x11} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname_x11} -p /sbin/ldconfig
%endif

%post -n %{libname}
if [ "$1" = "2" ]; then
  if [ -f %{_sysconfdir}/gtk-%{api_version}/gtk.immodules ]; then
    rm -f %{_sysconfdir}/gtk-%{api_version}/gtk.immodules
  fi
fi

%{_libdir}/gtk-%{api_version}/bin/gtk-query-immodules-%{api_version} > %{_sysconfdir}/gtk-%{api_version}/gtk.immodules.%{_lib}

%if %{build_fb}
%if %mdkversion < 200900
%post -n %{libname_linuxfb} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname_linuxfb} -p /sbin/ldconfig
%endif
%endif

%post 
if [ -d %{_datadir}/icons ]; then
 for i in `/bin/ls %{_datadir}/icons` ; do 
  [ -d "%{_datadir}/icons/$i" -a -e "%{_datadir}/icons/$i/icon-theme.cache" -a -e "%{_datadir}/icons/$i/index.theme" ] && gtk-update-icon-cache --force --quiet %{_datadir}/icons/$i
 done
 exit 0
fi

%files -f gtk20.lang
%defattr(-, root, root)
%doc README
%{_bindir}/gtk-query-immodules-%{api_version}
%{_bindir}/gdk-pixbuf-query-loaders
%{_bindir}/gtk-update-icon-cache
%{_datadir}/themes
%dir %{_sysconfdir}/gtk-%{api_version}
%config(noreplace) %{_sysconfdir}/gtk-%{api_version}/im-multipress.conf

%files -n %{libname}
%defattr(-, root, root)
%doc README
%ghost %verify (not md5 mtime size) %config(noreplace) %{_sysconfdir}/gtk-%{api_version}/gtk.immodules.%{_lib}
%dir %{_libdir}/gtk-%{api_version}
%dir %{_libdir}/gtk-%{api_version}/bin
%{_libdir}/gtk-%{api_version}/bin/gtk-query-immodules-%{api_version}
%dir %{_libdir}/gtk-%{api_version}/modules
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}.*
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/*.so
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}.*/engines
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/engines/*.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/printbackends/*.so

%files -n %{libname}-devel
%defattr(-, root, root)
%doc docs/*.txt AUTHORS ChangeLog NEWS* README*
%doc %{_datadir}/gtk-doc/html/gdk
%doc %{_datadir}/gtk-doc/html/gtk
%{_bindir}/gtk-demo
%_bindir/gtk-builder-convert
%{_datadir}/aclocal/*
%{_datadir}/gtk-%{api_version}
%{_includedir}/gtk-unix-print-%{api_version}/
%{_includedir}/gtk-%{api_version}/gdk
%{_includedir}/gtk-%{api_version}/gtk
%{_libdir}/gtk-%{api_version}/include
%{_libdir}/pkgconfig/gdk-%{api_version}.pc
%{_libdir}/pkgconfig/gtk+-%{api_version}.pc
%{_libdir}/pkgconfig/gtk+-unix-print-%{api_version}.pc
%{_libdir}/*x11*.so
%_datadir/gir-1.0/Gdk-2.0.gir
%_datadir/gir-1.0/Gtk-2.0.gir
%attr(644,root,root) %{_libdir}/*x11*.la
%{_libdir}/pkgconfig/*x11*


%files -n %{libname_pixbuf}
%defattr(-, root, root)
%{_libdir}/libgdk_pixbuf*.so.*
%_libdir/girepository-1.0/GdkPixbuf-2.0.typelib
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}.*/loaders
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/loaders/*.so
%{_libdir}/gtk-%{api_version}/bin/gdk-pixbuf-query-loaders
%ghost %verify (not md5 mtime size) %config(noreplace) %{_sysconfdir}/gtk-%{api_version}/gdk-pixbuf.loaders.%{_lib}

%files -n %{libname_pixbuf}-devel
%defattr(-, root, root)
%doc contrib/gdk-pixbuf-xlib/ChangeLog-* gdk-pixbuf/ChangeLog-*
%doc %{_datadir}/gtk-doc/html/gdk-pixbuf
%{_bindir}/gdk-pixbuf-csource
%dir %{_includedir}/gtk-%{api_version}
%{_includedir}/gtk-%{api_version}/gdk-pixbuf*
%_datadir/gir-1.0/GdkPixbuf-2.0.gir
%{_libdir}/libgdk_pixbuf*.so
%attr(644,root,root) %{_libdir}/libgdk_pixbuf*.la
%{_libdir}/pkgconfig/gdk-pixbuf*.pc


%files -n %{libname_x11}
%defattr(-, root, root)
%{_libdir}/*x11*.so.*
%_libdir/girepository-1.0/Gdk-2.0.typelib
%_libdir/girepository-1.0/Gtk-2.0.typelib

%if %build_fb
%files -n %{libname_linuxfb}
%defattr(-, root, root)
%{_libdir}/*linux-fb*.so.*

%files -n %{libname_linuxfb}-devel
%defattr(-, root, root)
%{_libdir}/*linux-fb*.so
%attr(644,root,root) %{_libdir}/*linux-fb*.la
%{_libdir}/pkgconfig/*linux-fb*
%endif

%files -n %gail_libname
%defattr(-,root,root)
%{_libdir}/libgailutil.so.%{gail_major}*
%{_libdir}/gtk-2.0/modules/libferret.so
%{_libdir}/gtk-2.0/modules/libgail.so

%files -n %gaildevelname
%defattr(-,root,root)
%{_datadir}/gtk-doc/html/gail-libgail-util
%{_libdir}/libgailutil.so
%attr(644,root,root) %{_libdir}/libgailutil.la
%{_includedir}/gail-1.0
%{_libdir}/pkgconfig/gail.pc
