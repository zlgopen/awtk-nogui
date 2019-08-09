import os
import copy

BIN_DIR=os.environ['BIN_DIR'];
LIB_DIR=os.environ['LIB_DIR'];

sources=Glob('src/*/*.c')
sources +=Glob('src/platforms/pc/*.c')
sources +=Glob('nogui/src/*/*.c')
sources +=Glob('nogui/src/*.c')

env=DefaultEnvironment().Clone()
env.Library(os.path.join(LIB_DIR, 'awtk'), sources)

sources=Glob('demos/*.c')
env.Program(os.path.join(BIN_DIR, 'demo'), sources);
