%define major	6
%define majorpp	1
%define libname %mklibname ggzdmod %{major}
%define libnamepp %mklibname ggzdmod++ %{majorpp}
%define devname %mklibname ggzdmod -d

%define enable_mysql 0
%{?_with_mysql: %global enable_mysql 1}

%define enable_pgsql 0
%{?_with_pgsql: %global enable_pgsql 1}

Summary:	Server software for the GGZ Gaming Zone
Name:		ggz-server
Version:	0.0.14.1
Release:	18
License:	GPLv2
Group:		Games/Other
Url:		https://www.ggzgamingzone.org/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		ggz-server-gcc43.diff
Patch1:		ggz-server-linkage_fix.diff
Patch2:		ggz_server_inotify.patch
Patch3:		ggz-server_wformat.patch
Patch4:		ggz-server-0.0.14.1-cstdio.patch
Patch5:		ggz-server-0.0.14.1-gcc46.patch

BuildRequires:	libggz-devel = %{version}
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(expat)
%if %{enable_mysql}
BuildRequires:	mysql-devel
%else
%if %{enable_pgsql}
BuildRequires:	postgresql-devel
%else
BuildRequires:	db-devel
%endif
%endif

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

%package -n	%{libname}
Summary:	GGZ server libraries
Group:		System/Libraries

%description -n	%{libname}
This package provides the libraries needed to run the server.

%package -n	%{libnamepp}
Summary:	GGZ server libraries
Group:		System/Libraries
Conflicts:	%{_lib}ggzdmod6 < 0.0.14.1-12

%description -n	%{libnamepp}
This package provides the libraries needed to run the server.

%package -n	%{devname}
Summary:	GGZ server development libraries
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{name}-devel < 0.0.14.1-12
Requires:	%{libname} = %{EVRD}
Requires:	%{libnamepp} = %{EVRD}

%description -n	%{devname}
This package provides all development related files necessary for you to
develop or compile any extra games which supports GGZ gaming server.

%prep
%if %{enable_mysql} && %{enable_pgsql}
echo "\"--with mysql\" and \"--with pgsql\" can't be used together."
exit 1
%endif

%setup -q
%autopatch -p1
autoreconf -fi

%build
%serverbuild
%configure2_5x \
	--disable-static \
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
%make LIBS="-pthread"

%install
%makeinstall_std

%files
%doc AUTHORS COPYING INSTALL NEWS README README.GGZ TODO
%config(noreplace) /etc/ggzd
%{_bindir}/*
%{_libdir}/ggzd
%{_datadir}/ggz/ggzd
%{_mandir}/man?/*

%files -n %{libname}
%{_libdir}/libggzdmod.so.%{major}*

%files -n %{libnamepp}
%{_libdir}/libggzdmod++.so.%{majorpp}*

%files -n %{devname}
%doc ChangeLog
%{_includedir}/*
%{_libdir}/libggzdmod++.so
%{_libdir}/libggzdmod.so

