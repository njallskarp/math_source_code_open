#!/usr/bin/env ruby
# Independent exact-integer check of verify_cycle_lower_bound.py.

barina_exclusive_limit = 1 << 71
hercher_x0_threshold = 1536 * (1 << 60)
hercher_strict_odd_bound = 137_500_000_000
p = 1054
q = 665

raise "Barina limit does not reach Hercher threshold" unless
  barina_exclusive_limit - 1 >= hercher_x0_threshold
raise "1054/665 is not a certified lower bound" unless 3**q > 2**p

odd_entries_min = hercher_strict_odd_bound + 1
shortcut_entries_min = (p * odd_entries_min).div(q) + 1
classical_entries_min = shortcut_entries_min + odd_entries_min

expected = [137_500_000_001, 217_932_330_829, 355_432_330_830]
actual = [odd_entries_min, shortcut_entries_min, classical_entries_min]
raise "unexpected lower bounds: #{actual.inspect}" unless actual == expected

puts "odd_entries_min=#{odd_entries_min}"
puts "shortcut_entries_min=#{shortcut_entries_min}"
puts "classical_entries_min=#{classical_entries_min}"
