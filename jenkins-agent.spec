################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _opt              /opt
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock/subsys
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _crondir          %{_sysconfdir}/cron.d
%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libdir32     %{_loc_exec_prefix}/%{_lib32}
%define _loc_libdir64     %{_loc_exec_prefix}/%{_lib64}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _loc_mandir       %{_loc_datarootdir}/man
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig
%define __ldconfig        %{_sbin}/ldconfig
%define __groupadd        %{_sbindir}/groupadd
%define __useradd         %{_sbindir}/useradd
%define __systemctl       %{_bindir}/systemctl

################################################################################

%define service_user  jenkins
%define service_group jenkins
%define service_home  /var/lib/jenkins

################################################################################

Summary:         Utility for executing Jenkins Agent dynamically
Name:            jenkins-agent
Version:         1.0.0
Release:         0%{?dist}
License:         MIT
Group:           Development/Tools
URL:             https://github.com/gongled/jenkins-agent

Source0:         https://github.com/gongled/%{name}/archive/v%{version}.tar.gz

BuildArch:       noarch
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:        bash wget

Provides:        %{name} = %{version}-%{release}

################################################################################

%description
Utility for executing Jenkins Agent dynamically.

################################################################################

%prep
%setup -q

%build
%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -dm 755 %{buildroot}%{_unitdir}

install -pm 755 SOURCES/%{name} %{buildroot}%{_bindir}/
install -pm 640 SOURCES/%{name}.conf %{buildroot}%{_sysconfdir}/%{name}/
install -pm 644 SOURCES/%{name}@.service %{buildroot}%{_unitdir}/

%clean
rm -rf %{buildroot}

################################################################################

%pre
getent group %{service_group} >/dev/null || groupadd -r %{service_group}
getent passwd %{service_user} >/dev/null || \
    useradd -r -M -g %{service_group} -d %{service_home} \
            -s /sbin/nologin %{service_user}
exit 0

%postun
if [[ $1 -ge 1 ]] ; then
    %{__systemctl} daemon-reload &>/dev/null || :
fi

################################################################################

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_bindir}/%{name}
%config(noreplace) %attr(0640,root,%{service_group}) %{_sysconfdir}/%{name}/%{name}.conf
%{_unitdir}/%{name}@.service

################################################################################

%changelog
* Mon Nov 11 2019 Gleb Goncharov <inbox@gongled.ru> - 1.0.0-0
- Initial build
