/* Copyright (c) 2019-2023. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#ifndef SIMGRID_MC_MUTEX_OBSERVER_HPP
#define SIMGRID_MC_MUTEX_OBSERVER_HPP

#include "simgrid/forward.h"
#include "src/kernel/activity/MutexImpl.hpp"
#include "src/kernel/actor/ActorImpl.hpp"
#include "src/kernel/actor/SimcallObserver.hpp"

#include <string>

namespace simgrid::kernel::actor {

/* All the observers of Mutex transitions are very similar, so implement them all together in this class */
class MutexObserver final : public SimcallObserver {
  mc::Transition::Type type_;
  activity::MutexImpl* const mutex_;

public:
  MutexObserver(ActorImpl* actor, mc::Transition::Type type, activity::MutexImpl* mutex);

  void serialize(std::stringstream& stream) const override;
  std::string to_string() const override;
  bool is_enabled() override;

  activity::MutexImpl* get_mutex() const { return mutex_; }
};

/* This observer is used for SEM_LOCK and SEM_UNLOCK (only) */
class SemaphoreObserver final : public SimcallObserver {
  mc::Transition::Type type_;
  activity::SemaphoreImpl* const sem_;

public:
  SemaphoreObserver(ActorImpl* actor, mc::Transition::Type type, activity::SemaphoreImpl* sem);

  void serialize(std::stringstream& stream) const override;
  std::string to_string() const override;

  activity::SemaphoreImpl* get_sem() const { return sem_; }
};

/* This observer is ued for SEM_WAIT, that is returning and needs the acquisition (in MC mode) */
class SemaphoreAcquisitionObserver final : public ResultingSimcall<bool> {
  mc::Transition::Type type_;
  activity::SemAcquisitionImpl* const acquisition_;
  const double timeout_;

public:
  SemaphoreAcquisitionObserver(ActorImpl* actor, mc::Transition::Type type, activity::SemAcquisitionImpl* acqui,
                               double timeout = -1.0);

  void serialize(std::stringstream& stream) const override;
  std::string to_string() const override;
  bool is_enabled() override;

  double get_timeout() const { return timeout_; }
};

/* This observer is used for BARRIER_LOCK and BARRIER_WAIT. WAIT is returning and needs the acquisition */
class BarrierObserver final : public ResultingSimcall<bool> {
  mc::Transition::Type type_;
  activity::BarrierImpl* const barrier_                = nullptr;
  activity::BarrierAcquisitionImpl* const acquisition_ = nullptr;
  const double timeout_;

public:
  BarrierObserver(ActorImpl* actor, mc::Transition::Type type, activity::BarrierImpl* bar);
  BarrierObserver(ActorImpl* actor, mc::Transition::Type type, activity::BarrierAcquisitionImpl* acqui,
                  double timeout = -1.0);

  void serialize(std::stringstream& stream) const override;
  std::string to_string() const override;
  bool is_enabled() override;

  double get_timeout() const { return timeout_; }
};

} // namespace simgrid::kernel::actor

#endif
