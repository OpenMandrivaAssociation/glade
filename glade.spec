%define api			2
%define major		0
%define girmajor	2.0

%define libname 	%mklibname gladeui %{api} %{major}
%define develname	%mklibname -d gladeui %{api}
%define girname		%mklibname gladeui-gir %{girmajor}

Summary: 	GTK+ / GNOME 3 widget builder
Name: 		glade
Version: 	3.10.2
Release:	1
License: 	GPLv2+
Url: 		http://glade.gnome.org/
Group: 		Development/GNOME and GTK+
Source0: 	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz

BuildRequires:	desktop-file-utils
BuildRequires: 	gtk-doc
BuildRequires: 	gnome-doc-utils
BuildRequires: 	intltool
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0.2
BuildRequires:	pkgconfig(libxml-2.0) >= 2.4.0
BuildRequires:	pkgconfig(pygobject-2.0) >= 2.27.0
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.10.1
Requires:	pygtk2.0

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

%package -n %{develname}
Summary:	Development libraries and include files for libgladeui (%{name})
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
Development libraries, headers files and documentation needed in order
to develop applications using libgladeui (%{name}).

%package -n %{girname}
Summary:        GObject Introspection interface description for libgladeui (%{name})
Group:          System/Libraries
Requires:       %{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for libgladeui (%{name}).

%prep
%setup -q

%build
%configure2_5x \
	--enable-gtk-doc \
	--disable-scrollkeeper \
	--disable-static

%make

%install
rm -fr %{buildroot}
%makeinstall_std

%find_lang %{name} --with-gnome
for omf in %buildroot%_datadir/omf/*/{*-??,*-??_??}.omf;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %{name}.lang
done

# menu
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GUIDesigner" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# we don't want these
find %{buildroot} -name "*.la" -delete

%files -f %{name}.lang
%doc AUTHORS README TODO
%{_bindir}/%{name}*
%dir %{_libdir}/%{name}/
%dir %{_libdir}/%{name}/modules/
%{_libdir}/%{name}/modules/libgladepython.so
%{_libdir}/%{name}/modules/libgladegtk.so
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/glade*

%files -n %{libname}
%{_libdir}/libgladeui-%{api}.so.%{major}*

%files -n %{girname}
%defattr(-,root,root)
%{_libdir}/girepository-1.0/Gladeui-%{girmajor}.typelib

%files -n %{develname}
%doc ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/libgladeui-2.0/
%{_libdir}/pkgconfig/gladeui-2.0.pc
%{_libdir}/libgladeui-%{api}.so
%{_datadir}/gir-1.0/Gladeui-%{girmajor}.gir

