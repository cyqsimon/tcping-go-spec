%global debug_package %{nil}
%global _prj_name tcping

Name:           tcping-go
Version:        2.6.0
Release:        4%{?dist}
Summary:        Ping TCP ports using tcping. Inspired by Linux's ping utility. Written in Go
Provides:       tcping
# EPEL 8 has tcping, a C implementation that does the same thing
Conflicts:      tcping

License:        MIT
URL:            https://github.com/pouriyajamshidi/tcping
Source0:        %{url}/archive/v%{version}.tar.gz
Patch0:         no-debian-build.patch

BuildRequires:  curl gcc git make tar

%description
A cross-platform ping program for TCP ports inspired by the Linux's ping
utility. This program will send TCP probes to an IP address or a hostname
specified by you and prints the results. It supports both IPv4 and IPv6.

%prep
%autosetup -n %{_prj_name}-%{version} -p1

# Use latest official stable Go build
_GO_VER="$(curl -Lf https://golang.org/VERSION?m=text | head -n1)"
%ifarch x86_64
    _ARCH=amd64
%endif
%ifarch aarch64
    _ARCH=arm64
%endif
if [[ -z "${_ARCH}" ]]; then
    echo "Unsupported architecture!"
    exit 1
fi
_GO_DL_NAME="${_GO_VER}.linux-${_ARCH}.tar.gz"
_GO_DL_URL="https://go.dev/dl/${_GO_DL_NAME}"

curl -Lfo "${_GO_DL_NAME}" "${_GO_DL_URL}"
tar -xf "${_GO_DL_NAME}"
# bins in go/bin

%build
_GO_BIN_DIR=$(realpath "go/bin")
export PATH="${_GO_BIN_DIR}:${PATH}"

make create_dirs build_linux_static
tar -xf executables/tcping_Linux_static.tar.gz

%check
_GO_BIN_DIR=$(realpath "go/bin")
export PATH="${_GO_BIN_DIR}:${PATH}"

make test

%install
# bin
mkdir -p %{buildroot}%{_bindir}
install -Dpm 755 -t %{buildroot}%{_bindir} %{_prj_name}

%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/%{_prj_name}

%changelog
* Mon Oct 07 2024 cyqsimon - 2.6.0-4
- Fix binary install source

* Mon Oct 07 2024 cyqsimon - 2.6.0-3
- Manually patch out `make build_debian_package` in Makefile
  - See https://github.com/pouriyajamshidi/tcping/issues/242

* Sun Oct 06 2024 cyqsimon - 2.6.0-2
- Always use latest official stable Go build
- Use make target `build_linux_static`

* Sun Oct 06 2024 cyqsimon - 2.6.0-1
- Release 2.6.0

* Wed Feb 28 2024 cyqsimon - 2.5.0-2
- Declare conflict with `tcping`

* Wed Feb 28 2024 cyqsimon - 2.5.0-1
- Release 2.5.0
