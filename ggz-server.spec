%define lib_major 6
%define libname %mklibname ggzdmod %{lib_major}
%define libname_basic libggzdmod

%define enable_mysql 0
%{?_with_mysql: %global enable_mysql 1}

%define enable_pgsql 0
%{?_with_pgsql: %global enable_pgsql 1}

Name:		ggz-server
Summary:	Server software for the GGZ Gaming Zone
Version:	0.0.14.1
Release:	11
License:	GPL
Group:		Games/Other
URL:		http://www.ggzgamingzone.org/
Source:		%{name}-%{version}.tar.bz2
Patch0:		ggz-server-gcc43.diff
Patch1:		ggz-server-linkage_fix.diff
Patch2:		ggz_server_inotify.patch
Patch3:		ggz-server_wformat.patch
Patch4:		ggz-server-0.0.14.1-cstdio.patch
Patch5:		ggz-server-0.0.14.1-gcc46.patch
BuildRequires:	autoconf
BuildRequires:	libggz-devel = %{version}
BuildRequires:	popt-devel
BuildRequires:	expat-devel
%if %{enable_mysql}
BuildRequires:	mysql-devel
%else
%if %{enable_pgsql}
BuildRequires:	postgresql-devel
%else
BuildRequires:	db-devel
%endif
%endif
Requires:	libggz = %{version}
Requires:	%{libname} = %{version}-%{release}

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
Provides:	%{libname_basic} = %{version}-%{release}

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
Requires:	%{libname} = %{version}-%{release}

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
%if %{enable_mysql} && %{enable_pgsql}
echo "\"--with mysql\" and \"--with pgsql\" can't be used together."
exit 1
%endif

%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0

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
%{_libdir}/libggzdmod.so.%{lib_major}
%{_libdir}/libggzdmod.so.%{lib_major}.*
%{_libdir}/libggzdmod++.so.*

%files devel
%doc ChangeLog
%{_includedir}/*
%{_libdir}/libggzdmod++.so
%{_libdir}/libggzdmod.so


%changelog
* Mon Apr 11 2011 Funda Wang <fwang@mandriva.org> 0.0.14.1-9mdv2011.0
+ Revision: 652515
- fix build with gcc 46
- build with db 5.1

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.0.14.1-8mdv2011.0
+ Revision: 605452
- rebuild

* Thu Dec 31 2009 Funda Wang <fwang@mandriva.org> 0.0.14.1-7mdv2010.1
+ Revision: 484309
- rebuild for db4.8

* Thu Sep 24 2009 Olivier Blin <oblin@mandriva.com> 0.0.14.1-6mdv2010.0
+ Revision: 448434
- fix build by including cstdio for EOF declaration
- fix some wformat errors (from Arnaud Patard)
- fix inotify stuff with patch from upstream (from Arnaud Patard)

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.0.14.1-5mdv2009.0
+ Revision: 234881
- added a gc43 fix (P0)
- added a linkage fix (P1)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Mar 23 2008 Emmanuel Andry <eandry@mandriva.org> 0.0.14.1-3mdv2008.1
+ Revision: 189604
- Fix lib group

* Sun Mar 23 2008 Emmanuel Andry <eandry@mandriva.org> 0.0.14.1-2mdv2008.1
+ Revision: 189602
- Fix devel group

* Tue Feb 26 2008 Emmanuel Andry <eandry@mandriva.org> 0.0.14.1-1mdv2008.1
+ Revision: 175531
- New version

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Dec 27 2007 Oden Eriksson <oeriksson@mandriva.com> 0.0.14-5mdv2008.1
+ Revision: 138207
- rebuilt against bdb 4.6.x libs

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Jul 16 2007 Emmanuel Andry <eandry@mandriva.org> 0.0.14-4mdv2008.0
+ Revision: 52713
- fix devel package
- use %%serverbuild macro


* Sun Mar 04 2007 Emmanuel Andry <eandry@mandriva.org> 0.0.14-3mdv2007.1
+ Revision: 131941
- rebuild with db4.5

* Wed Feb 28 2007 Emmanuel Andry <eandry@mandriva.org> 0.0.14-2mdv2007.1
+ Revision: 130240
- fix devel package

* Sat Feb 10 2007 Emmanuel Andry <eandry@mandriva.org> 0.0.14-1mdv2007.1
+ Revision: 118737
- New version 0.0.14
- New major 6
- Import ggz-server

* Sun Sep 03 2006 Emmanuel Andry <eandry@mandriva.org> 0.0.13-2mdv2007.0
- fix build on x86_64

* Mon May 22 2006 Emmanuel Andry <eandry@mandriva.org> 0.0.13-1mdk
- New version
- mkrel
- drop patch

* Sat Jan 15 2005 Abel Cheung <deaddog@mandrake.org> 0.0.9-1mdk
- New version

