%global commit0 3ecf1d7dad74e39d65852b78531b79e2a7e72b5b
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}


%global pa_major   12.2

# webrtc bits go wonky without this
# see also https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/JQQ66XJSIT2FGTK2YQY7AXMEH5IXMPUX/
%undefine _strict_symbol_defs_build
%global with_webrtc 1

# https://bugzilla.redhat.com/983606
%global _hardened_build 1

## support systemd activation
%global systemd 1
## enable systemd activation by default (instead of autospawn)
%if 0%{?fedora} > 27
%global systemd_activation 1
## TODO: ship preset to explicitly disable .service, enable .socket
%else
# gdm-hooks moved to gdm packaging f28+
%global gdm_hooks 1
%endif

## comment to disable tests
%global tests 1


Name:           pulseaudio-module-bluetooth
Summary:        Bluetooth support for the PulseAudio sound server and extra codecs
Version:        %{pa_major}%{?pa_minor:.%{pa_minor}}
Release:        10%{?dist}
License:        LGPLv2+
URL:            http://www.freedesktop.org/wiki/Software/PulseAudio
Source0:	https://github.com/EHfive/pulseaudio-modules-bt/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:	pulseaudio-module-bluetooth-snapshot

BuildRequires:  automake libtool
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:	ffmpeg-devel
BuildRequires:	fdk-aac-free-devel 
BuildRequires:	pulseaudio-libs-devel >= %{version}
BuildRequires:	pulseaudio >= %{version}
BuildRequires:	ldacbt-devel >= 2.0.2.3
BuildRequires:	cmake
BuildRequires:	git
%global bash_completionsdir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null || echo '/etc/bash_completion.d')
BuildRequires:  m4
BuildRequires:  libtool-ltdl-devel
BuildRequires:  intltool
BuildRequires:  pkgconfig
BuildRequires:  doxygen
BuildRequires:  xmltoman
# https://bugzilla.redhat.com/show_bug.cgi?id=1518777
%if 0%{?tcpwrap}
BuildRequires:  tcp_wrappers-devel
%endif
BuildRequires:  libsndfile-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk2-devel
BuildRequires:  GConf2-devel
BuildRequires:  avahi-devel
%if 0%{?fedora}
%global enable_lirc 1
%global enable_jack 1
%endif
BuildRequires:  libatomic_ops-static, libatomic_ops-devel
BuildRequires:  pkgconfig(bluez) >= 5.0
BuildRequires:  sbc-devel
BuildRequires:  libXt-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  libXtst-devel
BuildRequires:  libXi-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  libICE-devel
BuildRequires:  xcb-util-devel
BuildRequires:  openssl-devel
BuildRequires:  orc-devel
BuildRequires:  libtdb-devel
%if 0%{?fedora}
BuildRequires:  pkgconfig(soxr)
%endif
BuildRequires:  pkgconfig(speexdsp) >= 1.2
BuildRequires:  libasyncns-devel
%if 0%{?systemd}
BuildRequires:  systemd-devel >= 184
BuildRequires:  systemd
%endif
%if 0%{?systemd_activation}
%{?systemd_requires}
%endif
BuildRequires:  dbus-devel
BuildRequires:  libcap-devel
BuildRequires:  pkgconfig(fftw3f)
%if 0%{?with_webrtc}
BuildRequires:  pkgconfig(webrtc-audio-processing) >= 0.2
%endif
%if 0%{?tests}
BuildRequires:  pkgconfig(check)
%endif

Requires:       pulseaudio >= %{version}
Requires:       bluez >= 5.0 
Requires:	ffmpeg
Recommends:	fdk-aac-free
Requires:	ldacbt
Provides:	pulseaudio-module-bluetooth-aptx 

%description
Contains Bluetooth audio (A2DP/HSP/HFP) support for the PulseAudio sound server.
Includes support for APTX, APTX-HD, AAC codecs, SBC, Sony LDAC (A2DP codec).


%prep
%{S:1} -c %{commit0}
%setup -T -D -n %{name}-%{shortcommit0} 

%build

%cmake -DCMAKE_BUILD_TYPE=Release \
       -DFORCE_NOT_BUILD_LDAC=ON .

%make_build

%install
%make_install

%check
ctest -V %{?_smp_mflags}

%post
%{?ldconfig}
%ldconfig_postun

%files
%{_libdir}/pulse-%{pa_major}/modules/libbluez*-util.so
%{_libdir}/pulse-%{pa_major}/modules/module-bluez*-device.so
%{_libdir}/pulse-%{pa_major}/modules/module-bluez*-discover.so
%{_libdir}/pulse-%{pa_major}/modules/module-bluetooth-discover.so
%{_libdir}/pulse-%{pa_major}/modules/module-bluetooth-policy.so


%changelog

* Tue Aug 13 2019 - David Va <davidva AT tuta DOT io> 12.2-10
- A2DP_SINK_AAC sbc to aac

* Sat Jun 22 2019 - David Va <davidva AT tuta DOT io> 12.2-9
- Changed to fdk-aac-free

* Tue Feb 19 2019 - David Va <davidva AT tuta DOT io> 12.2-8
- Rebuilt for ldacbt

* Wed Jan 30 2019 - David Va <davidva AT tuta DOT io> 12.2-7
- Initial build
