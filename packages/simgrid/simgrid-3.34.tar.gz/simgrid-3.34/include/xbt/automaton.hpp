/* Copyright (c) 2015-2023. The SimGrid Team.
 * All rights reserved.                                                     */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#ifndef XBT_AUTOMATON_HPP
#define XBT_AUTOMATON_HPP

#include <utility>

#include <xbt/automaton.h>

namespace simgrid::xbt {

/** Add a proposition to an automaton (the C++ way)
 *
 *  This API hides all the callback and dynamic allocation hell from
 *  the used which can use C++ style functors and lambda expressions.
 */
template <class F> xbt_automaton_propositional_symbol_t add_proposition(const_xbt_automaton_t a, const char* id, F f)
{
  auto* callback = new F(std::move(f));
  return xbt_automaton_propositional_symbol_new_callback(
      a, id, [](auto* cb) -> int { return (*(F*)cb)(); }, callback, [](auto* cb) -> void { delete (F*)cb; });
}

} // namespace simgrid::xbt
#endif
