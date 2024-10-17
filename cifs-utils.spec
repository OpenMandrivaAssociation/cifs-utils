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
Version:	7.1
License:	GPLv3
Group:		Networking/Other
Release:	1
URL:		https://www.samba.org/linux-cifs/cifs-utils/
Source0:	http://download.samba.org/pub/linux-cifs/cifs-utils/%{name}-%{version}.tar.bz2
Source1:	http://download.samba.org/pub/linux-cifs/cifs-utils//%{name}-%{version}.tar.bz2.asc
Source2:	http://download.samba.org/pub/linux-cifs/cifs-utils/cifs-utils-pubkey_70F3B981.asc
BuildRequires:	autoconf automake libtool
BuildRequires:	pkgconfig(talloc)
BuildRequires:	pkgconfig(libcap-ng)
BuildRequires:	keyutils-devel
BuildRequires:	krb5-devel
BuildRequires:	pkgconfig(wbclient)
BuildRequires:	samba-winbind
BuildRequires:	gnupg
BuildRequires:	pam-devel
BuildRequires:	python-docutils
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

%package -n pam_cifscreds
Summary:        PAM module to manage NTLM credentials in kernel keyring
Group:          Networking/Other

%description -n pam_cifscreds
The pam_cifscreds PAM module is a tool for automatically adding
credentials (username and password) for the purpose of establishing
sessions in multiuser mounts.

When a cifs filesystem is mounted with the "multiuser" option, and does
not use krb5 authentication, it needs to be able to get the credentials
for each user from somewhere. The pam_cifscreds module can be used to
provide these credentials to the kernel automatically at login.

%prep
#check_sig %{SOURCE2} %{SOURCE1} %{SOURCE0}

%autosetup -p1

%build
%serverbuild
%configure \
	--sbindir=%{_bindir} \
	--enable-cifsacl \
	--enable-cifsidmap

%make_build

%install
# "make install" places compat symlinks there.
# We can wipe them later, but "make install"
# fails if the directory isn't there
mkdir -p %{buildroot}/sbin
%make_install

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
ln -s %{_libdir}/%{name}/idmapwb.so %{buildroot}%{_sysconfdir}/%{name}/idmap-plugin
mkdir -p %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.idmap.conf %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.spnego.conf %{buildroot}%{_sysconfdir}/request-key.d
cp contrib/request-key.d/README contrib/request-key.d/README.keyutils-1.5.5

mv %{buildroot}/sbin/* %{buildroot}%{_bindir}
rmdir %{buildroot}/sbin

%files
%doc AUTHORS README doc/linux-cifs-client-guide.odt contrib/request-key.d/README.keyutils-1.5.5
%config(noreplace) %{_sysconfdir}/%{name}/idmap-plugin
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.idmap.conf
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.spnego.conf
%{_bindir}/cifscreds
%{_bindir}/*etcifsacl
%{_bindir}/smbinfo
%{_bindir}/smb2-quota
%{_bindir}/cifs.upcall
%{_bindir}/cifs.idmap
%{_bindir}/mount.cifs
%{_bindir}/mount.smb3

%{_libdir}/%{name}/idmapwb.so
%doc %{_mandir}/man8/cifs.upcall.8*
%doc %{_mandir}/man8/cifs.idmap.8*
%doc %{_mandir}/man8/mount.cifs.8*
%doc %{_mandir}/man8/idmapwb.8*
%doc %{_mandir}/man1/*etcifsacl.1*
%doc %{_mandir}/man1/cifscreds.1*
%doc %{_mandir}/man1/smbinfo.1*
%doc %{_mandir}/man1/smb2-quota.1.*
%doc %{_mandir}/man8/mount.smb3.8.*


%files devel
%{_includedir}/cifsidmap.h

%files -n pam_cifscreds
%{_libdir}/security/pam_cifscreds.so
%doc %{_mandir}/man8/pam_cifscreds.8.*
