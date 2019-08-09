/**
 * File:   main_loop_sdl.c
 * Author: AWTK Develop Team
 * Brief:  dummy implemented main_loop interface
 *
 * Copyright (c) 2018 - 2019  Guangzhou ZHIYUAN Electronics Co.,Ltd.
 *
 * this program is distributed in the hope that it will be useful,
 * but without any warranty; without even the implied warranty of
 * merchantability or fitness for a particular purpose.  see the
 * license file for more details.
 *
 */

/**
 * history:
 * ================================================================
 * 2018-01-13 li xianjing <xianjimli@hotmail.com> created
 *
 */

#include "main_loop/main_loop_simple.h"
#include "base/window_manager.h"
#include "base/idle.h"
#include "base/events.h"
#include "base/timer.h"

#include <stdio.h>
#include "tkc/time_now.h"
#include "base/input_method.h"

static ret_t main_loop_dummy_destroy(main_loop_t* l) {
  main_loop_simple_t* loop = (main_loop_simple_t*)l;

  main_loop_simple_reset(loop);

  return RET_OK;
}

main_loop_t* main_loop_init(int w, int h) {
  main_loop_simple_t* loop = NULL;
  loop = main_loop_simple_init(w, h);
  loop->base.destroy = main_loop_dummy_destroy;

  return (main_loop_t*)loop;
}
