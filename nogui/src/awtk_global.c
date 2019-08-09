/**
 * File:   awtk.c
 * Author: AWTK Develop Team
 * Brief:  awtk
 *
 * Copyright (c) 2018 - 2019  Guangzhou ZHIYUAN Electronics Co.,Ltd.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * License file for more details.
 *
 */

/**
 * History:
 * ================================================================
 * 2018-03-03 Li XianJing <xianjimli@hotmail.com> created
 *
 */

#include "awtk.h"
#include "tkc/mem.h"
#include "base/idle.h"
#include "base/timer.h"
#include "tkc/time_now.h"
#include "base/locale_info.h"
#include "tkc/platform.h"
#include "base/main_loop.h"
#include "base/window_manager.h"
#include "base/widget_factory.h"
#include "base/assets_manager.h"

ret_t tk_init_internal(void) {
  return_value_if_fail(timer_init(time_now_ms) == RET_OK, RET_FAIL);
  return_value_if_fail(idle_manager_set(idle_manager_create()) == RET_OK, RET_FAIL);
  return_value_if_fail(widget_factory_set(widget_factory_create()) == RET_OK, RET_FAIL);
  return_value_if_fail(assets_manager_set(assets_manager_create(30)) == RET_OK, RET_FAIL);
  return_value_if_fail(window_manager_set(window_manager_create()) == RET_OK, RET_FAIL);

  return RET_OK;
}

ret_t tk_init(wh_t w, wh_t h, app_type_t app_type, const char* app_name, const char* app_root) {
  main_loop_t* loop = NULL;
  return_value_if_fail(platform_prepare() == RET_OK, RET_FAIL);
  ENSURE(system_info_init(app_type, app_name, app_root) == RET_OK);
  return_value_if_fail(tk_init_internal() == RET_OK, RET_FAIL);

  loop = main_loop_init(w, h);
  return_value_if_fail(loop != NULL, RET_FAIL);

  return RET_OK;
}

ret_t tk_deinit_internal(void) {
  widget_destroy(window_manager());
  window_manager_set(NULL);

  idle_manager_destroy(idle_manager());
  idle_manager_set(NULL);

  timer_manager_destroy(timer_manager());
  timer_manager_set(NULL);

  widget_factory_destroy(widget_factory());
  widget_factory_set(NULL);

  assets_manager_destroy(assets_manager());
  assets_manager_set(NULL);

  system_info_deinit();

  return RET_OK;
}

ret_t tk_exit(void) {
  main_loop_destroy(main_loop());
  main_loop_set(NULL);

  return tk_deinit_internal();
}

ret_t tk_run() {
  main_loop_run(main_loop());

  return tk_exit();
}

static ret_t tk_quit_idle(const timer_info_t* timer) {
  return main_loop_quit(main_loop());
}

ret_t tk_quit() {
  timer_add(tk_quit_idle, NULL, 0);
  return RET_OK;
}

ret_t tk_init_assets() {

  return RET_OK;
}

ret_t dialog_confirm(const char* stitle, const char* text) {
  return RET_OK;
}

ret_t dialog_warn(const char* title, const char* text) {
  return RET_OK;
}

ret_t dialog_info(const char* title, const char* text) {
  return RET_OK;
}

ret_t dialog_toast(const char* text, uint32_t duration) {
  return RET_OK;
}
