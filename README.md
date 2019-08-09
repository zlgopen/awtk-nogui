# AWTK-NOGUI

AWTK-NOGUI 是一个裁剪掉GUI控件和显示部分的版本，方便AWTK-MVVM在没有GUI的情况下使用。


## 一、下载

```
git clone https://github.com/zlgopen/awtk.git

git clone https://github.com/zlgopen/awtk-nogui.git

```

## 二、准备

```
cd awtk-nogui
python prepare.py
```

## 三、编译

```
scons
```

## 四、在AWTK-MVVM中使用

修改AWTK-MVVM的SConstruct文件：

```
sys.path.insert(0, '../awtk/')
```

为：
```
sys.path.insert(0, '../awtk-nogui/')
```

> 目前AWTK-MVVM的demo中，只有demo17是不需GUI的。

