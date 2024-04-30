# General maintainer notes:
#   Fedora guideliens for packaging of SELinux rules:
#     https://fedoraproject.org/wiki/SELinux/IndependentPolicy
#   RHEL instructions regarding Troubleshooting problems related to SELinux:
#     https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/using_selinux/troubleshooting-problems-related-to-selinux_using-selinux

# defining macros needed by SELinux
%global selinuxtype targeted
%global modulename mysql

Name:           mysql-selinux
Version:        1.0.10
Release:        1%{?dist}

License:        GPLv3
URL:            https://github.com/devexp-db/mysql-selinux
Summary:        SELinux policy modules for MySQL and MariaDB packages

Source0:        https://github.com/devexp-db/mysql-selinux/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  selinux-policy-devel

%{?selinux_requires}
Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}

%description
SELinux policy modules for MySQL and MariaDB packages.


%prep
%setup -q -n %{name}-%{version}

%build
make

%install
# install policy modules
install -d %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}
install -m 0644 %{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}


%pre
%selinux_relabel_pre -s %{selinuxtype}

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
fi

%posttrans
%selinux_relabel_post -s %{selinuxtype}


%files
%defattr(-,root,root,0755)
%attr(0644,root,root) %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2
%ghost %verify(not mode md5 size mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}
%license COPYING

# Note:
#   we do not pack the *.if file as seen in the example:
#     https://fedoraproject.org/wiki/SELinux/IndependentPolicy#The_%prep_and_%install_Section
#   since we do not have any interface to be shared (and even then it is optional)

%changelog
* Sat Nov 18 2023 Packit <hello@packit.dev> - 1.0.10-1
- 2nd attempt to fix rhbz#2186996 rhbz#2221433 rhbz#2245705 (Michal Schorm)
- Resolves rhbz#2250424

* Fri Nov 17 2023 Packit <hello@packit.dev> - 1.0.9-1
- Revert "Attempt to fix rhbz#2186996 rhbz#2221433 rhbz#2245705" This reverts commit de84778e555b891fd9ea5f3111c87a4990650d6c. (Michal Schorm)
- Resolves rhbz#2250360

* Tue Sep 26 2023 Michal Schorm <mschorm@redhat.com> - 1.0.7-2
- Bump release for rebuild

* Thu Sep 14 2023 Packit <hello@packit.dev> - 1.0.7-1
- Empty commit to test Fedora PACKIT configuration for packaging automation (Michal Schorm)

* Wed Jul 12 2023 Adam Dobes <adobes@redhat.com> - 1.0.6-1
- Rebase to 1.0.6

* Thu Jun 09 2022 Michal Schorm <mschorm@redhat.com> - 1.0.5-1
- Rebase to 1.0.5

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.0.4-2
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Tue May 04 2021 Lukas Javorsky <ljavorsk@redhat.com> - 1.0.4-1
- Rebase to 1.0.4
- Fix rpm verification it's a ghost file so it should ignore the error

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 1.0.2-3
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

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

