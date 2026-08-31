#!/usr/bin/env ruby
# Independent exact-integer check of verify_cycle_lower_bound.py.

barina_exclusive_limit = 1 << 71
hercher_x0_threshold = 1536 * (1 << 60)
hercher_strict_odd_bound = 137_500_000_000
lower_p = 1_686_221
lower_q = 1_063_887
upper_p = 301_994
upper_q = 190_537

raise "Barina limit does not reach Hercher threshold" unless
  barina_exclusive_limit - 1 >= hercher_x0_threshold
raise "lower rational is not below log_2(3)" unless 3**lower_q > 2**lower_p
raise "upper rational is not above log_2(3)" unless 3**upper_q < 2**upper_p

odd_entries_min = hercher_strict_odd_bound + 1
lower_floor = (lower_p * odd_entries_min).div(lower_q)
upper_floor = (upper_p * odd_entries_min).div(upper_q)
raise "rational bounds do not determine the floor" unless lower_floor == upper_floor
shortcut_entries_min = lower_floor + 1
classical_entries_min = shortcut_entries_min + odd_entries_min

expected = [137_500_000_001, 217_932_343_851, 355_432_343_852]
actual = [odd_entries_min, shortcut_entries_min, classical_entries_min]
raise "unexpected lower bounds: #{actual.inspect}" unless actual == expected

puts "odd_entries_min=#{odd_entries_min}"
puts "shortcut_entries_min=#{shortcut_entries_min}"
puts "classical_entries_min=#{classical_entries_min}"
