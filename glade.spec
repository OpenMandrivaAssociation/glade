%define url_ver %(echo %{version}|cut -d. -f1,2)
%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1

%define api 2
%define major 13
%define gimajor 2.0
%define libname %mklibname gladeui %{api} %{major}
%define devname %mklibname -d gladeui %{api}
%define girname %mklibname gladeui-gir %{gimajor}

Summary:	GTK+ / GNOME 3 widget builder
Name:		glade
Version:	3.38.1
Release:	2
License:	GPLv2+
Url:		http://glade.gnome.org/
Group:		Development/GNOME and GTK+
Source0:	http://ftp.gnome.org/pub/GNOME/sources/glade/%{url_ver}/%{name}-%{version}.tar.xz
# Glade 3.38.1 force use python embed in 3.8 version. Let's try use 3.9.
Patch0:		embed.patch

BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:	desktop-file-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:  pkgconfig(gjs-1.0)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:  pkgconfig(webkit2gtk-4.0)

%description
Glade is a RAD tool to enable quick & easy development of user interfaces
for the Gtk+ toolkit and the GNOME desktop environment.

The user interfaces designed in Glade are stored in XML format,
enabling easy integration with external tools. In particular libglade can
load the XML files and create the interfaces at runtime.

Other tools are available which can turn the XML files into source code
in languages such as C++, Perl and Python.

%package -n %{libname}
Summary:	Libraries required for %{name}
Group:		System/Libraries
Provides:	libgladeui = %{version}-%{release}

%description -n %{libname}
Libraries and file require to run program built with %{name}

%package -n %{devname}
Summary:	Development libraries and include files for libgladeui (%{name})
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}

%description -n %{devname}
Development libraries, headers files and documentation needed in order
to develop applications using libgladeui (%{name}).

%package -n %{girname}
Summary:	GObject Introspection interface description for libgladeui (%{name})
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for libgladeui (%{name}).

%prep
%setup -q
%autopatch -p1

%build
%meson

%meson_build

%install
%meson_install

%find_lang %{name} --with-gnome

# menu
desktop-file-install --vendor="" \
	--remove-category="Application" \
	--add-category="GUIDesigner" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

%files -f %{name}.lang
%doc AUTHORS NEWS TODO
%{_bindir}/%{name}*
%dir %{_libdir}/%{name}/
%dir %{_libdir}/%{name}/modules/
%{_libdir}/%{name}/modules/libgladepython.so
%{_libdir}/%{name}/modules/libgladegtk.so
%{_libdir}/%{name}/modules/libgladewebkit2gtk.so
%{_libdir}/%{name}/modules/libgladegjs.so
%{_datadir}/%{name}
%{_datadir}/gettext/its/glade-catalog.*
%{_datadir}/metainfo//org.gnome.Glade.appdata.xml
%{_datadir}/applications/org.gnome.Glade.desktop
%{_iconsdir}/hicolor/*/apps/glade*
%{_datadir}/icons/hicolor/*/apps/org.gnome.Glade*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libgladeui-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Gladeui-%{gimajor}.typelib

%files -n %{devname}
%{_includedir}/libgladeui-2.0/
%{_libdir}/pkgconfig/gladeui-2.0.pc
%{_libdir}/libgladeui-%{api}.so
%{_datadir}/gir-1.0/Gladeui-%{gimajor}.gir
