/* Copyright (c) 2012-2023. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

/***************** Centralized Mutual Exclusion Algorithm *******************/
/* This example implements a centralized mutual exclusion algorithm.        */
/* Bug : CS requests of client 1 not satisfied                              */
/* LTL property checked : G(r->F(cs)); (r=request of CS, cs=CS ok)          */
/****************************************************************************/

#ifdef GARBAGE_STACK
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#endif

#include <simgrid/modelchecker.h>
#include <simgrid/s4u.hpp>
#include <xbt/dynar.h>

XBT_LOG_NEW_DEFAULT_CATEGORY(bugged1_liveness, "my log messages");
namespace sg4 = simgrid::s4u;

class Message {
public:
  enum class Kind { GRANT, REQUEST, RELEASE };
  Kind kind                             = Kind::GRANT;
  sg4::Mailbox* return_mailbox          = nullptr;
  explicit Message(Message::Kind kind, sg4::Mailbox* mbox) : kind(kind), return_mailbox(mbox) {}
};

int r  = 0;
int cs = 0;

#ifdef GARBAGE_STACK
/** Do not use a clean stack */
static void garbage_stack(void)
{
  const size_t size = 256;
  int fd            = open("/dev/urandom", O_RDONLY);
  char foo[size];
  read(fd, foo, size);
  close(fd);
}
#endif

static void coordinator()
{
  bool CS_used = false;
  std::queue<sg4::Mailbox*> requests;

  sg4::Mailbox* mbox = sg4::Mailbox::by_name("coordinator");

  while (true) {
    auto m = mbox->get_unique<Message>();
    if (m->kind == Message::Kind::REQUEST) {
      if (CS_used) {
        XBT_INFO("CS already used. Queue the request.");
        requests.push(m->return_mailbox);
      } else {
        if (m->return_mailbox->get_name() != "1") {
          XBT_INFO("CS idle. Grant immediately");
          m->return_mailbox->put(new Message(Message::Kind::GRANT, mbox), 1000);
          CS_used = true;
        }
      }
    } else {
      if (not requests.empty()) {
        XBT_INFO("CS release. Grant to queued requests (queue size: %zu)", requests.size());
        sg4::Mailbox* req = requests.front();
        requests.pop();
        if (req->get_name() != "1") {
          req->put(new Message(Message::Kind::GRANT, mbox), 1000);
        } else {
          requests.push(req);
          CS_used = false;
        }
      } else {
        XBT_INFO("CS release. resource now idle");
        CS_used = false;
      }
    }
  }
}

static void client(int id)
{
  aid_t my_pid = sg4::this_actor::get_pid();

  sg4::Mailbox* my_mailbox = sg4::Mailbox::by_name(std::to_string(id));

  while (true) {
    XBT_INFO("Ask the request");
    sg4::Mailbox::by_name("coordinator")->put(new Message(Message::Kind::REQUEST, my_mailbox), 1000);

    if (id == 1) {
      r  = 1;
      cs = 0;
      XBT_INFO("Propositions changed : r=1, cs=0");
    }

    auto grant = my_mailbox->get_unique<Message>();
    xbt_assert(grant->kind == Message::Kind::GRANT);

    if (id == 1) {
      cs = 1;
      r  = 0;
      XBT_INFO("Propositions changed : r=0, cs=1");
    }

    XBT_INFO("%d got the answer. Sleep a bit and release it", id);

    sg4::this_actor::sleep_for(1);

    sg4::Mailbox::by_name("coordinator")->put(new Message(Message::Kind::RELEASE, my_mailbox), 1000);

    sg4::this_actor::sleep_for(static_cast<double>(my_pid));

    if (id == 1) {
      cs = 0;
      r  = 0;
      XBT_INFO("Propositions changed : r=0, cs=0");
    }
  }
}

static void raw_client(int id)
{
#ifdef GARBAGE_STACK
  // At this point the stack of the callee (client) is probably filled with
  // zeros and uninitialized variables will contain 0. This call will place
  // random byes in the stack of the callee:
  garbage_stack();
#endif
  client(id);
}

int main(int argc, char* argv[])
{
  sg4::Engine e(&argc, argv);

  MC_automaton_new_propositional_symbol_pointer("r", &r);
  MC_automaton_new_propositional_symbol_pointer("cs", &cs);

  e.load_platform(argv[1]);

  sg4::Actor::create("coordinator", e.host_by_name("Tremblay"), coordinator)
      ->set_kill_time(argc > 3 ? std::stod(argv[3]) : -1.0);
  if (std::stod(argv[2]) == 0) {
    sg4::Actor::create("client", e.host_by_name("Boivin"), raw_client, 1);
    sg4::Actor::create("client", e.host_by_name("Fafard"), raw_client, 2);
  } else { // "Visited" case
    sg4::Actor::create("client", e.host_by_name("Boivin"), raw_client, 2);
    sg4::Actor::create("client", e.host_by_name("Fafard"), raw_client, 1);
  }
  e.run();

  return 0;
}
