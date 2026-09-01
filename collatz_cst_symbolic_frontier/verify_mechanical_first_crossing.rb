# frozen_string_literal: true

# Independent exact audit of cap-maximizing mechanical first-crossing cylinders.

require 'digest'

LOW_MASK = (1 << 256) - 1

State = Struct.new(:length, :odd_count, :residue, :endpoint, :pow2, :pow3)

def extend_state(state, bit)
  raise 'invalid parity bit' unless [0, 1].include?(bit)

  if bit.zero?
    lift = state.endpoint & 1
    intermediate = state.endpoint + state.pow3 * lift
    raise 'even compatibility failed' unless (intermediate & 1).zero?

    endpoint = intermediate / 2
    odd_count = state.odd_count
    pow3 = state.pow3
  else
    lift = (1 - state.endpoint) & 1
    intermediate = state.endpoint + state.pow3 * lift
    raise 'odd compatibility failed' if (intermediate & 1).zero?

    endpoint = (3 * intermediate + 1) / 2
    odd_count = state.odd_count + 1
    pow3 = 3 * state.pow3
  end
  State.new(
    state.length + 1,
    odd_count,
    state.residue + state.pow2 * lift,
    endpoint,
    2 * state.pow2,
    pow3
  )
end

def digest_record(state)
  difference = state.residue - state.endpoint
  format(
    "%d,%d,%d,%d,%064x,%064x,%064x\n",
    state.length,
    state.odd_count,
    state.residue.bit_length,
    state.endpoint.bit_length,
    state.residue & LOW_MASK,
    state.endpoint & LOW_MASK,
    difference & LOW_MASK
  )
end

max_length = Integer(ARGV.fetch(0, '100000'))
raise 'max_length must be positive' unless max_length.positive?

state = State.new(0, 0, 0, 0, 1, 1)
digest = Digest::SHA256.new
cases = 0
nontrivial_cases = 0
equalities = 0
failures = 0
last_length = 0
last_odd_count = 0

(1..max_length).each do |_crossing_length|
  if state.pow3 < 2 * state.pow2
    crossing = extend_state(state, 0)
    cases += 1
    last_length = crossing.length
    last_odd_count = crossing.odd_count
    if crossing.odd_count >= 2
      nontrivial_cases += 1
      failures += 1 if crossing.residue <= crossing.endpoint
    elsif crossing.residue == crossing.endpoint
      equalities += 1
    end
    digest.update(digest_record(crossing))
  end

  next_bit = state.pow3 < 2 * state.pow2 ? 1 : 0
  state = extend_state(state, next_bit)
end

puts "max_length=#{max_length}"
puts "first_crossing_cases=#{cases}"
puts "nontrivial_cases=#{nontrivial_cases}"
puts "trivial_equalities=#{equalities}"
puts "nontrivial_failures=#{failures}"
puts "last_crossing_length=#{last_length}"
puts "last_crossing_odd_count=#{last_odd_count}"
puts "full_sha256=#{digest.hexdigest}"
puts 'status=exact mechanical first-crossing audit passed'
