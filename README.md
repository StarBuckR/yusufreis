# Projectx
<p align="center">
    <img src="https://raw.githubusercontent.com/StarBuckR/yusufreis/master/screenshots/Summary.png">    
</p>

<p align="center">
 <img alt="Build" src="https://github.com/StarBuckR/yusufreis/workflows/Yusufreis%20CI/badge.svg">
</p>

# Install Directly From Latest .deb File (eg. Pardus 19.x, Debian 10, Ubuntu 18.04 and Ubuntu 20.04)
```
curl -s https://api.github.com/repos/StarBuckR/yusufreis/releases/latest | grep "browser_download_url.*deb" | cut -d '"' -f 4 | wget -qi -
sudo apt install -y  ./`curl -s https://api.github.com/repos/StarBuckR/yusufreis/releases/latest | grep "browser_download_url.*deb" | cut -d '"' -f 4 | grep -o '[^/]*$'`
```
## Run 

Run with default language
```
yusufreis
```

Run with spesific language

```
LANGUAGE=tr yusufreis
```
# Install From Source Code(Debian)
```
git clone https://github.com/StarBuckR/yusufreis
cd yusufreis
sudo bash build_debpackage.sh
```

# Run Without Installing

## Required Dependecies
### Debian
* python3
* python3-gi 
* python3-pil
* graphicsmagick-imagemagick-compat
* gir1.2-appindicator3-0.1

### RedHat
* python3
* python3-gobject
* python3-pillow
* imagemagick
* libappindicator-gtk3

## Run

```
python3 src/tray.py
```

or with spesific language
```
LANGUAGE=tr python3 src/tray.py
```

# Sample Window
<p align="center">
    <img src="https://raw.githubusercontent.com/StarBuckR/yusufreis/master/screenshots/Controls.png">    
</p>
