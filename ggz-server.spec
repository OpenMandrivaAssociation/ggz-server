%define version 0.0.14.1
%define release %mkrel 4

%define lib_major 6
%define libname %mklibname ggzdmod %{lib_major}
%define libname_basic libggzdmod

%define enable_mysql 0
%{?_with_mysql: %global enable_mysql 1}

%define enable_pgsql 0
%{?_with_pgsql: %global enable_pgsql 1}

Name:		ggz-server
Summary:	Server software for the GGZ Gaming Zone
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Games/Other
Source:		%name-%version.tar.bz2
URL:		http://www.ggzgamingzone.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libggz-devel = %{version}
BuildRequires:	popt-devel autoconf
BuildRequires:	expat-devel
%if %enable_mysql
BuildRequires:	mysql-devel
%else
%if %enable_pgsql
BuildRequires:	postgresql-devel
%else
BuildRequires:	db4-devel
%endif
%endif
Requires:	libggz = %{version}
Requires:	%{libname} = %{version}

%description
The GGZ Gaming Zone server allows other computers to connect to yours via
the Internet and play network games.  Currently, the following game servers
are packaged with GGZ:
  - Spades		- Connect the Dots
  - Tic-Tac-Toe		- La Pocha
  - Chinese Checkers	- Chess
  - Combat		- Hastings
  - Krosswater		- Reversi
  - GGZ Cards		- Escape
  - Keepalive		- Muehle

# Main package
%package -n	%{libname}
Summary:	GGZ server libraries
Group:		System/Libraries
Provides:	%{libname_basic} = %{version}

%description -n	%{libname}
The GGZ Gaming Zone server allows other computers to connect to yours via
the Internet and play network games.  Currently, the following game servers
are packaged with GGZ:
  - Spades		- Connect the Dots
  - Tic-Tac-Toe		- La Pocha
  - Chinese Checkers	- Chess
  - Combat		- Hastings
  - Krosswater		- Reversi
  - GGZ Cards		- Escape
  - Keepalive		- Muehle

This package provides the libraries needed to run the server.

# Devel package
%package	devel
Summary:	GGZ server development libraries
Group:		Development/C
Provides:	%{libname_basic}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%libname = %{version}

%description	devel
The GGZ Gaming Zone server allows other computers to connect to yours via
the Internet and play network games.  Currently, the following game servers
are packaged with GGZ:
  - Spades		- Connect the Dots
  - Tic-Tac-Toe		- La Pocha
  - Chinese Checkers	- Chess
  - Combat		- Hastings
  - Krosswater		- Reversi
  - GGZ Cards		- Escape
  - Keepalive		- Muehle

This package provides all development related files necessary for you to
develop or compile any extra games which supports GGZ gaming server.

%prep
%if %enable_mysql && %enable_pgsql
echo "\"--with mysql\" and \"--with pgsql\" can't be used together."
exit 1
%endif

%setup -q

autoconf

%build
%serverbuild
%configure \
	--with-libggz-libraries=%{_libdir} \
%if %enable_mysql
	--with-database=mysql
%else
%if %enable_pgsql
	--with-database=pgsql
%else
	--with-database=db4
%endif
%endif
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL NEWS README README.GGZ TODO

%config(noreplace) /etc/ggzd
%{_bindir}/*
%{_libdir}/ggzd
%{_datadir}/ggz/ggzd
%{_mandir}/man?/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libggzdmod.so.%{lib_major}
%{_libdir}/libggzdmod.so.%{lib_major}.*
%{_libdir}/libggzdmod++.so.*

%files devel
%defattr(-,root,root)
%doc ChangeLog
%{_includedir}/*
%{_libdir}/libggzdmod++.a
%{_libdir}/libggzdmod++.la
%{_libdir}/libggzdmod.a
%{_libdir}/libggzdmod.la
%{_libdir}/libggzdmod++.so
%{_libdir}/libggzdmod.so



