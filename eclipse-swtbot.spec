%{?scl:%scl_package eclipse-swtbot}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 2

Name:           %{?scl_prefix}eclipse-swtbot
Version:        2.4.0
Release:        3.%{baserelease}%{?dist}
Summary:        UI and functional testing tool for SWT and Eclipse based applications

License:        EPL
URL:            http://www.eclipse.org/swtbot/
Source0:        http://git.eclipse.org/c/swtbot/org.eclipse.swtbot.git/snapshot/org.eclipse.swtbot-%{version}.tar.xz
BuildRequires:  %{?scl_prefix}tycho
BuildRequires:  %{?scl_prefix}tycho-extras
BuildRequires:  %{?scl_prefix}eclipse-gef
BuildRequires:  %{?scl_prefix}eclipse-pde
BuildRequires:  %{?scl_prefix}cbi-plugins
BuildRequires:  %{?scl_prefix}eclipse-license
BuildRequires:  %{?scl_prefix}tycho
BuildRequires:  %{?scl_prefix_java_common}log4j
BuildRequires:  %{?scl_prefix_java_common}hamcrest
BuildArch:      noarch

Patch0: junit_less_than_412.patch

%description
SWTBot is a Java based UI/functional testing tool for testing SWT and Eclipse
based applications. SWTBot provides APIs that are simple to read and write.
The APIs also hide the complexities involved with SWT and Eclipse. This makes
it suitable for UI/functional testing by everyone, not just developers.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n org.eclipse.swtbot-%{version}

%patch0

for j in $(find -name \*.jar); do
if [ ! -L $j ] ; then
rm -fr $j
fi
done
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId ='target-platform-configuration']"
%pom_remove_plugin org.jacoco:jacoco-maven-plugin
%pom_remove_plugin org.eclipse.tycho:tycho-packaging-plugin
%pom_disable_module org.eclipse.swtbot.updatesite
%pom_disable_module org.eclipse.swtbot.nebula.gallery
%pom_disable_module org.eclipse.swtbot.nebula.gallery.finder
%pom_disable_module org.eclipse.swtbot.nebula.gallery.finder.test

%mvn_package ":*.test" __noinstall
%mvn_package ":*.test.*" __noinstall
%mvn_package ":*.{examples,demo}" __noinstall
%mvn_package "::jar:sources:"
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_build -j -f
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles

%changelog
* Thu Jul 28 2016 Mat Booth <mat.booth@redhat.com> - 2.4.0-3.2
- Add patch for older version of junit

* Thu Jul 28 2016 Mat Booth <mat.booth@redhat.com> - 2.4.0-3.1
- Auto SCL-ise package for rh-eclipse46 collection

* Thu Jul 28 2016 Mat Booth <mat.booth@redhat.com> - 2.4.0-3
- Drop unnecessary BR on jacoco

* Tue May 03 2016 Mat Booth <mat.booth@redhat.com> - 2.4.0-2
- Don't ship demo project as it requires examples that are not shipped

* Wed Apr 27 2016 Alexander Kurtakov <akurtako@redhat.com> 2.4.0-1
- Update to upstream 2.4.0.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 14 2015 Roland Grunberg <rgrunber@redhat.com> - 2.3.0-2
- Rebuild as an Eclipse p2 Droplet.

* Wed Jun 24 2015 Alexander Kurtakov <akurtako@redhat.com> 2.3.0-1
- Update to upstream 2.3.0.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 9 2015 Alexander Kurtakov <akurtako@redhat.com> 2.2.1-5
- Add BR on full hamcrest now that platform depend only on part of it.

* Fri Feb  6 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-4
- Rebuild to generate missing OSGi auto-requires

* Wed Dec 3 2014 Alexander Kurtakov <akurtako@redhat.com> 2.2.1-3
- Build with xmvn.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 4 2014 Alexander Kurtakov <akurtako@redhat.com> 2.2.1-1
- Update to upstream 2.2.1 release.

* Mon Aug 12 2013 Alexander Kurtakov <akurtako@redhat.com> 2.1.1-1
- Update to latest upstream version.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 19 2013 Alexander Kurtakov <akurtako@redhat.com> 2.1.0-1
- Update to the official release.

* Tue Feb 26 2013 Alexander Kurtakov <akurtako@redhat.com> 2.1.0-0.2.20130226git
- New snapshot removing org.junit4 references.

* Tue Feb 26 2013 Alexander Kurtakov <akurtako@redhat.com> 2.1.0-0.1.20130225git
- Update to 2.1.0 prerelease - compatible with kepler platform.

* Wed Feb 20 2013 Alexander Kurtakov <akurtako@redhat.com> 2.0.5-4.20120802git
- Skip tycho version check.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-3.20120802git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 6 2012 Alexander Kurtakov <akurtako@redhat.com> 2.0.5-2.20120802git
- Fix review comments.

* Thu Aug 2 2012 Alexander Kurtakov <akurtako@redhat.com> 2.0.5-1.gita95f41b7ae6d7790dab36bca982d4b833fd2662d
- Initial package
