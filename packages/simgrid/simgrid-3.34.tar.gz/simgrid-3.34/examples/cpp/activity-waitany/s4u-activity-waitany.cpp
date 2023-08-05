/* Copyright (c) 2010-2023. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "simgrid/s4u.hpp"
#include <cstdlib>
#include <iostream>
#include <string>
namespace sg4 = simgrid::s4u;

XBT_LOG_NEW_DEFAULT_CATEGORY(s4u_activity_waittany, "Messages specific for this s4u example");

static void bob()
{
  sg4::Mailbox* mbox    = sg4::Mailbox::by_name("mbox");
  const sg4::Disk* disk = sg4::Host::current()->get_disks().front();
  std::string* payload;

  XBT_INFO("Create my asynchronous activities");
  auto exec = sg4::this_actor::exec_async(5e9);
  auto comm = mbox->get_async(&payload);
  auto io   = disk->read_async(3e8);

  std::vector<sg4::ActivityPtr> pending_activities = {boost::dynamic_pointer_cast<sg4::Activity>(exec),
                                                      boost::dynamic_pointer_cast<sg4::Activity>(comm),
                                                      boost::dynamic_pointer_cast<sg4::Activity>(io)};

  XBT_INFO("Wait for asynchrounous activities to complete");
  while (not pending_activities.empty()) {
    ssize_t changed_pos = sg4::Activity::wait_any(pending_activities);
    if (changed_pos != -1) {
      auto* completed_one = pending_activities[changed_pos].get();
      if (dynamic_cast<sg4::Comm*>(completed_one))
        XBT_INFO("Completed a Comm");
      if (dynamic_cast<sg4::Exec*>(completed_one))
        XBT_INFO("Completed an Exec");
      if (dynamic_cast<sg4::Io*>(completed_one))
        XBT_INFO("Completed an I/O");
      pending_activities.erase(pending_activities.begin() + changed_pos);
    }
  }
  XBT_INFO("Last activity is complete");
  delete payload;
}

static void alice()
{
  auto* payload = new std::string("Message");
  XBT_INFO("Send '%s'", payload->c_str());
  sg4::Mailbox::by_name("mbox")->put(payload, 6e8);
}

int main(int argc, char* argv[])
{
  sg4::Engine e(&argc, argv);

  e.load_platform(argv[1]);

  sg4::Actor::create("bob", e.host_by_name("bob"), bob);
  sg4::Actor::create("alice", e.host_by_name("alice"), alice);

  e.run();

  return 0;
}
