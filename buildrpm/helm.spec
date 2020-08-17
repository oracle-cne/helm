{{{$version := printf "%s.%s.%s" .major .minor .patch}}}
%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global app_name helm
%global app_version {{{$version}}}
%global oracle_release_version 1.0.1

Name:           %{app_name}
Version:        %{app_version}
Release:        %{oracle_release_version}%{?dist}
BuildArch:      x86_64
Summary:        The package manager for Kubernetes 
License:        Apache-2.0
Group:          System/Management
Url:            https://github.com/kubernetes/helm
Vendor:         Oracle America
Source:         helm-%{version}.tar.bz2
BuildRequires:  golang >= 1.13.15
BuildRequires:	glide
BuildRequires:	mercurial
Requires:	ca-certificates
Requires:	kubectl

#%{?systemd_requires}

%description
The package manager for Kubernetes

Helm helps you manage Kubernetes applications — 
Helm Charts helps you define, install, and upgrade 
even the most complex Kubernetes application.

Charts are easy to create, version, share, and publish — 
so start using Helm and stop the copy-and-paste madness.

%if "%{app_version}" < "3.0.0"
%package -n rudder 
Summary:  RESTful API for Helm Repositories and the Tiller service
Requires: ca-certificates
Requires: kubectl

%description -n rudder
RESTful API for Helm Repositories and the Tiller service

%package -n tiller 
Summary:  Manages installation of charts inside k8s cluster
Requires: ca-certificates
Requires: kubectl

%description -n tiller
Manages installation of charts inside k8s cluster
%endif

%prep
%setup -q -n helm-%{version}
mkdir -p src/k8s.io/helm
mv $(ls | grep -v "^src$") src/k8s.io/helm

%build
export GOPATH=$(pwd)
pushd src/k8s.io/helm
glide cache-clear
%if "%{app_version}" < "3.0.0"
make bootstrap build
%else
make
%endif
popd

%install
pushd src/k8s.io/helm
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} bin/helm
%if "%{app_version}" < "3.0.0"
install -p -m 755 -t %{buildroot}%{_bindir} bin/tiller
install -p -m 755 -t %{buildroot}%{_bindir} bin/protoc-gen-go
install -p -m 755 -t %{buildroot}%{_bindir} bin/rudder
%endif
popd
mv src/k8s.io/helm/LICENSE .
mv src/k8s.io/helm/THIRD_PARTY_LICENSES.txt .

%files
%license LICENSE THIRD_PARTY_LICENSES.txt
%{_bindir}/helm
%if "%{app_version}" < "3.0.0"
%{_bindir}/tiller
%{_bindir}/protoc-gen-go
%{_bindir}/rudder

%files -n rudder
%license LICENSE THIRD_PARTY_LICENSES.txt
%{_bindir}/rudder

%files -n tiller
%license LICENSE THIRD_PARTY_LICENSES.txt
%{_bindir}/tiller
%endif

%changelog
* {{{.changelog_timestamp}}} - {{{$version}}}-1.0.1
- Added Oracle Specific Build Files for helm
