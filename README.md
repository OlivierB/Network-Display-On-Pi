Network-Display-On-Pi
=====================

(NDOP)

# Install
 - pypcap : http://sourceforge.net/projects/pylibpcap/
 - psutil : https://code.google.com/p/psutil/
 - python-tornado

## Web
### Install :
- openbox
- unclutter (optional mouse hider)
- sakura (optional good terminal)

### openbox configuration :
create file ~/.config/openbox/autostart
Insert commands lines :
	sakura &
	google-chrome --kiosk --incognito --no-context-menu http://address &
