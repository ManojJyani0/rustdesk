Name:       remotedesk
Version:    1.4.1
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://remotedesk.com
Vendor:     remotedesk <info@remotedesk.com>
Requires:   gtk3 libxcb1 xdotool libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/remotedesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/remotedesk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/remotedesk.service -t "%{buildroot}/usr/share/remotedesk/files"
install -Dm 644 $HBB/res/remotedesk.desktop -t "%{buildroot}/usr/share/remotedesk/files"
install -Dm 644 $HBB/res/remotedesk-link.desktop -t "%{buildroot}/usr/share/remotedesk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/remotedesk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/remotedesk.svg"

%files
/usr/share/remotedesk/*
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
ln -sf /usr/share/remotedesk/remotedesk /usr/bin/remotedesk
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
    rm /usr/bin/remotedesk || true
    rmdir /usr/lib/remotedesk || true
    rmdir /usr/local/remotedesk || true
    rmdir /usr/share/remotedesk || true
    rm /usr/share/applications/remotedesk.desktop || true
    rm /usr/share/applications/remotedesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/remotedesk || true
    rmdir /usr/local/remotedesk || true
  ;;
esac
