#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (running fails?)

Summary:	Flexible test runner with layer support
Summary(pl.UTF-8):	Elastyczne uruchamianie testów z obsługą warstw
Name:		python3-zope.testrunner
Version:	7.2
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/zope.testrunner/
Source0:	https://files.pythonhosted.org/packages/source/z/zope.testrunner/zope_testrunner-%{version}.tar.gz
# Source0-md5:	9e41c200a79a18e33a631a2b5cf7c678
URL:		https://www.zope.org/
BuildRequires:	python3 >= 1:3.9
BuildRequires:	python3-devel >= 1:3.9
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-zope.exceptions
BuildRequires:	python3-zope.interface
BuildRequires:	python3-zope.testing
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinxcontrib-programoutput
BuildRequires:	python3-zope.exceptions
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.9
Requires:	python3-zope-base
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides a flexible test runner with layer support.

%description -l pl.UTF-8
Ten pakiet zapewnia elastyczne uruchamianie testów z obsługą warstw.

%package examples
Summary:	Example tests for zope.testrunner
Summary(pl.UTF-8):	Przykładowe testy dla szkieletu zope.testrunner
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description examples
Example tests for zope.testrunner.

%description examples -l pl.UTF-8
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
%setup -q -n zope_testrunner-%{version}

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
%{__python3} -m zope.testrunner --test-path=src
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/testrunner/tests/*.{py,rst}
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/testrunner/tests/__pycache__
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/testrunner/tests/logsupport
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/testrunner/tests/testrunner-ex*/__pycache__
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/testrunner/tests/testrunner-ex*/*/__pycache__
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/zope/testrunner/tests/testrunner-ex*/*/*/__pycache__

%{__mv} $RPM_BUILD_ROOT%{_bindir}/zope-testrunner{,-3}
ln -sf zope-testrunner-3 $RPM_BUILD_ROOT%{_bindir}/zope-testrunner

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.rst LICENSE.md README.rst
%attr(755,root,root) %{_bindir}/zope-testrunner
%attr(755,root,root) %{_bindir}/zope-testrunner-3
%dir %{py3_sitescriptdir}/zope/testrunner
%{py3_sitescriptdir}/zope/testrunner/*.py
%{py3_sitescriptdir}/zope/testrunner/__pycache__
%{py3_sitescriptdir}/zope.testrunner-%{version}-py*.egg-info
%{py3_sitescriptdir}/zope.testrunner-%{version}-py*-nspkg.pth

%files examples
%defattr(644,root,root,755)
%dir %{py3_sitescriptdir}/zope/testrunner/tests
%{py3_sitescriptdir}/zope/testrunner/tests/testrunner-ex*

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
