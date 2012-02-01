Summary:	Tools for Managing Linux CIFS Client Filesystems
Name:		cifs-utils
Version:	5.3
License:	GPLv3
Group:		Networking/Other
Release:	1
URL:		http://www.samba.org/linux-cifs/cifs-utils/
Source0:	ftp://ftp.samba.org/pub/linux-cifs/cifs-utils/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.samba.org/pub/linux-cifs/cifs-utils/%{name}-%{version}.tar.bz2.asc
BuildRequires:	pkgconfig(talloc)
BuildRequires:	pkgconfig(libcap-ng)
BuildRequires:	keyutils-devel
BuildRequires:	krb5-devel
Suggests:	sudo nss_wins
Provides:	mount-cifs = %{version}
Obsoletes:	mount-cifs <= 4.0
Requires:       keyutils

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

mkdir -p %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.idmap.conf %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.spnego.conf %{buildroot}%{_sysconfdir}/request-key.d
cp contrib/request-key.d/README contrib/request-key.d/README.keyutils-1.5.5

%files
%doc AUTHORS README doc/linux-cifs-client-guide.odt contrib/request-key.d/README.keyutils-1.5.5
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.idmap.conf
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.spnego.conf
%{_bindir}/cifscreds
/sbin/cifs.upcall
/sbin/mount.cifs
/bin/mount.cifs
/bin/umount.cifs
%{_mandir}/man8/cifs.upcall.8*
%{_mandir}/man8/mount.cifs.8*
%{_mandir}/man1/cifscreds.1*
