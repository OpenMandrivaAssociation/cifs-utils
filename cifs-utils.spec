Summary:	Tools for Managing Linux CIFS Client Filesystems
Name:		cifs-utils
Version:	5.8
License:	GPLv3
Group:		Networking/Other
Release:	3
Url:		http://www.samba.org/linux-cifs/cifs-utils/
Source0:	ftp://ftp.samba.org/pub/linux-cifs/cifs-utils/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.samba.org/pub/linux-cifs/cifs-utils/%{name}-%{version}.tar.bz2.asc
Patch0:		FORTIFY_SOURCE_ftrunkate.patch

BuildRequires:	libtool
BuildRequires:	samba-winbind
BuildRequires:	acl-devel
BuildRequires:	keyutils-devel
BuildRequires:	krb5-devel
BuildRequires:	pkgconfig(libcap-ng)
BuildRequires:	pkgconfig(talloc)
BuildRequires:	pkgconfig(wbclient)
Requires:       keyutils
Suggests:	sudo nss_wins
Provides:	mount-cifs = %{version}

%description
Tools for Managing Linux CIFS Client Filesystems.

%prep

%setup -q

# remove -Werror
perl -pi -e "s|-Werror||g" Makefile*

%build
%serverbuild
rm -rf autom4te.cache
autoreconf -fi
%configure2_5x \
	--sbindir=/sbin

%make

%install
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
%{_bindir}/getcifsacl
%{_bindir}/setcifsacl

/sbin/cifs.upcall
/sbin/mount.cifs
/sbin/cifs.idmap
/bin/mount.cifs
/bin/umount.cifs

%{_mandir}/man8/cifs.upcall.8*
%{_mandir}/man8/mount.cifs.8*
%{_mandir}/man8/cifs.idmap.8*
%{_mandir}/man1/cifscreds.1*
%{_mandir}/man1/getcifsacl.1*
%{_mandir}/man1/setcifsacl.1*

