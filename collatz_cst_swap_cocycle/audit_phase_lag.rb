#!/usr/bin/env ruby
# Independent direct-formula audit of the normalized Collatz phase lag.

require "digest"

def inverse_mod(value, modulus)
  return 0 if modulus == 1
  old_r, r = value, modulus
  old_s, s = 1, 0
  until r.zero?
    quotient = old_r / r
    old_r, r = r, old_r - quotient * r
    old_s, s = s, old_s - quotient * s
  end
  raise "noninvertible" unless old_r == 1
  old_s % modulus
end

def popcount(value)
  value.to_s(2).count("1")
end

# This implementation does not use the cylinder-lifting recurrence in the
# Python checker.  It composes the affine numerator directly and solves its
# final congruence for the canonical residue.
def direct_state(bits, length)
  power_three = 1
  numerator = 0
  length.times do |position|
    next if ((bits >> position) & 1).zero?
    numerator = 3 * numerator + (1 << position)
    power_three *= 3
  end
  modulus = 1 << length
  residue = (-numerator * inverse_mod(power_three, modulus)) % modulus
  endpoint = (power_three * residue + numerator) / modulus
  [power_three, numerator, residue, endpoint]
end

def gap_coordinates(modulus, power_three, numerator, residue, endpoint)
  gap = modulus - power_three
  mu = gap == 1 ? 0 : (-numerator * inverse_mod(power_three, gap)) % gap
  kappa, remainder = (modulus * mu + numerator).divmod(modulus * gap)
  raise "window residue" unless remainder == residue * gap
  raise "window margin" unless residue - endpoint == mu - gap * kappa
  [gap, mu, kappa]
end

def chronological_word(bits, length)
  (0...length).map { |position| (bits >> position) & 1 }.join
end

def audit(max_length)
  digest = Digest::SHA256.new
  contracting_words = 0
  adjacent_edges = 0
  phase_lag_failures = 0
  window_failures = 0
  full_less_circle = 0
  full_equal_circle = 0
  full_greater_circle = 0
  zero_index_source_edges = 0
  zero_index_source_equal = 0
  zero_index_source_strict = 0
  zero_index_source_antidominance_failures = 0
  maximum_window_index = 0
  first_strict = nil

  (2..max_length).each do |length|
    modulus = 1 << length
    states = {}
    coordinates = {}
    (0...modulus).each do |bits|
      state = direct_state(bits, length)
      next unless state[0] < modulus
      states[bits] = state
      coordinates[bits] = gap_coordinates(modulus, *state)
    end
    contracting_words += states.length
    maximum_window_index = [maximum_window_index,
                            coordinates.values.map(&:last).max].max

    states.keys.sort.each do |bits|
      power_three, source_b, source_r, source_z = states.fetch(bits)
      gap, source_mu, source_kappa = coordinates.fetch(bits)
      (0...(length - 1)).each do |position|
        next unless ((bits >> position) & 3) == 2
        target_bits = bits ^ (3 << position)
        _, target_b, target_r, target_z = states.fetch(target_bits)
        _, target_mu, target_kappa = coordinates.fetch(target_bits)
        prefix_ones = popcount(bits & ((1 << position) - 1))
        suffix_ones = popcount(bits >> (position + 2))
        local_modulus = 1 << (length - position)
        inverse = inverse_mod(3**(prefix_ones + 1), local_modulus)
        displacement = (1 << position) * inverse
        numerator_drop = (1 << position) * 3**suffix_ones
        jump, remainder = (gap * inverse + 3**suffix_ones).divmod(local_modulus)
        raise "jump integrality" unless remainder.zero?

        phase_lag_failures += 1 unless modulus * jump ==
                                               gap * displacement + numerator_drop
        phase_lag_failures += 1 unless source_b - target_b == numerator_drop
        phase_lag_failures += 1 unless gap * (source_r + displacement) ==
                                               modulus * (source_mu + jump -
                                               gap * source_kappa) + target_b

        full_wrap = (source_r + displacement) / modulus
        circle_wrap = (source_mu + jump) / gap
        phase_lag_failures += 1 unless target_r == source_r + displacement -
                                                    modulus * full_wrap
        phase_lag_failures += 1 unless target_mu == source_mu + jump -
                                                      gap * circle_wrap
        window_failures += 1 unless target_kappa - source_kappa ==
                                            full_wrap - circle_wrap

        if full_wrap < circle_wrap
          full_less_circle += 1
        elsif full_wrap == circle_wrap
          full_equal_circle += 1
        else
          full_greater_circle += 1
        end

        if source_kappa.zero?
          zero_index_source_edges += 1
          if full_wrap < circle_wrap || ![0, 1].include?(target_kappa)
            zero_index_source_antidominance_failures += 1
          end
          if full_wrap == circle_wrap
            zero_index_source_equal += 1
          elsif full_wrap > circle_wrap
            zero_index_source_strict += 1
            first_strict ||= [
              length, chronological_word(bits, length),
              chronological_word(target_bits, length), position,
              popcount(bits), gap, source_r, source_z, source_b, source_mu,
              source_kappa, target_r, target_z, target_b, target_mu,
              target_kappa, displacement, numerator_drop, jump, full_wrap,
              circle_wrap
            ]
          end
        end

        adjacent_edges += 1
        digest << format("%d,%x,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n",
                         length, bits, position, source_r, target_r, source_b,
                         target_b, source_mu, target_mu, source_kappa,
                         target_kappa, displacement, numerator_drop, jump,
                         full_wrap, circle_wrap)
      end
    end
  end

  raise "strict defect not found" if first_strict.nil?
  labels = %w[K source target j q d source_r source_z source_B source_mu
              source_kappa target_r target_z target_B target_mu target_kappa
              delta E J W C]
  first_record = labels.zip(first_strict).map { |key, value| "#{key}=#{value}" }.join(";")
  {
    max_length: max_length,
    contracting_words: contracting_words,
    adjacent_edges: adjacent_edges,
    phase_lag_failures: phase_lag_failures,
    window_failures: window_failures,
    full_less_circle: full_less_circle,
    full_equal_circle: full_equal_circle,
    full_greater_circle: full_greater_circle,
    zero_index_source_edges: zero_index_source_edges,
    zero_index_source_equal: zero_index_source_equal,
    zero_index_source_strict: zero_index_source_strict,
    zero_index_source_antidominance_failures: zero_index_source_antidominance_failures,
    maximum_window_index: maximum_window_index,
    first_zero_index_source_strict_defect: first_record,
    sha256: digest.hexdigest
  }
end

max_length = Integer(ARGV.fetch(0, "14"))
audit(max_length).each { |key, value| puts "#{key}=#{value}" }
puts "status=independent exact normalized phase-lag audit passed"
