#include "awtk.h"
#include "base/assets_manager.h"
#ifndef WITH_FS_RES
#ifdef WITH_STB_IMAGE
#else
#endif/*WITH_STB_IMAGE*/
#ifdef WITH_VGCANVAS
#endif/*WITH_VGCANVAS*/
#if defined(WITH_STB_FONT) || defined(WITH_FT_FONT)
#else/*WITH_STB_FONT or WITH_FT_FONT*/
#endif/*WITH_STB_FONT or WITH_FT_FONT*/
#endif/*WITH_FS_RES*/

ret_t assets_init(void) {
  assets_manager_t* rm = assets_manager();

#ifdef WITH_FS_RES
  assets_manager_preload(rm, ASSET_TYPE_FONT, "default");
  assets_manager_preload(rm, ASSET_TYPE_STYLE, "default");
#else
#ifdef WITH_VGCANVAS
#endif/*WITH_VGCANVAS*/
#endif

  tk_init_assets();
  return RET_OK;
}
