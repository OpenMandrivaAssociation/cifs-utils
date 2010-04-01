Summary:	Tools for Managing Linux CIFS Client Filesystems
Name:		cifs-utils
Version:	4.0
License:	GPLv3
Group:		Networking/Other
Release:	%mkrel 0.1
URL:		http://www.samba.org/linux-cifs/cifs-utils/
Source0:	ftp://ftp.samba.org/pub/linux-cifs/cifs-utils/%{name}-%{version}.tar.bz2
#BuildRequires:	talloc-devel >= 4.0
BuildRequires:	pkgconfig(talloc)
BuildRequires:	keyutils-devel
BuildRequires:	krb5-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Tools for Managing Linux CIFS Client Filesystems.

%prep

%setup -q

%build
%serverbuild
rm -rf autom4te.cache
%configure2_5x \
    --sbindir=/sbin

%make

%install
rm -rf %{buildroot}

%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS README doc/linux-cifs-client-guide.odt
/sbin/cifs.upcall
/sbin/mount.cifs
%{_mandir}/man8/cifs.upcall.8*
%{_mandir}/man8/mount.cifs.8*

