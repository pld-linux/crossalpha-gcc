Summary:	Cross ALPHA GNU binary utility development utilities - gcc
Summary(es):	Utilitarios para desarrollo de binarios de la GNU - ALPHA gcc
Summary(fr):	Utilitaires de développement binaire de GNU - ALPHA gcc
Summary(pl):	Skro¶ne narzêdzia programistyczne GNU dla ALPHA - gcc
Summary(pt_BR):	Utilitários para desenvolvimento de binários da GNU - ALPHA gcc
Summary(tr):	GNU geliþtirme araçlarý - ALPHA gcc
Name:		crossalpha-gcc
Version:	3.3.3
Release:	2
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	3c6cfd9fcd180481063b4058cf6faff2
BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:	crossalpha-binutils
BuildRequires:	flex
BuildRequires:	/bin/bash
Requires:	crossalpha-binutils
Requires:	gcc-dirs
ExcludeArch:	alpha
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		alpha-pld-linux
%define		_prefix		/usr
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		_noautostrip	.*libgcc\\.a

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
%setup -q -n gcc-%{version}

%build
rm -rf obj-%{target}
install -d obj-%{target}
cd obj-%{target}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false ../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--disable-shared \
	--enable-haifa \
	--enable-languages="c,c++" \
	--enable-long-long \
	--enable-namespaces \
	--with-gnu-as \
	--with-gnu-ld \
	--with-system-zlib \
	--with-multilib \
	--without-headers \
	--with-newlib \
	--without-x \
	--target=%{target} \
	--host=%{_target_platform} \
	--build=%{_target_platform}

PATH=$PATH:/sbin:%{_sbindir}

cd ..
#LDFLAGS_FOR_TARGET="%{rpmldflags}"

%{__make} -C obj-%{target}
# CC="gcc -DHAVE_DESIGNATED_INITIALIZERS=0" all-gcc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/lib,%{_datadir},%{_bindir},%{gcclib}}

cd obj-%{target}
PATH=$PATH:/sbin:%{_sbindir}

%{__make} -C gcc install \
	prefix=%{_prefix} \
	mandir=%{_mandir} \
	infodir=%{_infodir} \
	gxx_include_dir=$RPM_BUILD_ROOT%{arch}/include/g++ \
	DESTDIR=$RPM_BUILD_ROOT

# c++filt is provided by binutils
#rm -f $RPM_BUILD_ROOT%{_bindir}/i386-mipsel-c++filt

# what is this there for???
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

# the same... make hardlink
#ln -f $RPM_BUILD_ROOT%{arch}/bin/gcc $RPM_BUILD_ROOT%{_bindir}/%{target}-gcc

%{target}-strip -g $RPM_BUILD_ROOT%{gcclib}/libgcc.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-gcc
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-g++
%attr(755,root,root) %{_bindir}/%{target}-c++
#%dir %{arch}/bin
#%attr(755,root,root) %{arch}/bin/cpp
#%attr(755,root,root) %{arch}/bin/gcc
#%attr(755,root,root) %{arch}/bin/gcov
#%%{arch}/include/_G_config.h
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/cc1plus
##%attr(755,root,root) %{gcclib}/tradcpp0
##%attr(755,root,root) %{gcclib}/cpp0
%attr(755,root,root) %{gcclib}/collect2
#%%{gcclib}/SYSCALLS.c.X
%{gcclib}/libgcc.a
%{gcclib}/specs*
%dir %{gcclib}/include
%{gcclib}/include/*.h
#%%{gcclib}/include/iso646.h
#%%{gcclib}/include/limits.h
#%%{gcclib}/include/proto.h
#%%{gcclib}/include/stdarg.h
#%%{gcclib}/include/stdbool.h
#%%{gcclib}/include/stddef.h
#%%{gcclib}/include/syslimits.h
#%%{gcclib}/include/varargs.h
#%%{gcclib}/include/va-*.h
%{_mandir}/man1/%{target}-gcc.1*
