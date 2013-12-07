%define check_sig() export GNUPGHOME=%{_tmppath}/rpm-gpghome \
if [ -d "$GNUPGHOME" ] \
then echo "Error, GNUPGHOME $GNUPGHOME exists, remove it and try again"; exit 1 \
fi \
install -d -m700 $GNUPGHOME \
gpg --import %{1} \
gpg --trust-model always --verify %{2} %{?3} \
rm -Rf $GNUPGHOME ;\
\

Summary:	Tools for Managing Linux CIFS Client Filesystems
Name:		cifs-utils
Version:	6.1
License:	GPLv3
Group:		Networking/Other
Release:	4
URL:		http://www.samba.org/linux-cifs/cifs-utils/
Source0:	ftp://ftp.samba.org/pub/linux-cifs/cifs-utils/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.samba.org/pub/linux-cifs/cifs-utils/%{name}-%{version}.tar.bz2.asc
Source2:	ftp://ftp.samba.org/pub/linux-cifs/cifs-utils/cifs-utils-pubkey_70F3B981.asc
BuildRequires:	autoconf automake libtool
BuildRequires:	pkgconfig(talloc)
BuildRequires:	pkgconfig(libcap-ng)
BuildRequires:	keyutils-devel
BuildRequires:	krb5-devel
BuildRequires:	pkgconfig(wbclient)
BuildRequires:	samba-winbind
BuildRequires:	gnupg
Suggests:	sudo nss_wins
Provides:	mount-cifs = %{version}
Obsoletes:	mount-cifs <= 5.8
Requires:	keyutils

%description
Tools for Managing Linux CIFS Client Filesystems.

%package	devel
Summary:	Files needed for building plugins for cifs-utils
Group:		Development/C

%description	devel
This package contains the header file necessary for building ID mapping
plugins for cifs-utils.

%prep
%check_sig %{SOURCE2} %{SOURCE1} %{SOURCE0}

%setup -q
%apply_patches

%build
%serverbuild
%configure2_5x \
    --sbindir=/sbin \
    --enable-cifsacl \
    --enable-cifsidmap \

%make

%install
%makeinstall_std
ln -s ../sbin/mount.cifs %{buildroot}%{_bindir}/mount.cifs
# Hack for smb4k
ln -s umount %{buildroot}%{_bindir}/umount.cifs

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
ln -s %{_libdir}/%{name}/idmapwb.so %{buildroot}%{_sysconfdir}/%{name}/idmap-plugin
mkdir -p %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.idmap.conf %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.spnego.conf %{buildroot}%{_sysconfdir}/request-key.d
cp contrib/request-key.d/README contrib/request-key.d/README.keyutils-1.5.5

%files
%doc AUTHORS README doc/linux-cifs-client-guide.odt contrib/request-key.d/README.keyutils-1.5.5
%config(noreplace) %{_sysconfdir}/%{name}/idmap-plugin
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.idmap.conf
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.spnego.conf
%{_bindir}/cifscreds
%{_bindir}/*etcifsacl
/sbin/cifs.upcall
/sbin/cifs.idmap
/sbin/mount.cifs
%{_libdir}/%{name}/idmapwb.so
%{_bindir}/mount.cifs
%{_bindir}/umount.cifs
%{_mandir}/man8/cifs.upcall.8*
%{_mandir}/man8/cifs.idmap.8*
%{_mandir}/man8/mount.cifs.8*
%{_mandir}/man8/idmapwb.8*
%{_mandir}/man1/*etcifsacl.1*
%{_mandir}/man1/cifscreds.1*

%files devel
%{_includedir}/cifsidmap.h
