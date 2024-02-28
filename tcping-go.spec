%global debug_package %{nil}

Name:           tcping-go
Version:        2.5.0
Release:        1%{?dist}
Summary:        Ping TCP ports using tcping. Inspired by Linux's ping utility. Written in Go
Provides:       tcping

License:        MIT
URL:            https://github.com/pouriyajamshidi/tcping
Source0:        https://github.com/pouriyajamshidi/tcping/archive/v%{version}.tar.gz

BuildRequires:  golang make tar

%description
A cross-platform ping program for TCP ports inspired by the Linux's ping
utility. This program will send TCP probes to an IP address or a hostname
specified by you and prints the results. It supports both IPv4 and IPv6.

%prep
%autosetup

%build
make build_linux_static
tar -xf executables/tcping_Linux_static.tar.gz

%check
make test

%install
# bin
mkdir -p %{buildroot}%{_bindir}
install -Dpm 755 -t %{buildroot}%{_bindir} executables/tcping

%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/tcping

%changelog
* Wed Feb 28 2024 cyqsimon - 2.5.0-1
- Release 2.5.0