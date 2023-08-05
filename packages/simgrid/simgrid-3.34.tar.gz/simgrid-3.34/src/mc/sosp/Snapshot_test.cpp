/* Copyright (c) 2014-2023. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "src/3rd-party/catch.hpp"
#include "src/mc/mc_config.hpp"
#include "src/mc/sosp/Snapshot.hpp"

#include <cstddef>
#include <memory>
#include <sys/mman.h>
#include <xbt/random.hpp>

class snap_test_helper {
  simgrid::mc::PageStore page_store_{500};
  simgrid::mc::RemoteProcessMemory memory_{getpid(), nullptr};

  struct prologue_return {
    size_t size;
    std::byte* src;
    std::byte* dstn;
    std::unique_ptr<simgrid::mc::Region> region0;
    std::unique_ptr<simgrid::mc::Region> region;
  };
  prologue_return prologue(int n); // common to the below 5 fxs

  static void init_memory(std::byte* mem, size_t size);

public:
  void read_whole_region();
  void read_region_parts();
  void compare_whole_region();
  void compare_region_parts();
  void read_pointer();

  static void basic_requirements();
};

void snap_test_helper::init_memory(std::byte* mem, size_t size)
{
  std::generate_n(mem, size, []() { return static_cast<std::byte>(simgrid::xbt::random::uniform_int(0, 0xff)); });
}

void snap_test_helper::basic_requirements()
{
  REQUIRE(xbt_pagesize == getpagesize());
  REQUIRE(1 << xbt_pagebits == xbt_pagesize);
}

snap_test_helper::prologue_return snap_test_helper::prologue(int n)
{
  // Store region page(s):
  size_t byte_size = n * xbt_pagesize;
  auto* source =
      static_cast<std::byte*>(mmap(nullptr, byte_size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0));
  INFO("Could not allocate source memory");
  REQUIRE(source != MAP_FAILED);

  // Init memory and take snapshots:
  init_memory(source, byte_size);
  auto region0 =
      std::make_unique<simgrid::mc::Region>(page_store_, memory_, simgrid::mc::RegionType::Data, source, byte_size);
  for (int i = 0; i < n; i += 2) {
    init_memory(source + i * xbt_pagesize, xbt_pagesize);
  }
  auto region =
      std::make_unique<simgrid::mc::Region>(page_store_, memory_, simgrid::mc::RegionType::Data, source, byte_size);

  auto* destination =
      static_cast<std::byte*>(mmap(nullptr, byte_size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0));
  INFO("Could not allocate destination memory");
  REQUIRE(destination != MAP_FAILED);

  return {.size    = byte_size,
          .src     = source,
          .dstn    = destination,
          .region0 = std::move(region0),
          .region  = std::move(region)};
}

void snap_test_helper::read_whole_region()
{
  for (int n = 1; n != 32; ++n) {
    prologue_return ret = prologue(n);
    const void* read    = ret.region->read(ret.dstn, ret.src, ret.size);
    INFO("Mismatch in MC_region_read()");
    REQUIRE(not memcmp(ret.src, read, ret.size));

    munmap(ret.dstn, ret.size);
    munmap(ret.src, ret.size);
  }
}

void snap_test_helper::read_region_parts()
{
  for (int n = 1; n != 32; ++n) {
    prologue_return ret = prologue(n);

    for (int j = 0; j != 100; ++j) {
      size_t offset    = simgrid::xbt::random::uniform_int(0, ret.size - 1);
      size_t size      = simgrid::xbt::random::uniform_int(0, ret.size - offset - 1);
      const void* read = ret.region->read(ret.dstn, (const char*)ret.src + offset, size);
      INFO("Mismatch in MC_region_read()");
      REQUIRE(not memcmp((char*)ret.src + offset, read, size));
    }
    munmap(ret.dstn, ret.size);
    munmap(ret.src, ret.size);
  }
}

void snap_test_helper::compare_whole_region()
{
  for (int n = 1; n != 32; ++n) {
    prologue_return ret = prologue(n);

    INFO("Unexpected match in MC_snapshot_region_memcmp() with previous snapshot");
    REQUIRE(MC_snapshot_region_memcmp(ret.src, ret.region0.get(), ret.src, ret.region.get(), ret.size));

    munmap(ret.dstn, ret.size);
    munmap(ret.src, ret.size);
  }
}

void snap_test_helper::compare_region_parts()
{
  for (int n = 1; n != 32; ++n) {
    prologue_return ret = prologue(n);

    for (int j = 0; j != 100; ++j) {
      size_t offset = simgrid::xbt::random::uniform_int(0, ret.size - 1);
      size_t size   = simgrid::xbt::random::uniform_int(0, ret.size - offset - 1);

      INFO("Mismatch in MC_snapshot_region_memcmp()");
      REQUIRE(not MC_snapshot_region_memcmp((char*)ret.src + offset, ret.region.get(), (char*)ret.src + offset,
                                            ret.region.get(), size));
    }
    munmap(ret.dstn, ret.size);
    munmap(ret.src, ret.size);
  }
}

const int some_global_variable  = 42;
const void* const some_global_pointer = &some_global_variable;
void snap_test_helper::read_pointer()
{
  prologue_return ret = prologue(1);
  memcpy(ret.src, &some_global_pointer, sizeof(void*));
  const simgrid::mc::Region region2(page_store_, memory_, simgrid::mc::RegionType::Data, ret.src, ret.size);
  INFO("Mismtach in MC_region_read_pointer()");
  REQUIRE(MC_region_read_pointer(&region2, ret.src) == some_global_pointer);

  munmap(ret.dstn, ret.size);
  munmap(ret.src, ret.size);
}

/*************** End: class snap_test_helper *****************************/

TEST_CASE("MC::Snapshot: A copy/snapshot of a given memory region", "MC::Snapshot")
{
  INFO("Sparse snapshot (using pages)");

  snap_test_helper::basic_requirements();

  snap_test_helper snap_test;

  INFO("Read whole region");
  snap_test.read_whole_region();

  INFO("Read region parts");
  snap_test.read_region_parts();

  INFO("Compare whole region");
  snap_test.compare_whole_region();

  INFO("Compare region parts");
  snap_test.compare_region_parts();

  INFO("Read pointer");
  snap_test.read_pointer();
}
