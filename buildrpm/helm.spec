
%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif
%global golang_version 1.22.8
%global _buildhost build-ol%{?oraclelinux}-%{?_arch}.oracle.com

%global app_name helm
%global app_version 4.0.2
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
make GIT_TAG=v%{app_version} GIT_DIRTY=clean GOFLAGS="-trimpath=false" VERSION="v%{app_version}" VERSION_METADATA="v%{app_version}" EXT_LDFLAGS="-X main.version=v%{app_version}"
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
* Thu Dec 11 2025 Oracle Cloud Native Environment Authors <noreply@oracle.com> - 4.0.2-1
- Added Oracle Specific build Files
