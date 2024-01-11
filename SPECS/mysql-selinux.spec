# defining macros needed by SELinux
%global selinuxtype targeted
%global moduletype contrib
%global modulename mysql

Name:           mysql-selinux
Version:        1.0.5
Release:        1%{?dist}

License:        GPLv3
URL:            https://github.com/devexp-db/mysql-selinux
Summary:        SELinux policy modules for MySQL and MariaDB packages

Source0:        https://github.com/devexp-db/mysql-selinux/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  selinux-policy-devel
Requires(post): policycoreutils
%{?selinux_requires}

%description
SELinux policy modules for MySQL and MariaDB packages.


%prep
%setup -q -n %{name}-%{version}

%build
make

%install
# install policy modules
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 0644 %{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages


%pre
%selinux_relabel_pre -s %{selinuxtype}

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{modulename}.pp.bz2 || :

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename} || :
fi

%posttrans
%selinux_relabel_post -s %{selinuxtype} || :


%files
%defattr(-,root,root,0755)
%attr(0644,root,root) %{_datadir}/selinux/packages/%{modulename}.pp.bz2
%ghost %verify(not mode md5 size mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}
%license COPYING

%changelog
* Thu Jun 09 2022 Michal Schorm <mschorm@redhat.com> - 1.0.5-1
- Rebase to 1.0.5

* Fri Mar 18 2022 Lukas Javorsky <ljavorsk@redhat.com> - 1.0.4-1
- Rebase to 1.0.4
- Unintentional removal of semicolon

* Fri Mar 18 2022 Lukas Javorsky <ljavorsk@redhat.com> - 1.0.3-1
- Rebase to 1.0.3
- Remove setuid/setgid capabilities from mysqld_t type.

* Thu Jan 10 2022 Lukas Javorsky <ljavorsk@redhat.com> - 1.0.2-6
- Fix the gating.yaml file so it checks the correct tests

* Thu Apr 22 2021 Lukas Javorsky <ljavorsk@redhat.com> - 1.0.2-5
- Fix rpm verification it's a ghost file so it should ignore the error

* Mon Dec 07 2020 Honza Horak <hhorak@redhat.com> - 1.0.2-4
- Rebuild for added tmt gating
  Related: #1895021

* Wed Dec 02 2020 Michal Schorm <mschorm@redhat.com> - 1.0.2-1
- Rebase to 1.0.2 release
  Added context for "*mariadb*" named executables

* Tue Dec 01 2020 Michal Schorm <mschorm@redhat.com> - 1.0.1-1
- Rebase to 1.0.1 release
  This release is just a sync-up with upstream selinux-policy
- URL changed to a new upstream repository

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Kevin Fenzi <kevin@scrye.com> - 1.0.0-7
- Also make sure posttrans does not fail.

* Thu Jan 10 2019 Kevin Fenzi <kevin@scrye.com> - 1.0.0-6
- Add Requires(post) on policycoreutils for semodule and make sure post/postun cannot fail

* Thu Dec 06 2018 Jakub Janco <jjanco@redhat.com> - 1.0.0-5
- Sync with upstream

* Wed Aug 29 2018 Jakub Janco <jjanco@redhat.com> - 1.0.0-4
- Allow mysqld sys_nice capability

* Mon Aug 20 2018 Jakub Janco <jjanco@redhat.com> - 1.0.0-3
- reflect latest changes of mysql policy

* Fri Jul 27 2018 Jakub Janco <jjanco@redhat.com> - 1.0.0-2
- reflect latest changes of Independent Product Policy

* Wed Jul 18 2018 Jakub Janco <jjanco@redhat.com> - 1.0.0-1
- First Build

