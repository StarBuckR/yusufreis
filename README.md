# yusufreis

## Dependencies

* Python3
* GTK3
* [gi(PyGObject)](https://pypi.org/project/PyGObject/)
* [Pillow](https://pypi.org/project/Pillow/)

## Install

### Pardus 19.x, Debian 10, Ubuntu 18.04 and Ubuntu 20.04

```
curl -s https://api.github.com/repos/StarBuckR/yusufreis/releases/latest | grep "browser_download_url.*deb" | cut -d '"' -f 4 | wget -qi -
sudo apt install -y  ./`curl -s https://api.github.com/repos/StarBuckR/yusufreis/releases/latest | grep "browser_download_url.*deb" | cut -d '"' -f 4 | grep -o '[^/]*$'`
```

## Run 

Run with default language
```
yusufreis
```

Run with spesific Language

```
LANGUAGE=tr yusufreis
```
 
 
