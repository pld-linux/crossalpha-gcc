Summary:	Cross ALPHA GNU binary utility development utilities - gcc
Summary(es):	Utilitarios para desarrollo de binarios de la GNU - ALPHA gcc
Summary(fr):	Utilitaires de développement binaire de GNU - ALPHA gcc
Summary(pl):	Skro¶ne narzêdzia programistyczne GNU dla ALPHA - gcc
Summary(pt_BR):	Utilitários para desenvolvimento de binários da GNU - ALPHA gcc
Summary(tr):	GNU geliþtirme araçlarý - ALPHA gcc
Name:		crossalpha-gcc
Version:	3.4.3
Release:	2
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	e744b30c834360fccac41eb7269a3011
%define		_llh_ver	2.6.9.1
Source1:	http://ep09.pld-linux.org/~mmazur/linux-libc-headers/linux-libc-headers-%{_llh_ver}.tar.bz2
# Source1-md5:	d3507b2c0203a0760a677022badcf455
Source2:	glibc-20041030.tar.bz2
# Source2-md5:	4e14871efd881fbbf523a0ba16175bc7
URL:		http://gcc.gnu.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	crossalpha-binutils
BuildRequires:	flex
BuildRequires:	/bin/bash
Requires:	crossalpha-binutils
Requires:	gcc-dirs
ExcludeArch:	alpha
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		alpha-pld-linux
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_libdir}/gcc/%{target}
%define		gcclib		%{gccarch}/%{version}

%define		_noautostrip	.*%{gcclib}.*/libgc.*\\.a

%description
This package contains a cross-gcc which allows the creation of
binaries to be run on ALPHA linux (architecture alpha-linux) on
i386-machines.

%description -l de
Dieses Paket enthält einen Cross-gcc, der es erlaubt, auf einem
i386-Rechner Code für alpha-Linux zu generieren.

%description -l pl
Ten pakiet zawiera skro¶ny gcc pozwalaj±cy na robienie na maszynach
i386 binariów do uruchamiania na ALPHA (architektura "alpha-linux").

%prep
%setup -q -n gcc-%{version} -a1 -a2

%build
FAKE_ROOT=$PWD/fake-root

rm -rf $FAKE_ROOT && install -d $FAKE_ROOT/usr/include
cp -r linux-libc-headers-%{_llh_ver}/include/{asm-alpha,linux} $FAKE_ROOT/usr/include
ln -s asm-alpha $FAKE_ROOT/usr/include/asm

cd libc
rm -rf builddir && install -d builddir && cd builddir
../configure \
	--prefix=$FAKE_ROOT/usr \
	--build=%{_target_platform} \
	--host=%{target} \
	--disable-nls \
	--with-headers=$FAKE_ROOT/usr/include \
	--disable-sanity-checks \
	--enable-hacker-mode

%{__make} sysdeps/gnu/errlist.c
%{__make} install-headers

install bits/stdio_lim.h $FAKE_ROOT/usr/include/bits
touch $FAKE_ROOT/usr/include/gnu/stubs.h
cd ../..

rm -rf obj-%{target}
install -d obj-%{target}
cd obj-%{target}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--disable-shared \
	--disable-threads \
	--enable-languages="c" \
	--enable-c99 \
	--enable-long-long \
	--with-gnu-as \
	--with-gnu-ld \
	--with-system-zlib \
	--with-multilib \
	--with-sysroot=$FAKE_ROOT \
	--without-x \
	--target=%{target} \
	--host=%{_target_platform} \
	--build=%{_target_platform}

%{__make} all-gcc

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C obj-%{target} install-gcc \
	DESTDIR=$RPM_BUILD_ROOT

# don't want this here
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

%if 0%{!?debug:1}
%{target}-strip -g $RPM_BUILD_ROOT%{gcclib}/libgcc.a
%{target}-strip -g $RPM_BUILD_ROOT%{gcclib}/libgcov.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-gcc
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%{gcclib}/crt*.o
%{gcclib}/libgcc.a
%{gcclib}/specs*
%dir %{gcclib}/include
%{gcclib}/include/*.h
%{_mandir}/man1/%{target}-cpp.1*
%{_mandir}/man1/%{target}-gcc.1*
