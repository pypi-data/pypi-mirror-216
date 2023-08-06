# ===============================================================================
# Copyright 2021 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

EDM_REQUIREMENTS = [
    "chaco>=5.0.0,<5.1.0",
    "certifi",
    "cython",
    "envisage",
    "future",
    "gitpython",
    "keyring",
    "jinja2",
    "lxml",
    "numpy",
    "pandas",
    "patsy",
    "pillow",
    "pip",
    "pyface",
    "pyparsing",
    "pyproj",
    # "pymysql", #edm install 0.7.9 version 1.0.2 or greater required. used pip
    "pyqt5",
    "pytables",
    "pyyaml",
    "pygments",
    "qt",
    "Reportlab",
    "requests",
    "scipy",
    "sqlalchemy>=1.3.0,<1.4.0",
    "traits>=6.3.0,<6.7.0",
    "traitsui>=7.4.0,<7.5.0" "xlrd",
    "xlsxwriter",
    "xlwt",
    "statsmodels",
    "cryptography",
]

CONDA_REQUIREMENTS = [
    # "chaco",
    "cython",
    "gitpython",
    "jinja2",
    "lxml",
    "numpy",
    "pillow",
    "pip",
    "pyparsing",
    "pyproj",
    "pyqt5",
    "pytables",
    "pyyaml",
    "pygments",
    "Reportlab",
    "requests",
    "scipy",
    "sqlalchemy",
    "xlrd",
    "xlsxwriter",
    "xlwt",
    "statsmodels",
    "google_auth_oauthlib",
]

PIP_REQUIREMENTS = [
    "uncertainties",
    "qimage2ndarray",
    "pymysql==0.7.9",
    "envisage",
    "chaco",
    "traitsui",
    "traits",
]

VALVE_REQUIREMENTS = ["pyserial", "twisted"]
PIP_EXTRAS = ["peakutils", "utm"]

# ============= EOF =============================================
