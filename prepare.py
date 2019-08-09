import os
import os
import sys
import glob
import shutil

def join_path(root, subdir):
    return os.path.abspath(os.path.normpath(os.path.join(root, subdir)))

def mkdir_if_not_exist(fullpath):
    if os.path.exists(fullpath):
        print(fullpath+' exist.')
    else:
        os.makedirs(fullpath)

def copy_folder(src, dst):
    print(src + '=>' + dst)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

def copy_file(src, dst):
    print(src + '=>' + dst)
    with open(dst, 'w') as outfile:
        with open(src) as infile:
            outfile.write(infile.read())
            outfile.write('\n')

def file_write(name, content):
  with open(name, 'w') as outfile:
    outfile.write(content)


AWTK_ROOT=join_path('.', '../awtk/')
AWTK_SRC=join_path(AWTK_ROOT, 'src')

def prepare_dirs():
    mkdir_if_not_exist('src');
    mkdir_if_not_exist('3rd/gtest');
    mkdir_if_not_exist('src/base');
    mkdir_if_not_exist('src/tkc');
    mkdir_if_not_exist('src/ui_loader');
    mkdir_if_not_exist('src/main_loop');
    mkdir_if_not_exist('src/native_window');
    mkdir_if_not_exist('src/widgets');
    mkdir_if_not_exist('src/platforms/pc');
    mkdir_if_not_exist('src/platforms/raw');

def copy_sources():
    copy_folder(join_path(AWTK_ROOT, "3rd/gtest"), "3rd/gtest")
    all_sources=glob.glob(join_path(AWTK_SRC, 'tkc/*.c')) + \
      glob.glob(join_path(AWTK_SRC, 'base/*.c')) + \
      glob.glob(join_path(AWTK_SRC, 'platforms/*/*.c')) + \
      glob.glob(join_path(AWTK_SRC, 'ui_loader/*.c'))
    
    all_sources +=glob.glob(join_path(AWTK_SRC, 'tkc/*.h')) + \
      glob.glob(join_path(AWTK_SRC, 'base/*.h')) + \
      glob.glob(join_path(AWTK_SRC, 'platforms/*/*.h')) + \
      glob.glob(join_path(AWTK_SRC, 'ui_loader/*.h'))

    all_sources += glob.glob(join_path(AWTK_SRC, 'native_window/native_window_raw.h'));
    all_sources += glob.glob(join_path(AWTK_SRC, 'main_loop/main_loop_simple.h'));
    all_sources += glob.glob(join_path(AWTK_SRC, 'widgets/dialog.h'));
    all_sources += glob.glob(join_path(AWTK_SRC, 'widgets/window.h'));
    
    all_sources += glob.glob(join_path(AWTK_SRC, 'native_window/native_window_raw.c'));
    all_sources += glob.glob(join_path(AWTK_SRC, 'main_loop/main_loop_simple.c'));
    all_sources += glob.glob(join_path(AWTK_SRC, 'widgets/dialog.c'));
    all_sources += glob.glob(join_path(AWTK_SRC, 'widgets/window.c'));

    excluded_files = ['text_edit', 'hscrollable', 'ui_loader_xml']

    for f in all_sources:
        basename, ext = os.path.splitext(os.path.basename(f))
        dst=f.replace(AWTK_SRC, 'src');
        if basename in excluded_files:
            print('skip ' + f)
        else:
            copy_file(f, dst)

prepare_dirs();
copy_sources();

