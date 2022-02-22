#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (running fails?)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Flexible test runner with layer support
Summary(pl.UTF-8):	Elastyczne uruchamianie testów z obsługą warstw
Name:		python-zope.testrunner
Version:	5.4.0
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/zope.testrunner/
Source0:	https://files.pythonhosted.org/packages/source/z/zope.testrunner/zope.testrunner-%{version}.tar.gz
# Source0-md5:	ae1320203ab70780632e030da50d82b0
URL:		https://www.zope.org/
%if %{with python2}
BuildRequires:	python >= 1:2.7
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-six
BuildRequires:	python-zope.exceptions
BuildRequires:	python-zope.interface
BuildRequires:	python-zope.testing
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.5
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-six
BuildRequires:	python3-zope.exceptions
BuildRequires:	python3-zope.interface
BuildRequires:	python3-zope.testing
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinxcontrib-programoutput
BuildRequires:	python3-zope.exceptions
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
Requires:	python-zope-base
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides a flexible test runner with layer support.

%description -l pl.UTF-8
Ten pakiet zapewnia elastyczne uruchamianie testów z obsługą warstw.

%package -n python3-zope.testrunner
Summary:	Flexible test runner with layer support
Summary(pl.UTF-8):	Elastyczne uruchamianie testów z obsługą warstw
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5
Requires:	python3-zope-base

%description -n python3-zope.testrunner
This package provides a flexible test runner with layer support.

%description -n python3-zope.testrunner -l pl.UTF-8
Ten pakiet zapewnia elastyczne uruchamianie testów z obsługą warstw.

%package -n python3-zope.testrunner-examples
Summary:	Example tests for zope.testrunner
Summary(pl.UTF-8):	Przykładowe testy dla szkieletu zope.testrunner
Group:		Development/Tools
Requires:	python3-zope.testrunner = %{version}-%{release}

%description -n python3-zope.testrunner-examples
Example tests for zope.testrunner.

%description -n python3-zope.testrunner-examples -l pl.UTF-8
Przykładowe testy dla szkieletu zope.testrunner.

%package apidocs
Summary:	API documentation for Python zope.testrunner module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona zope.testrunner
Group:		Documentation

%description apidocs
API documentation for Python zope.testrunner module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona zope.testrunner.

%prep
%setup -q -n zope.testrunner-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install \
	--install-purelib=%{py_sitescriptdir}

%py_postclean
# python2 test examples are useless because of postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/zope/testrunner/tests

%{__mv} $RPM_BUILD_ROOT%{_bindir}/zope-testrunner{,-2}
%endif

%if %{with python3}
%py3_install \
	--install-purelib=%{py3_sitescriptdir}

%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/testrunner/tests/*.{py,rst}
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/testrunner/tests/__pycache__
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/testrunner/tests/testrunner-ex*/__pycache__
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/testrunner/tests/testrunner-ex*/*/__pycache__
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/testrunner/tests/testrunner-ex*/*/*/__pycache__

%{__mv} $RPM_BUILD_ROOT%{_bindir}/zope-testrunner{,-3}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.rst LICENSE.md README.rst
%attr(755,root,root) %{_bindir}/zope-testrunner-2
%{py_sitescriptdir}/zope/testrunner
%{py_sitescriptdir}/zope.testrunner-%{version}-py*.egg-info
%{py_sitescriptdir}/zope.testrunner-%{version}-py*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-zope.testrunner
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.rst LICENSE.md README.rst
%attr(755,root,root) %{_bindir}/zope-testrunner-3
%dir %{py3_sitescriptdir}/zope/testrunner
%{py3_sitescriptdir}/zope/testrunner/*.py
%{py3_sitescriptdir}/zope/testrunner/__pycache__
%{py3_sitescriptdir}/zope.testrunner-%{version}-py*.egg-info
%{py3_sitescriptdir}/zope.testrunner-%{version}-py*-nspkg.pth

%files -n python3-zope.testrunner-examples
%defattr(644,root,root,755)
%dir %{py3_sitescriptdir}/zope/testrunner/tests
%{py3_sitescriptdir}/zope/testrunner/tests/testrunner-ex*
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
