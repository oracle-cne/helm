{{{$version := printf "%s.%s.%s" .major .minor .patch}}}
%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif
%{!?registry: %global registry container-registry.oracle.com/olcne}

%global app_name helm
%global app_version {{{$version}}}
%global oracle_release_version 1.0.1

Name:           %{app_name}-container-image
Version:        %{app_version}
Release:        %{oracle_release_version}%{?dist}
BuildArch:      x86_64
Summary:        The package manager for Kubernetes 
License:        Apache-2.0
Group:          System/Management
Url:            https://github.com/kubernetes/helm
Vendor:         Oracle America
Source:         %{name}-%{version}.tar.bz2


%description
The package manager for Kubernetes

Helm helps you manage Kubernetes applications —
Helm Charts helps you define, install, and upgrade
even the most complex Kubernetes application.

Charts are easy to create, version, share, and publish —
so start using Helm and stop the copy-and-paste madness.


%prep
%setup -n %{name}-%{version}


%build
%if "%{app_version}" < "3.0.0"
for package in helm tiller rudder; do
  %global rpm_name ${package}-%{version}-%{release}.%{_build_arch}
  yumdownloader --destdir=${PWD}/rpms %{rpm_name}
  
  ls -ltr ${PWD}/rpms

  %global docker_tag %{registry}/${package}:v%{version}
  docker build --pull --build-arg https_proxy=${https_proxy} --build-arg PRODUCT=${package} --build-arg VERSION=%{version} --build-arg RELEASE=%{release} --build-arg PLATFORM=%{_build_arch} -t %{docker_tag} -f ./olm/builds/Dockerfile.${package} .
  docker save -o ${package}.tar %{docker_tag}
done
%else
%global rpm_name %{app_name}-%{version}-%{release}.%{_build_arch}
yumdownloader --destdir=${PWD}/rpms %{rpm_name}

ls -ltr ${PWD}/rpms

%global docker_tag %{registry}/%{app_name}:v%{version}
docker build --pull --build-arg https_proxy=${https_proxy} --build-arg PRODUCT=%{app_name} --build-arg VERSION=%{version} --build-arg RELEASE=%{release} --build-arg PLATFORM=%{_build_arch} -t %{docker_tag} -f ./olm/builds/Dockerfile.helm .
docker save -o %{app_name}.tar %{docker_tag}
%endif


%install
install -D -m 755 %{app_name}.tar %{buildroot}/usr/local/share/olcne/%{app_name}.tar
%if "%{app_version}" < "3.0.0"
for package in tiller rudder; do
  install -D -m 755 ${package}.tar %{buildroot}/usr/local/share/olcne/${package}.tar
done
%endif


%files
%license LICENSE
/usr/local/share/olcne/*.tar


%changelog
* {{{.changelog_timestamp}}} - %{version}-%{oracle_release_version}
- Added Oracle Specific Build Files for helm related container-images
