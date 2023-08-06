# qqwry-linux-python3

Linux下自动更新qqwry的工具

## 安装

```bash
pip3  install qqwry-linux-python3
```

## 更新 qqwry.dat

### 原理

1. 从微信公众号文章中取出最新zip包地址并下载

   > https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3Mzc0NTA3NA==&action=getalbum&album_id=2329805780276838401
   >
   > zip地址如：https://www.cz88.net/soft/H50VASDc3-2023-06-21.zip

2. 解压zip得到setup.exe

3. 解压setup.exe得到qqwry.dat

### 代码

```python
>>> from qqwry.src import UpdateQQwry
>>> uq = UpdateQQwry('./qqwry.dat')
>>> uq.update()
/usr/local/bin/innoextract is valid
https://www.cz88.net/soft/H50VASDc3-2023-06-21.zip Downloading...
https://www.cz88.net/soft/H50VASDc3-2023-06-21.zip Download completed
copy /tmp/app/qqwry.dat to /root/.nali/qqwry.dat completed
True
```

## 使用 qqwry.dat

```python
>>> from qqwry.src import QQwry
>>> qw = QQwry()
>>> qw.load_file('./qqwry.dat')
True
>>> print(qw.lookup('8.8.8.8'))
('美国加利福尼亚州圣克拉拉县山景市', '谷歌公司DNS服务器')
```

