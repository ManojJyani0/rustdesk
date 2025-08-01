Name:       remotedesk
Version:    1.1.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb1 xdotool libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/remotedesk/
mkdir -p %{buildroot}/usr/share/remotedesk/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/remotedesk %{buildroot}/usr/bin/remotedesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/remotedesk/libsciter-gtk.so
install $HBB/res/remotedesk.service %{buildroot}/usr/share/remotedesk/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/remotedesk.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/remotedesk.svg
install $HBB/res/remotedesk.desktop %{buildroot}/usr/share/remotedesk/files/
install $HBB/res/remotedesk-link.desktop %{buildroot}/usr/share/remotedesk/files/

%files
/usr/bin/remotedesk
/usr/share/remotedesk/libsciter-gtk.so
/usr/share/remotedesk/files/remotedesk.service
/usr/share/icons/hicolor/256x256/apps/remotedesk.png
/usr/share/icons/hicolor/scalable/apps/remotedesk.svg
/usr/share/remotedesk/files/remotedesk.desktop
/usr/share/remotedesk/files/remotedesk-link.desktop

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop remotedesk || true
  ;;
esac

%post
cp /usr/share/remotedesk/files/remotedesk.service /etc/systemd/system/remotedesk.service
cp /usr/share/remotedesk/files/remotedesk.desktop /usr/share/applications/
cp /usr/share/remotedesk/files/remotedesk-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable remotedesk
systemctl start remotedesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop remotedesk || true
    systemctl disable remotedesk || true
    rm /etc/systemd/system/remotedesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/remotedesk.desktop || true
    rm /usr/share/applications/remotedesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
