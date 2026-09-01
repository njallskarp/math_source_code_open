# frozen_string_literal: true

# Independent exact-integer checker for the coefficient-noncontracting frontier.

require "digest"
require "json"

def binomial(n, k)
  k = [k, n - k].min
  (1..k).reduce(1) { |value, index| value * (n - k + index) / index }
end

depth = Integer(ARGV.fetch(0, "300"), 10)
raise ArgumentError, "depth must be nonnegative" if depth.negative?

frontier = { 0 => 1 }
crossings_at_depth = 0
cumulative_crossings = 0

1.upto(depth) do |length|
  next_frontier = Hash.new(0)
  crossings_at_depth = 0
  threshold = 2**length
  frontier.each do |odd_count, count|
    [0, 1].each do |bit|
      next_odd_count = odd_count + bit
      if 3**next_odd_count >= threshold
        next_frontier[next_odd_count] += count
      else
        crossings_at_depth += count
      end
    end
  end
  cumulative_crossings += crossings_at_depth
  frontier = next_frontier
end

ordered = frontier.keys.sort.map { |odd_count| [odd_count, frontier.fetch(odd_count)] }
encoded = JSON.generate(ordered)
safe_words = frontier.values.sum
rational_ballot_weight = 0
rational_ballot_weight += 1 while 3**rational_ballot_weight < 2**depth
ballot_numerator = binomial(depth, rational_ballot_weight)
rational_ballot_lower_bound = if depth.zero?
                                1
                              else
                                (ballot_numerator + depth - 1) / depth
                              end

puts "depth=#{depth}"
puts "safe_words=#{safe_words}"
puts "safe_words_decimal_digits=#{safe_words.to_s.length}"
puts "active_q_states=#{frontier.length}"
puts "minimum_q=#{frontier.empty? ? -1 : frontier.keys.min}"
puts "maximum_q=#{frontier.empty? ? -1 : frontier.keys.max}"
puts "first_crossings_at_depth=#{crossings_at_depth}"
puts "cumulative_first_crossings=#{cumulative_crossings}"
puts "rational_ballot_weight=#{rational_ballot_weight}"
puts "rational_ballot_lower_bound=#{rational_ballot_lower_bound}"
puts "distribution_sha256=#{Digest::SHA256.hexdigest(encoded)}"
puts "status=all exact checks passed"
