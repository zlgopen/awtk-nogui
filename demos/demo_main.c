/**
 * File:   demo_main.c
 * Author: AWTK Develop Team
 * Brief:  demo main
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
 * 2018-02-16 Li XianJing <xianjimli@hotmail.com> created
 *
 */

#include "awtk.h"
#include "tkc/mem.h"
#include "tkc/fs.h"
#include "tkc/path.h"
#include "base/system_info.h"
#include "base/window_manager.h"

#include "assets.h"
ret_t application_init(void);

int main(int argc, char* argv[]) {
  tk_init(0, 0, 0, NULL, NULL);

  assets_init();
  application_init();

  tk_run();

  return 0;
}
