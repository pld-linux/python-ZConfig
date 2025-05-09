#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-ZConfig.spec)

%define		module		ZConfig
Summary:	Structured Configuration Library
Summary(pl.UTF-8):	Biblioteka ustrukturyzowanych plików konfiguracyjnych
Name:		python-%{module}
# keep 3.x here for python2 support
Version:	3.6.1
Release:	4
License:	ZPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/Z/ZConfig/%{module}-%{version}.tar.gz
# Source0-md5:	ec207a5078c0b0d1e81d6d9b8c2208af
URL:		https://github.com/zopefoundation/ZConfig/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-docutils
BuildRequires:	python-manuel
BuildRequires:	python-zope.exceptions
BuildRequires:	python-zope.testrunner
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-docutils
BuildRequires:	python3-manuel
BuildRequires:	python3-zope.exceptions
BuildRequires:	python3-zope.testrunner
%endif
%endif
%if %{with doc}
BuildRequires:	python-sphinxcontrib-programoutput
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ZConfig is a configuration library intended for general use. It
supports a hierarchical schema-driven configuration model that allows
a schema to specify data conversion routines written in Python.
ZConfig's model is very different from the model supported by the
ConfigParser module found in Python's standard library, and is more
suitable to configuration-intensive applications.

%description -l pl.UTF-8
ZConfig to biblioteka konfiguracji, przeznaczona do ogólnego użytku.
Obsługuje hierarchiczny, oparty na schematach model konfiguracji,
pozwalający na określanie w schematach napisanych w Pythonie procedur
konwersji danych. Model ZConfig różni się znacząco od modelu
obsługiwanego przez moduł ConfigParser z biblioteki standardowej
Pythona i bardziej odpowiada aplikacjon korzystającym intensywnie z
konfiguracji.

%package -n python3-%{module}
Summary:	Structured Configuration Library
Summary(pl.UTF-8):	Biblioteka ustrukturyzowanych plików konfiguracyjnych
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
ZConfig is a configuration library intended for general use. It
supports a hierarchical schema-driven configuration model that allows
a schema to specify data conversion routines written in Python.
ZConfig's model is very different from the model supported by the
ConfigParser module found in Python's standard library, and is more
suitable to configuration-intensive applications.

%description -n python3-%{module} -l pl.UTF-8
ZConfig to biblioteka konfiguracji, przeznaczona do ogólnego użytku.
Obsługuje hierarchiczny, oparty na schematach model konfiguracji,
pozwalający na określanie w schematach napisanych w Pythonie procedur
konwersji danych. Model ZConfig różni się znacząco od modelu
obsługiwanego przez moduł ConfigParser z biblioteki standardowej
Pythona i bardziej odpowiada aplikacjon korzystającym intensywnie z
konfiguracji.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Pythona %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

mkdir -p stubs
cat >stubs/zconfig <<EOF
#!/bin/sh
%{__python} $(pwd)/src/ZConfig/validator.py "\$@"
EOF
cat >stubs/zconfig_schema2html <<EOF
#!/bin/sh
%{__python} $(pwd)/src/ZConfig/schema2html.py "\$@" 
EOF
chmod 755 stubs/zconfig*

%build
%if %{with python2}
%py_build

%if %{with tests}
LC_ALL=C.UTF-8 \
PYTHONPATH=$(pwd)/src \
zope-testrunner-2 --test-path=src -v
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
zope-testrunner-3 --test-path=src -v
%endif
%endif

%if %{with doc}
PATH=$(pwd)/stubs:$PATH \
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/ZConfig/tests
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/ZConfig/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{py_sitescriptdir}/ZConfig
%{py_sitescriptdir}/ZConfig-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/zconfig
%attr(755,root,root) %{_bindir}/zconfig_schema2html
%{py3_sitescriptdir}/ZConfig
%{py3_sitescriptdir}/ZConfig-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
