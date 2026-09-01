# frozen_string_literal: true

# Independent exact-integer verifier for block composition and lift intervals.

require "digest"
require "json"

def words(length)
  return [[]] if length.zero?

  (0...(2**length)).map do |value|
    value.to_s(2).rjust(length, "0").chars.map(&:to_i)
  end
end

def affine_offset(word)
  word.each_with_index.reduce(0) do |offset, (bit, index)|
    (bit == 1 ? 3 : 1) * offset + bit * 2**index
  end
end

def extended_gcd(a, b)
  return [a, 1, 0] if b.zero?

  divisor, x1, y1 = extended_gcd(b, a % b)
  [divisor, y1, x1 - (a / b) * y1]
end

def inverse_mod(value, modulus)
  divisor, inverse, = extended_gcd(value, modulus)
  raise "noninvertible" unless divisor == 1

  inverse % modulus
end

def cylinder(word)
  length = word.length
  odd_count = word.sum
  offset = affine_offset(word)
  modulus = 2**length
  residue = modulus == 1 ? 0 : (-offset * inverse_mod(3**odd_count, modulus)) % modulus
  endpoint, remainder = (3**odd_count * residue + offset).divmod(modulus)
  raise "nonintegral endpoint" unless remainder.zero?

  [length, odd_count, residue, endpoint, offset]
end

def shortcut_step(value)
  value.odd? ? (3 * value + 1) / 2 : value / 2
end

def trajectory(word, start)
  values = [start]
  word.each do |bit|
    raise "parity mismatch" unless start % 2 == bit

    start = shortcut_step(start)
    values << start
  end
  values
end

def safe_interval(word)
  length, = cylinder(word)
  _, _, residue, = cylinder(word)
  lower = residue.zero? ? 1 : 0
  upper = nil
  value = residue
  odd_count = 0
  word.each_with_index do |bit, index|
    odd_count += bit
    value = shortcut_step(value)
    intercept = value - residue
    slope = 3**odd_count * 2**(length - index - 1) - 2**length
    if slope.positive?
      lower = [lower, -(intercept.div(slope))].max
    elsif slope.zero?
      return nil if intercept.negative?
    else
      return nil if intercept.negative?

      candidate = intercept.div(-slope)
      upper = upper.nil? ? candidate : [upper, candidate].min
    end
    return nil unless upper.nil? || lower <= upper
  end
  [[lower, 0].max, upper]
end

def compose(left, right)
  k, q, r, s, left_offset = cylinder(left)
  h, p, right_residue, right_endpoint, right_offset = cylinder(right)
  modulus = 2**h
  lift = if modulus == 1
           0
         else
           ((right_residue - s) * inverse_mod(3**q, modulus)) % modulus
         end
  intermediate = s + 3**q * lift
  quotient, remainder = (intermediate - right_residue).divmod(modulus)
  raise "incompatible block" unless remainder.zero? && quotient >= 0

  [
    k + h,
    q + p,
    r + 2**k * lift,
    right_endpoint + 3**p * quotient,
    3**p * left_offset + 2**k * right_offset
  ]
end

max_length = Integer(ARGV.fetch(0, "10"), 10)
raise ArgumentError, "max length must be nonnegative" if max_length.negative?

records = []
words_checked = 0
compositions_checked = 0
lifts_checked = 0
0.upto(max_length) do |length|
  words(length).each do |word|
    words_checked += 1
    data = cylinder(word)
    interval = safe_interval(word)
    records << [word.join, interval&.at(0), interval&.at(1)]
    0.upto(20) do |lift|
      start = data[2] + 2**length * lift
      values = trajectory(word, start)
      survives = start.positive? && values.drop(1).all? { |value| value >= start }
      represented = !interval.nil? && lift >= interval[0] &&
                    (interval[1].nil? || lift <= interval[1])
      raise "interval mismatch" unless survives == represented

      lifts_checked += 1
    end
    0.upto(length) do |split|
      raise "composition mismatch" unless compose(word.take(split), word.drop(split)) == data

      compositions_checked += 1
    end
  end
end

puts "max_length=#{max_length}"
puts "words_checked=#{words_checked}"
puts "lifts_checked=#{lifts_checked}"
puts "compositions_checked=#{compositions_checked}"
puts "interval_sha256=#{Digest::SHA256.hexdigest(JSON.generate(records))}"

frontier = [[[], 0]]
first_crossings = 0
trivial_intervals = 0
unexpected_intervals = 0
1.upto(20) do |depth|
  next_frontier = []
  frontier.each do |word, odd_count|
    [0, 1].each do |bit|
      extension = word + [bit]
      next_odd_count = odd_count + bit
      if 3**next_odd_count >= 2**depth
        next_frontier << [extension, next_odd_count]
        next
      end
      first_crossings += 1
      interval = safe_interval(extension)
      next if interval.nil?

      if extension == [1, 0] && interval == [0, 0]
        trivial_intervals += 1
      else
        unexpected_intervals += 1
      end
    end
  end
  frontier = next_frontier
end
puts "cst_audit_depth=20"
puts "cst_first_crossings_checked=#{first_crossings}"
puts "cst_trivial_intervals=#{trivial_intervals}"
puts "cst_unexpected_intervals=#{unexpected_intervals}"
puts "cst_safe_frontier_at_depth=#{frontier.length}"
puts "status=all exact checks passed"
