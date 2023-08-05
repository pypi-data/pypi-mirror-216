/* Copyright (c) 2018-2023. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "simgrid/engine.h"
#include <xbt.h>

#define SIMIX_H_NO_DEPRECATED_WARNING // avoid deprecation warning on include (remove with XBT_ATTRIB_DEPRECATED_v335)
#include "simgrid/simix.h" // we don't need it, but someone must check that this file is actually usable in plain C

XBT_LOG_NEW_DEFAULT_CATEGORY(test, "Logging specific to this test");

int main(int argc, char** argv)
{
  simgrid_init(&argc, argv);

  for (int i = 1; i < argc; i++)
    XBT_INFO("argv[%d]=%s", i, argv[i]);

  return 0;
}
