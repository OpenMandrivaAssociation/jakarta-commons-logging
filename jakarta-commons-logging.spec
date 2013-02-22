# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define base_name  logging
%define short_name commons-%{base_name}
%define section    free
%define gcj_support 0
%bcond_without	bootstrap

Name:           jakarta-%{short_name}
Version:        1.1
Release:        %mkrel 3.3.8
Epoch:          0
Summary:        Jakarta Commons Logging Package
License:        Apache License
Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:            http://jakarta.apache.org/commons/%{base_name}/
Source0:        http://www.apache.org/dist/jakarta/commons/logging/source/commons-logging-%{version}-src.tar.bz2
Patch1:         %{short_name}-eclipse-manifest.patch
BuildRequires:  ant
%if !%{with bootstrap}
BuildRequires:	ant-junit
BuildRequires:  avalon-framework
BuildRequires:  avalon-logkit
%endif
BuildRequires:  java-rpmbuild
BuildRequires:  junit 
BuildRequires:  log4j
BuildRequires:  servlet6
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif

%description
The commons-logging package provides a simple, component oriented
interface (org.apache.commons.logging.Log) together with wrappers for
logging systems. The user can choose at runtime which system they want
to use. In addition, a small number of basic implementations are
provided to allow users to use the package standalone. 
commons-logging was heavily influenced by Avalon's Logkit and Log4J. The
commons-logging abstraction is meant to minimixe the differences between
the two, and to allow a developer to not tie himself to a particular
logging implementation.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Javadoc for %{name}.

# -----------------------------------------------------------------------------

%prep
%setup -q -n %{short_name}-%{version}-src
%patch1 -p1

# -----------------------------------------------------------------------------

%build
cat > build.properties <<EOBM
junit.jar=$(build-classpath junit)
log4j.jar=$(build-classpath log4j)
log4j12.jar=$(build-classpath log4j)
%if !%{with bootstrap}
logkit.jar=$(build-classpath avalon-logkit)
avalon-framework.jar=$(build-classpath avalon-framework)
%endif
servletapi.jar=$(build-classpath tomcat6-servlet-2.5-api)
EOBM
%if !%{with bootstrap}
export OPT_JAR_LIST="ant/ant-junit"
%endif
%{ant} -Dsource.version=1.4 -Dtarget.version=1.4 clean compile
#%{ant} -Dsource.version=1.4 -Dtarget.version=1.4 compile.tests test

(cd src/java && %{javadoc} -d ../../target/docs/api `%{_bindir}/find . -type f -name '*.java'`)

# -----------------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 644 target/%{short_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -p -m 644 target/%{short_name}-adapters-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-adapters-%{version}.jar
install -p -m 644 target/%{short_name}-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-api-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a target/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# -----------------------------------------------------------------------------

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc PROPOSAL.html STATUS.html LICENSE.txt RELEASE-NOTES.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

# -----------------------------------------------------------------------------


%changelog
* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1-3.3.7mdv2011.0
+ Revision: 606058
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1-3.3.6mdv2010.1
+ Revision: 522981
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.1-3.3.5mdv2010.0
+ Revision: 425440
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.1-3.3.4mdv2009.1
+ Revision: 351288
- rebuild

* Thu Jul 31 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.1-3.3.3mdv2009.0
+ Revision: 257587
- update osgi manifest

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 0:1.1-3.3.2mdv2009.0
+ Revision: 167947
- fix no-buildroot-tag
- kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.1-3.3.2mdv2008.1
+ Revision: 120915
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.1-3.3.1mdv2008.0
+ Revision: 87413
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Wed Aug 22 2007 David Walluck <walluck@mandriva.org> 0:1.1-3.3.0mdv2008.0
+ Revision: 69293
- bump release

* Wed Aug 22 2007 David Walluck <walluck@mandriva.org> 0:1.1-3.3mdv2008.0
+ Revision: 69201
- do not run tests
- set OPT_JAR_LIST=ant/ant-junit
- add eclipse manifest patch
- build and run tests even though they fail on gcj
- manually build javadocs
- remove javadoc scriptlets


* Wed Mar 14 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.1-3.3mdv2007.1
+ Revision: 143758
- rebuild for 2007.1
- Import jakarta-commons-logging

* Fri Aug 04 2006 David Walluck <walluck@mandriva.org> 0:1.1-3.2mdv2007.0
- enable debug package

* Mon Jun 12 2006 David Walluck <walluck@mandriva.org> 0:1.1-3.1mdv2007.0
- bump release

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:1.1-2mdv2007.0
- this is not a noarch package

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:1.1-1mdv2007.0
- 1.1
- rebuild for libgcj.so.7
- aot-compile
- no api docs

* Fri May 13 2005 David Walluck <walluck@mandriva.org> 0:1.0.4-2.1mdk
- release

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:1.0.4-2jpp
- Rebuild with ant-1.6.2

* Fri Jun 25 2004 Kaj J. Niemi <kajtzu@fi.basen.net> - 0:1.0.4-1jpp
- Update to 1.0.4 (tomcat 5.0.27 wants it)
- Drop Patch #0 (jakarta-commons-logging-noclasspath.patch), unnecessary

