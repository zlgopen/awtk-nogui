/**
 * File:   window_manager_default.c
 * Author: AWTK Develop Team
 * Brief:  default window manager
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
 * 2018-01-13 Li XianJing <xianjimli@hotmail.com> created
 *
 */

#include "tkc/mem.h"
#include "base/keys.h"
#include "base/idle.h"
#include "tkc/utils.h"
#include "base/timer.h"
#include "base/layout.h"
#include "tkc/time_now.h"
#include "widgets/dialog.h"
#include "base/locale_info.h"
#include "base/system_info.h"
#include "base/image_manager.h"
#include "base/dialog_highlighter_factory.h"
#include "window_manager/window_manager_default.h"

static ret_t window_manager_dispatch_window_event(widget_t* window, event_type_t type) {
  window_event_t evt;
  event_t e = event_init(type, window);
  widget_dispatch(window, &e);

  evt.window = window;
  evt.e = event_init(type, window->parent);
  return widget_dispatch(window->parent, (event_t*)&(evt));
}

static ret_t window_manager_dispatch_window_open(widget_t* curr_win) {
  window_manager_dispatch_window_event(curr_win, EVT_WINDOW_WILL_OPEN);

  return window_manager_dispatch_window_event(curr_win, EVT_WINDOW_OPEN);
}

static ret_t window_manager_default_open_window(widget_t* widget, widget_t* window) {
  ret_t ret = RET_OK;
  return_value_if_fail(widget != NULL && window != NULL, RET_BAD_PARAMS);

  window_manager_dispatch_window_open(window);
  ret = widget_add_child(widget, window);
  return_value_if_fail(ret == RET_OK, RET_FAIL);

  window->dirty = FALSE;
  widget->target = window;
  widget->key_target = window;

  return ret;
}

static ret_t window_manager_prepare_close_window(widget_t* widget, widget_t* window) {
  return_value_if_fail(widget != NULL && window != NULL, RET_BAD_PARAMS);

  if (widget->target == window) {
    widget->target = NULL;
  }

  if (widget->key_target == window) {
    widget->key_target = NULL;
  }

  if (widget->grab_widget != NULL) {
    if (widget->grab_widget == window) {
      widget->grab_widget = NULL;
    }
  }

  return RET_OK;
}

static ret_t window_manager_default_close_window_force(widget_t* widget, widget_t* window) {
  window_manager_default_t* wm = WINDOW_MANAGER_DEFAULT(widget);

  return_value_if_fail(wm != NULL, RET_BAD_PARAMS);
  return_value_if_fail(widget_is_window(window), RET_BAD_PARAMS);

  window_manager_prepare_close_window(widget, window);
  window_manager_dispatch_window_event(window, EVT_WINDOW_CLOSE);
  widget_remove_child(widget, window);
  widget_destroy(window);

  return RET_OK;
}

static ret_t window_manager_default_close_window(widget_t* widget, widget_t* window) {
  return window_manager_default_close_window_force(widget, window);
}


static ret_t window_manager_default_paint(widget_t* widget) {
  return RET_OK;
}

static ret_t window_manager_default_dispatch_input_event(widget_t* widget, event_t* e) {
  input_device_status_t* ids = NULL;
  window_manager_default_t* wm = WINDOW_MANAGER_DEFAULT(widget);
  return_value_if_fail(wm != NULL && e != NULL, RET_BAD_PARAMS);

  native_window_preprocess_event(wm->native_window, e);
  ids = &(wm->input_device_status);
  if (wm->ignore_user_input) {
    if (ids->pressed && e->type == EVT_POINTER_UP) {
      log_debug("animating ignore input, but it is last pointer_up\n");
    } else {
      log_debug("animating ignore input\n");
      return RET_OK;
    }
  }

  input_device_status_on_input_event(ids, widget, e);

  return RET_OK;
}

ret_t window_manager_paint_system_bar(widget_t* widget, canvas_t* c) {
  return RET_OK;
}

static ret_t window_manager_default_post_init(widget_t* widget, wh_t w, wh_t h) {
  return RET_OK;
}

static window_manager_vtable_t s_window_manager_self_vtable = {
    .paint = window_manager_default_paint,
    .post_init = window_manager_default_post_init,
    .open_window = window_manager_default_open_window,
    .close_window = window_manager_default_close_window,
    .close_window_force = window_manager_default_close_window_force,
    .dispatch_input_event = window_manager_default_dispatch_input_event,
};

static const widget_vtable_t s_window_manager_vtable = {
    .size = sizeof(window_manager_t),
    .is_window_manager = TRUE,
    .type = WIDGET_TYPE_WINDOW_MANAGER,
};

widget_t* window_manager_create(void) {
  window_manager_default_t* wm = TKMEM_ZALLOC(window_manager_default_t);
  return_value_if_fail(wm != NULL, NULL);

  return window_manager_init(WINDOW_MANAGER(wm), &s_window_manager_vtable,
                             &s_window_manager_self_vtable);
}
