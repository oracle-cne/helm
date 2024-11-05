{{{$version := printf "%s.%s.%s" .major .minor .patch}}}
%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif
%global golang_version 1.22.8
%global _buildhost build-ol%{?oraclelinux}-%{?_arch}.oracle.com

%global app_name helm
%global app_version {{{$version}}}
%global oracle_release_version 1

Name:           %{app_name}
Version:        %{app_version}
Release:        %{oracle_release_version}%{?dist}
Summary:        The package manager for Kubernetes
License:        Apache-2.0
Group:          System/Management
Url:            https://github.com/kubernetes/helm
Vendor:         Oracle America
Source:         helm-%{version}.tar.bz2
BuildRequires:  golang >= %{golang_version}
Requires:	    ca-certificates

%description
The package manager for Kubernetes. Helm helps you manage Kubernetes applications — Helm Charts helps you define, install, and upgrade even the most complex Kubernetes application.
Charts are easy to create, version, share, and publish — so start using Helm and stop the copy-and-paste madness.

%prep
%setup -q -n helm-%{version}
mkdir -p src/k8s.io/helm
mv $(ls | grep -v "^src$") src/k8s.io/helm

%build
export GOPATH=$(pwd)
pushd src/k8s.io/helm
go version
make GIT_TAG=v%{app_version} GIT_DIRTY=clean
popd

%install
pushd src/k8s.io/helm
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} bin/helm
popd
mv src/k8s.io/helm/LICENSE .
mv src/k8s.io/helm/THIRD_PARTY_LICENSES.txt .

%files
%license LICENSE THIRD_PARTY_LICENSES.txt
%{_bindir}/helm

%changelog
* {{{.changelog_timestamp}}} - {{{$version}}}-1
- Added Oracle Specific build Files
