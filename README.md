# Simple Ubuntu Container

This is a simple Ubuntu container written in python following [Liz Rice's talk](https://www.youtube.com/watch?v=8fi7uSYlOdc). To run the container you'll first need to download the file system

```bash
wget https://cdimage.ubuntu.com/ubuntu-base/releases/24.04.5/release/ubuntu-base-24.04.3-base-amd64.tar.gz
mkdir fs && tar -xzf ubuntu-base-24.04.3-base-amd64.tar.gz -C fs
```
