# frozen_string_literal: true

# Independent exact-integer checker for the coefficient-noncontracting frontier.

require "digest"
require "json"

def binomial(n, k)
  k = [k, n - k].min
  (1..k).reduce(1) { |value, index| value * (n - k + index) / index }
end

def divisors(value)
  raise ArgumentError, "value must be positive" if value < 1

  small = []
  large = []
  candidate = 1
  while candidate * candidate <= value
    if (value % candidate).zero?
      small << candidate
      large << value / candidate if candidate * candidate != value
    end
    candidate += 1
  end
  small + large.reverse
end

def euler_phi(value)
  raise ArgumentError, "value must be positive" if value < 1

  result = value
  remaining = value
  prime = 2
  while prime * prime <= remaining
    if (remaining % prime).zero?
      result -= result / prime
      remaining /= prime while (remaining % prime).zero?
    end
    prime += 1
  end
  result -= result / remaining if remaining > 1
  result
end

def binary_necklaces(length, weight)
  unless length >= 0 && weight.between?(0, length)
    raise ArgumentError, "require length >= 0 and 0 <= weight <= length"
  end
  return 1 if length.zero?

  numerator = divisors(length.gcd(weight)).sum do |divisor|
    euler_phi(divisor) * binomial(length / divisor, weight / divisor)
  end
  quotient, remainder = numerator.divmod(length)
  raise "nonintegral Burnside average" unless remainder.zero?

  quotient
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
necklace_lower_bound = binary_necklaces(depth, rational_ballot_weight)

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
puts "necklace_lower_bound=#{necklace_lower_bound}"
puts "necklace_improvement=#{necklace_lower_bound - rational_ballot_lower_bound}"
puts "distribution_sha256=#{Digest::SHA256.hexdigest(encoded)}"
puts "status=all exact checks passed"
