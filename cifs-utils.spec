Summary:	Tools for Managing Linux CIFS Client Filesystems
Name:		cifs-utils
Version:	4.9
License:	GPLv3
Group:		Networking/Other
Release:	%mkrel 1
URL:		http://www.samba.org/linux-cifs/cifs-utils/
Source0:	ftp://ftp.samba.org/pub/linux-cifs/cifs-utils/%{name}-%{version}.tar.bz2
#BuildRequires:	talloc-devel >= 4.0
BuildRequires:	pkgconfig(talloc)
BuildRequires:	keyutils-devel
BuildRequires:	krb5-devel
BuildRequires:	cap-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Suggests:	sudo nss_wins
Provides:	mount-cifs = %{version}
Obsoletes:	mount-cifs <= 4.0

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
mkdir %{buildroot}/bin
ln -s ../sbin/mount.cifs %{buildroot}/bin/mount.cifs
# Hack for smb4k
ln -s umount %{buildroot}/bin/umount.cifs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS README doc/linux-cifs-client-guide.odt
/sbin/cifs.upcall
/sbin/mount.cifs
/bin/mount.cifs
/bin/umount.cifs
%{_mandir}/man8/cifs.upcall.8*
%{_mandir}/man8/mount.cifs.8*

