%define		_rc	rc4
%define		_rel	2.1
%include	/usr/lib/rpm/macros.java
Summary:	Jakarta Commons HTTPClient Package
Summary(pl.UTF-8):	Pakiet Jakarta Commons HTTPClient
Name:		jakarta-commons-httpclient3
Version:	3.0
Release:	0.%{_rc}.%{_rel}
License:	Apache Software License
Source0:	http://archive.apache.org/dist/jakarta/commons/httpclient/source/commons-httpclient-%{version}-%{_rc}-src.tar.gz
# Source0-md5:	961edab7cdf9950f2a6d2243301407e3
Group:		Development/Languages/Java
URL:		http://jakarta.apache.org/commons/httpclient/
BuildRequires:	ant
BuildRequires:	jakarta-commons-codec
BuildRequires:	jakarta-commons-logging >= 1.0.3
BuildRequires:	jce >= 1.2.2
BuildRequires:	jpackage-utils
BuildRequires:	jsse >= 1.0.3.01
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jakarta-commons-logging >= 1.0.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Hyper-Text Transfer Protocol (HTTP) is perhaps the most
significant protocol used on the Internet today. Web services,
network-enabled appliances and the growth of network computing
continue to expand the role of the HTTP protocol beyond user-driven
web browsers, and increase the number of applications that may require
HTTP support. Although the java.net package provides basic support for
accessing resources via HTTP, it doesn't provide the full flexibility
or functionality needed by many applications. The Jakarta Commons HTTP
Client component seeks to fill this void by providing an efficient,
up-to-date, and feature-rich package implementing the client side of
the most recent HTTP standards and recommendations. Designed for
extension while providing robust support for the base HTTP protocol,
the HTTP Client component may be of interest to anyone building
HTTP-aware client applications such as web browsers, web service
clients, or systems that leverage or extend the HTTP protocol for
distributed communication.

%description -l pl.UTF-8
Protokół przesyłania hypertekstu (HTTP - Hyper-Text Transfer Protocol)
jest prawdopodobnie najbardziej znaczącym z używanych obecnie
protokołów w Internecie. Usługi WWW, zastosowania sieciowe i rozwój
usług sieciowych nadal rozszerza rolę protokołu HTTP poza przeglądarki
obsługiwane przez użytkownika i zwiększa liczbę aplikacji mogących
potrzebować obsługi HTTP. Mimo że pakiet java.net udostępnia
podstawową obsługę dostępu do zasobów poprzez HTTP, nie dostarcza
pełnej elastyczności czy funkcjonalności potrzebnej wielu aplikacjom.
Komponent Jakarta Commons HTTP Client stara się wypełnić tę lukę
dostarczając wydajny, aktualny i bogaty w możliwości pakiet
implementujący kliencką stronę najnowszych standardów i rekomendacji
HTTP. Zaprojektowany do rozszerzania, a jednocześnie dostarczający
bogatą obsługę podstawowego protokołu HTTP, komponent HTTP Client może
być interesujący dla każdego tworzącego aplikacje klienckie
obsługujące HTTP, takie jak przeglądarki WWW, klientów usług WWW czy
systemy wykorzystujące lub rozszerzające protokół HTTP do komunikacji
rozproszonej.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%package demo
Summary:	Demos for %{name}
Summary(pl.UTF-8):	Programy demonstracyjne dla pakietu %{name}
Group:		Development
Requires:	%{name} = %{version}-%{release}

%description demo
Demos for %{name}.

%description demo -l pl.UTF-8
Programy demonstracyjne dla pakietu %{name}.

%package manual
Summary:	Manual for %{name}
Summary(pl.UTF-8):	Podręcznik dla pakietu %{name}
Group:		Documentation

%description manual
Manual for %{name}.

%description manual -l pl.UTF-8
Podręcznik dla pakietu %{name}.

%prep
%setup -q -n commons-httpclient-%{version}-%{_rc}
mkdir lib # duh
rm -rf docs/apidocs docs/*.patch docs/*.orig docs/*.rej

%build
export LC_ALL=en_US # source not in ASCII
export CLASSPATH=$(build-classpath jsse jce junit commons-codec commons-logging)
%ant \
	-Dbuild.sysclasspath=first \
	-Djavadoc.j2sdk.link=%{_javadocdir}/java \
	-Djavadoc.logging.link=%{_javadocdir}/jakarta-commons-logging \
	dist test

rm -rf apidoc
rm -f dist/docs/{BUILDING,TESTING}.txt
mv dist/docs/api apidoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a dist/commons-httpclient.jar $RPM_BUILD_ROOT%{_javadir}/commons-httpclient-%{version}.jar
ln -s commons-httpclient-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/commons-httpclient.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a apidoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# demo
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr src/examples/* src/contrib $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.txt RELEASE_NOTES.txt
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files manual
%defattr(644,root,root,755)
%doc dist/docs/*
