#!/usr/bin/env ruby
# Independently implemented exact checker for the adjacent-swap cocycle.

require "digest"

Cylinder = Struct.new(:length, :odd_count, :residue, :endpoint, :pow2, :pow3) do
  def extend(bit)
    raise "invalid bit" unless bit == 0 || bit == 1
    if bit == 0
      lift = endpoint & 1
      intermediate = endpoint + pow3 * lift
      raise "even compatibility" unless (intermediate & 1).zero?
      next_endpoint = intermediate / 2
      next_odd_count = odd_count
      next_pow3 = pow3
    else
      lift = (1 - endpoint) & 1
      intermediate = endpoint + pow3 * lift
      raise "odd compatibility" if (intermediate & 1).zero?
      next_endpoint = (3 * intermediate + 1) / 2
      next_odd_count = odd_count + 1
      next_pow3 = 3 * pow3
    end
    Cylinder.new(length + 1, next_odd_count, residue + pow2 * lift,
                 next_endpoint, 2 * pow2, next_pow3)
  end

  def numerator
    pow2 * endpoint - pow3 * residue
  end

  def margin
    residue - endpoint
  end
end

def inverse_mod(value, modulus)
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

def first_crossings(max_length)
  groups = Hash.new { |hash, key| hash[key] = {} }
  stack = [[0, Cylinder.new(0, 0, 0, 0, 1, 1)]]
  until stack.empty?
    bits, state = stack.pop
    next if state.length == max_length
    [0, 1].each do |bit|
      extension = state.extend(bit)
      extension_bits = bits | (bit << state.length)
      if extension.pow3 < extension.pow2
        groups[extension.length][extension_bits] = extension
      else
        stack << [extension_bits, extension]
      end
    end
  end
  groups
end

def coefficient_gap_coordinates(state)
  gap = state.pow2 - state.pow3
  raise "noncontracting" unless gap.positive?
  margin_residue = if gap == 1
                     0
                   else
                     (-state.numerator * inverse_mod(state.pow3, gap)) % gap
                   end
  window_numerator = state.pow2 * margin_residue + state.numerator
  window_denominator = state.pow2 * gap
  window_index, remainder = window_numerator.divmod(window_denominator)
  raise "window residue" unless remainder == state.residue * gap
  raise "window margin" unless state.margin == margin_residue - gap * window_index
  [gap, margin_residue, window_index]
end

def audit(max_length)
  groups = first_crossings(max_length)
  digest = Digest::SHA256.new
  cylinders = groups.values.sum(&:length)
  edges = 0
  wrapped = 0
  unwrapped = 0
  minimum_jump = nil
  maximum_jump = 0
  maximum_window_index = 0
  wrap_defect_failures = 0

  groups.keys.sort.each do |length|
    states = groups[length]
    modulus = 1 << length
    gap_coordinates = states.transform_values do |state|
      coefficient_gap_coordinates(state)
    end
    maximum_window_index = [maximum_window_index,
                            gap_coordinates.values.map(&:last).max].max
    states.keys.sort.each do |bits|
      source = states.fetch(bits)
      (0...(length - 1)).each do |position|
        next unless ((bits >> position) & 3) == 2
        target = states.fetch(bits ^ (3 << position))
        prefix_ones = popcount(bits & ((1 << position) - 1))
        suffix_ones = popcount(bits >> (position + 2))
        local_modulus = 1 << (length - position)
        inverse = inverse_mod(3**(prefix_ones + 1), local_modulus)
        complement = local_modulus - inverse
        gap = modulus - source.pow3
        suffix_power = 3**suffix_ones
        numerator_delta = (1 << position) * suffix_power
        residue_delta = (1 << position) * inverse
        raise "numerator" unless source.numerator - target.numerator == numerator_delta
        raise "residue" unless target.residue == (source.residue + residue_delta) % modulus

        jump_numerator = gap * inverse + suffix_power
        raise "integrality" unless (jump_numerator % local_modulus).zero?
        positive_jump = jump_numerator / local_modulus
        wrapped_here = source.residue + residue_delta >= modulus
        expected = positive_jump - (wrapped_here ? gap : 0)
        raise "cocycle" unless target.margin - source.margin == expected
        _, margin_residue, window_index = gap_coordinates.fetch(bits)
        _, target_margin_residue, target_window_index =
          gap_coordinates.fetch(bits ^ (3 << position))
        circle_wrap = margin_residue + positive_jump >= gap
        unless target_margin_residue == (margin_residue + positive_jump) % gap
          raise "coefficient-gap rotation"
        end
        unless target_window_index - window_index ==
               (wrapped_here ? 1 : 0) - (circle_wrap ? 1 : 0)
          wrap_defect_failures += 1
        end
        negative_numerator = gap * complement - suffix_power
        raise "negative integrality" unless (negative_numerator % local_modulus).zero?
        negative_jump = negative_numerator / local_modulus
        raise "complement" unless positive_jump + negative_jump == gap
        raise "bounds" unless positive_jump.positive? && negative_jump.positive?

        wrapped_here ? wrapped += 1 : unwrapped += 1
        edges += 1
        minimum_jump = [minimum_jump || positive_jump, positive_jump, negative_jump].min
        maximum_jump = [maximum_jump, positive_jump, negative_jump].max
        digest << format("%d,%x,%d,%d,%d,%d,%d,%d,%d,%d\n",
                         length, bits, position, source.residue, source.endpoint,
                         target.residue, target.endpoint, positive_jump,
                         negative_jump, wrapped_here ? 1 : 0)
      end
    end
  end
  {
    max_length: max_length,
    first_crossing_cylinders: cylinders,
    adjacent_edges: edges,
    unwrapped_edges: unwrapped,
    wrapped_edges: wrapped,
    minimum_jump: minimum_jump || 0,
    maximum_jump: maximum_jump,
    maximum_window_index: maximum_window_index,
    wrap_defect_failures: wrap_defect_failures,
    sha256: digest.hexdigest
  }
end

max_length = Integer(ARGV.fetch(0, "20"))
audit(max_length).each { |key, value| puts "#{key}=#{value}" }
puts "status=independent exact adjacent-swap cocycle audit passed"
