#!/usr/bin/env bash

SETUP_NAME="Dependencies setup script"
SETUP_TITLE="# Setup"
SHELL_RCFILE=".dr_$(basename "$SHELL")rc"
SHELL_PROFILE=".$(basename "$SHELL")_profile"
PY3_REQ_VER=$(cat "$SCRIPT_DIR"/.python-version)

DEPENDENCIES_LIST=("pyenv" "python" "poetry")
DEB_PACKAGES=(
  build-essential curl make libbz2-dev libffi-dev libgdbm-dev
  liblzma-dev libncurses5-dev libncursesw5-dev libreadline-dev
  libsqlite3-dev libssl-dev libxml2-dev libxmlsec1-dev llvm lzma lzma-dev
  make python3-openssl tcl-dev tk-dev xz-utils wget zlib1g-dev
)
RPM_PACKAGES=(
  bzip2-devel curl gcc-c++ libffi-devel make ncurses-devel
  openssl-devel python3-tkinter readline-devel sqlite-devel tar tk-devel
  wget xz-devel
)
COLUMNS_LIMIT="100"
BOLD=$(tput bold)
NORM=$(tput sgr0)
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
BLUE=$(tput setaf 4)
CYAN=$(tput setaf 6)
SCRIPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}")" &>/dev/null && pwd )

HEADER1() { echo -e "\n   ${BOLD}${YELLOW}$1${NORM}"; }
HEADER2() { echo -e "\n   ${BOLD}${BLUE}$1${NORM}"; }
HEADER3() { echo -e "\t${BOLD}${CYAN}$1${NORM}"; }
VERSION() { echo "$@" | awk -F. '{ printf("%d%03d%03d%03d\n", $1,$2,$3,$4); }'; }
TITLE() { 
  printf -- '=%.0s' $(seq 1 ${COLUMNS_LIMIT}); printf '\n'
  printf "%s%$(( (${#1} + COLUMNS_LIMIT) / 2))s%s\n" "${BLUE}${BOLD}" "$1" "${NORM}"
  printf -- '=%.0s' $(seq 1 ${COLUMNS_LIMIT}); printf '\n'
}

DETECT_OS(){
  uname_out=$(uname -a)
  case "${uname_out}" in
    *microsoft*)  OS="WSL2";;
    Linux*)       OS="Linux";;
    Darwin*)      OS="Mac";;
    *)            OS="UNKNOWN:${uname_out}"
  esac
  if [ -f /etc/os-release ]; then
    # shellcheck source=/dev/null
    . /etc/os-release
    OSID=$ID
    OSN=$NAME
    VER=$VERSION_ID
  elif type lsb_release >/dev/null 2>&1; then
    OSID=$(lsb_release -sc)
    OSN=$(lsb_release -si)
    VER=$(lsb_release -sr)
  elif [ -f /etc/lsb-release ]; then
    # shellcheck source=/dev/null
    . /etc/lsb-release
    OSID=$ID
    OSN=$DISTRIB_ID
    VER=$DISTRIB_RELEASE
  elif [ -f /etc/arch-release ]; then
    OSID=$ID
    OSN="Arch family"
    VER=$(cat /etc/*version)
  elif [ -f /etc/debian_version ]; then
    OSID=$ID
    OSN="Debian family"
    VER=$(cat /etc/debian_version)
  elif [ -f /etc/redhat-release ]; then
    OSID=$ID
    OSN="RedHat family"
    VER=$(cat /etc/redhat_version)
  else
    OSID=$ID
    OSN=$(uname -s)
    VER=$(uname -r)
  fi
  HEADER1 "Running on: ${OSID} - ${OS} / ${OSN} - ${VER} - ${OSTYPE}";
  if [[ "${OS}" =~ ^(Linux|Mac|WSL2)$ ]];
    then HEADER2 "Operating System - supported";
      if [[ "${OSID}" =~ ^(ubuntu|debian|linuxmint)$ ]]; then declare -a DEB_PACKAGE_INSTALL
        for DEB_PACKAGE in "${DEB_PACKAGES[@]}"; do if ! dpkg -l | grep -qw "$DEB_PACKAGE";
          then DEB_PACKAGE_INSTALL+=("$DEB_PACKAGE"); fi; done
        if [[ ${#DEB_PACKAGE_INSTALL[@]} -gt 0 ]]; then sudo apt update;
          sudo apt install "${DEB_PACKAGE_INSTALL[@]}";fi
      fi
      if [[ "${OSID}" =~ ^(fedora|centos|redhat)$ ]]; then declare -a RPM_PACKAGE_INSTALL;
        for RPM_PACKAGE in "${RPM_PACKAGES[@]}"; do if ! rpm -qa | grep -qw "$RPM_PACKAGE";
          then RPM_PACKAGE_INSTALL+=("$RPM_PACKAGE"); fi; done
        if [[ "${#RPM_PACKAGE_INSTALL[@]}" -gt 0 ]]; then sudo dnf install -y "${RPM_PACKAGE_INSTALL[@]}"; fi
        dnf grouplist --installed | grep -wq "Development Tools";
        if [ "${PIPESTATUS[1]}" != "0" ]; then sudo yum -y group install "Development Tools";fi
      fi
    else HEADER2 "Operating System - NOT supported"; exit 1;
  fi
}

LOAD_CONFIG(){
  [ ! -f ~/"$SHELL_RCFILE" ] && (umask 022; touch "$HOME/$SHELL_RCFILE");
  echo "$SETUP_TITLE" >"$HOME/$SHELL_RCFILE"
  ! grep -q "$SHELL_RCFILE" "$HOME/.$(basename "$SHELL")rc" && \
  echo -e "source \$HOME/$SHELL_RCFILE\n" >>"$HOME/.$(basename "$SHELL")rc"
  # shellcheck source=/dev/null
  [ -f "$HOME/$SHELL_RCFILE" ] && source "$HOME/$SHELL_RCFILE"
}

INSTALL_DEPENDENCIES(){
  HEADER1 "Installing dependencies"
  for ITEM in "${DEPENDENCIES_LIST[@]}"; do
    HEADER2 "Checking ${ITEM^^} ..."
    if command -v "$ITEM" >/dev/null;
      then declare "INSTALLED_${ITEM^^}=true";
      else declare "INSTALLED_${ITEM^^}=false";
    fi
    "install_${ITEM}"
  done
}

VERSION_COMPARE() {
  if [[ $(VERSION "$1") == $(VERSION "$2") ]]; then return 0; fi
  if [[ $(VERSION "$1") > $(VERSION "$2") ]]; then return 1; fi
  if [[ $(VERSION "$1") < $(VERSION "$2") ]]; then return 2; fi
}

DISPLAY_INFO(){
  HEADER1 "Installed Dependencies"
  printf -- '=%.0s' $(seq 1 ${COLUMNS_LIMIT}); printf '\n'
  for ITEM in "${DEPENDENCIES_LIST[@]}"; do
    printf " %-55s %s\n" "${BOLD}${GREEN}$($ITEM --version)${NORM}" "$(which "$ITEM")"
	done
  printf -- '=%.0s' $(seq 1 ${COLUMNS_LIMIT}); printf '\n'
  echo -e "\n  Execute below shown command to load configuration settings in \
  the current shell window\n\n    $ ${BOLD}${RED}source ~/$SHELL_RCFILE${NORM}\n"
}

install_pyenv(){
  HEADER3 "Is PYENV installed: $INSTALLED_PYENV"
  if [[ ! "$INSTALLED_PYENV" == true ]]; then curl -sSL https://pyenv.run | bash || exit 1; fi
  for CONFIG in "$HOME/$SHELL_RCFILE" "$HOME/$SHELL_PROFILE"; do
    if ! grep -q "### PYENV CONFIG" "$CONFIG"; then 
      echo -e "### PYENV CONFIG\nexport PYENV_ROOT=\"\$HOME/.pyenv\"\n \
      command -v pyenv >/dev/null || export PATH=\"\$PYENV_ROOT/bin:\$HOME/.local/bin:\$PATH\"\n \
      eval \"\$(pyenv init -)\"\n" | awk '{$1=$1};1' >> "$CONFIG"
    fi
  done
  # shellcheck source=/dev/null
  source "$HOME/$SHELL_RCFILE"
}

install_python(){
  HEADER3 "Is PYTHON installed: $INSTALLED_PYTHON"
  pyenv versions
  PY3_CUR_VER=$(python3 --version 2>/dev/null | cut -d ' ' -f 2; if [ "${PIPESTATUS[0]}" != 0 ]; then echo "0.0.0"; fi)
  if VERSION_COMPARE "${PY3_CUR_VER}" "${PY3_REQ_VER}";
    then echo "Python versions match: ${PY3_CUR_VER} = ${PY3_REQ_VER}";
    else echo "Python versions mis-match: ${PY3_CUR_VER} <> ${PY3_REQ_VER}"; pyenv install "${PY3_REQ_VER}";
  fi
}

install_poetry(){
  HEADER3 "Is POETRY installed: $INSTALLED_POETRY"
  for CONFIG in "$HOME/$SHELL_RCFILE" "$HOME/$SHELL_PROFILE"; do
    if ! grep -q "### POETRY CONFIG" "$CONFIG"; then 
      echo -e "### POETRY CONFIG\n \
      command -v poetry >/dev/null || export PATH=\"\$HOME/.local/bin:\$PATH\"\n" | awk '{$1=$1};1' >>"$CONFIG"
    fi
  done
  # shellcheck source=/dev/null
  source "$HOME/$SHELL_RCFILE"
  HEADER2 "Installing Poetry"
  curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.5.1 python3 -
  HEADER2 "Installing Poetry plugins"
  poetry self add poetry-plugin-pyenv@latest poetry-dotenv-plugin@latest poethepoet[poetry_plugin]@latest

  HEADER2 "Running Poetry installation"
  poetry install
}

TITLE "${SETUP_NAME^^}"
cd "$SCRIPT_DIR" || echo "Cannot change directory to: $SCRIPT_DIR"
DETECT_OS
LOAD_CONFIG
INSTALL_DEPENDENCIES
DISPLAY_INFO
