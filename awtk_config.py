import os
import os.path
import platform

OS_NAME = platform.system()
ARCH = platform.architecture();
is32bit = (ARCH[0] == '32bit');

if is32bit:
  TARGET_ARCH='x86'
else:
  TARGET_ARCH=''

print('ARCH=' + str(ARCH) + ' TARGET_ARCH=' + TARGET_ARCH)

def joinPath(root, subdir):
  return os.path.normpath(os.path.join(root, subdir))

TK_ROOT=os.path.dirname(os.path.normpath(os.path.abspath(__file__)))

print('TK_ROOT: ' + TK_ROOT);

TK_SRC        = joinPath(TK_ROOT, 'src')
TK_BIN_DIR    = joinPath(TK_ROOT, 'bin')
TK_LIB_DIR    = joinPath(TK_ROOT, 'lib')
TK_3RD_ROOT   = joinPath(TK_ROOT, '3rd')
TK_TOOLS_ROOT = joinPath(TK_ROOT, 'tools')
TK_DEMO_ROOT  = joinPath(TK_ROOT, 'demos')
GTEST_ROOT    = joinPath(TK_ROOT, '3rd/gtest/googletest')

COMMON_CFLAGS=''
COMMON_CCFLAGS=' -DTK_ROOT=\\\"'+TK_ROOT+'\\\" ' 
COMMON_CCFLAGS=COMMON_CCFLAGS+' -DHAS_STD_MALLOC -DHAS_STDIO -DWITHOUT_EXT_WIDGETS -DAWTK_NOGUI '
COMMON_CCFLAGS=COMMON_CCFLAGS+' -DWITHOUT_WIDGET_ANIMATOR -DWITHOUT_LAYOUTER -DWITH_WIDGET_TYPE_CHECK '

OS_FLAGS=''
OS_LIBS=[]
OS_LIBPATH=[]
OS_CPPPATH=[]
OS_LINKFLAGS=''
OS_SUBSYSTEM_CONSOLE=''
OS_SUBSYSTEM_WINDOWS=''
OS_PROJECTS=[]

if OS_NAME == 'Darwin':
  OS_FLAGS='-g -Wall'
  OS_LIBS = ['stdc++', 'pthread', 'm', 'dl']
  OS_LINKFLAGS='-framework Cocoa -framework QuartzCore -framework OpenGL -weak_framework Metal -weak_framework MetalKit'
  COMMON_CCFLAGS = COMMON_CCFLAGS + ' -DWITH_WIDGET_POOL=1000 '
  COMMON_CCFLAGS = COMMON_CCFLAGS + ' -D__APPLE__ -DHAS_PTHREAD -DMACOS -DENABLE_MEM_LEAK_CHECK1 '
  COMMON_CCFLAGS = COMMON_CCFLAGS + ' -D__STDC_LIMIT_MACROS -D__STDC_FORMAT_MACROS -D__STDC_CONSTANT_MACROS  -DBGFX_CONFIG_RENDERER_METAL=1 '

elif OS_NAME == 'Linux':
  OS_FLAGS='-g -Wall'
  OS_LIBS = ['GL', 'gtk-3','gdk-3','Xext', 'X11', 'sndio','stdc++', 'pthread', 'm', 'dl']
  COMMON_CFLAGS=COMMON_CFLAGS+' -std=gnu99 '
  COMMON_CCFLAGS = COMMON_CCFLAGS + ' -DLINUX -DHAS_PTHREAD'
  COMMON_CCFLAGS = COMMON_CCFLAGS + ' -DSDL_REAL_API -DSDL_TIMER_UNIX -DSDL_VIDEO_DRIVER_X11 -DSDL_VIDEO_DRIVER_X11_SUPPORTS_GENERIC_EVENTS '
  COMMON_CCFLAGS = COMMON_CCFLAGS + ' -DSDL_AUDIO_DRIVER_SNDIO -DSDL_VIDEO_OPENGL_GLX -DSDL_VIDEO_RENDER_OGL '
  COMMON_CCFLAGS = COMMON_CCFLAGS + ' -DSDL_LOADSO_DLOPEN -DSDL_VIDEO_OPENGL_EGL -DSDL_VIDEO_OPENGL_ES2 '
  COMMON_CCFLAGS = COMMON_CCFLAGS + ' -DSDL_REAL_API -DSDL_HAPTIC_DISABLED -DSDL_SENSOR_DISABLED -DSDL_JOYSTICK_DISABLED '
  OS_PROJECTS=['3rd/SDL/SConscript']
  if TARGET_ARCH == 'x86':
    OS_FLAGS = OS_FLAGS + ' -DWITH_DOUBLE_FLOAT '
  else:
    OS_FLAGS = OS_FLAGS + ' -DWITH_64BIT_CPU '

elif OS_NAME == 'Windows':
  OS_LIBS=['gdi32', 'user32','winmm.lib','imm32.lib','version.lib','shell32.lib','ole32.lib','Oleaut32.lib','Advapi32.lib','DelayImp.lib','psapi.lib']
  OS_FLAGS='-DWIN32 -D_WIN32 -DWINDOWS /EHsc -D_CONSOLE  /DEBUG /Od  /FS /Z7 '
  #OS_FLAGS='-DWIN32 -D_WIN32 -DWINDOWS /EHsc -D_CONSOLE  /DEBUG /Od  /FS /Z7 -D_DEBUG /MDd '
  COMMON_CCFLAGS = COMMON_CCFLAGS + ' -DSDL_REAL_API -DSDL_HAPTIC_DISABLED -DSDL_SENSOR_DISABLED -DSDL_JOYSTICK_DISABLED '
  COMMON_CCFLAGS = COMMON_CCFLAGS + '-D__STDC_LIMIT_MACROS -D__STDC_FORMAT_MACROS -D__STDC_CONSTANT_MACROS -D_HAS_EXCEPTIONS=0 -D_HAS_ITERATOR_DEBUGGING=0 -D_ITERATOR_DEBUG_LEVEL=0 -D_SCL_SECURE=0'
  COMMON_CCFLAGS = COMMON_CCFLAGS + '-D_SECURE_SCL=0 -D_SCL_SECURE_NO_WARNINGS -D_CRT_SECURE_NO_WARNINGS -D_CRT_SECURE_NO_DEPRECATE '
  OS_PROJECTS=['3rd/SDL/SConscript']
  if TARGET_ARCH == 'x86':
    OS_FLAGS += OS_FLAGS + ' /MD '
    OS_LINKFLAGS='/MACHINE:X86 /DEBUG'
    OS_SUBSYSTEM_CONSOLE='/SUBSYSTEM:CONSOLE,5.01  '
    OS_SUBSYSTEM_WINDOWS='/SUBSYSTEM:WINDOWS,5.01  '
    COMMON_CCFLAGS = COMMON_CCFLAGS + ' -D_WIN32 '
  else:
    OS_FLAGS = OS_FLAGS + ' -DWITH_64BIT_CPU '
    OS_LINKFLAGS='/MACHINE:X64 /DEBUG'
    OS_SUBSYSTEM_CONSOLE='/SUBSYSTEM:CONSOLE  '
    OS_SUBSYSTEM_WINDOWS='/SUBSYSTEM:WINDOWS  '
    COMMON_CCFLAGS = COMMON_CCFLAGS + ' -D_WIN64 '

CFLAGS=COMMON_CFLAGS
LINKFLAGS=OS_LINKFLAGS;
LIBPATH=[TK_LIB_DIR] + OS_LIBPATH
CCFLAGS=OS_FLAGS + COMMON_CCFLAGS 
LIBS=['awtk'] + OS_LIBS

CPPPATH=[TK_ROOT, 
  TK_SRC, 
  TK_3RD_ROOT, 
  joinPath(TK_ROOT, 'nogui'), 
  joinPath(TK_ROOT, 'nogui/src'), 
  joinPath(TK_3RD_ROOT, 'pixman'), 
  joinPath(TK_3RD_ROOT, 'pixman/pixman'), 
  joinPath(TK_3RD_ROOT, 'cairo/cairo'), 
  joinPath(TK_3RD_ROOT, 'bgfx/bgfx/include'), 
  joinPath(TK_3RD_ROOT, 'bgfx/bx/include'), 
  joinPath(TK_3RD_ROOT, 'bgfx/bimg/include'), 
  joinPath(TK_3RD_ROOT, 'agge'), 
  joinPath(TK_3RD_ROOT, 'agg/include'), 
  joinPath(TK_3RD_ROOT, 'nanovg'), 
  joinPath(TK_3RD_ROOT, 'nanovg/gl'), 
  joinPath(TK_3RD_ROOT, 'nanovg/base'), 
  joinPath(TK_3RD_ROOT, 'nanovg/agge'), 
  joinPath(TK_3RD_ROOT, 'nanovg/bgfx'), 
  joinPath(TK_3RD_ROOT, 'SDL/src'), 
  joinPath(TK_3RD_ROOT, 'SDL/include'), 
  joinPath(TK_3RD_ROOT, 'agge/src'), 
  joinPath(TK_3RD_ROOT, 'agge/include'), 
  joinPath(TK_3RD_ROOT, 'gpinyin/include'), 
  joinPath(TK_3RD_ROOT, 'libunibreak'), 
  TK_TOOLS_ROOT] + OS_CPPPATH

os.environ['TK_ROOT'] = TK_ROOT
os.environ['CCFLAGS'] = CCFLAGS;
os.environ['GTEST_ROOT'] = GTEST_ROOT;
os.environ['TK_3RD_ROOT'] = TK_3RD_ROOT;

TOOLS_PREFIX=''
