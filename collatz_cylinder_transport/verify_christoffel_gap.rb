# Independent exact checker for the finite Christoffel realizability-gap screen.

def extended_gcd(a, b)
  return [a, 1, 0] if b.zero?

  gcd, x1, y1 = extended_gcd(b, a % b)
  [gcd, y1, x1 - (a / b) * y1]
end

def modular_inverse(a, modulus)
  gcd, x, = extended_gcd(a, modulus)
  raise 'inverse does not exist' unless gcd == 1

  x % modulus
end


def numerator_by_positions(length, weight)
  (0...weight).sum do |index|
    position = (index * length) / weight
    (2**position) * (3**(weight - 1 - index))
  end
end


max_length = Integer(ARGV.fetch(0, '300'))
pairs_checked = 0

(2..max_length).each do |length|
  ((length / 2 + 1)..length).each do |weight|
    next unless 3**weight < 2**length

    pairs_checked += 1
    numerator = numerator_by_positions(length, weight)
    modulus = 2**length
    denominator = modulus - 3**weight
    inverse = modular_inverse(3**weight, modulus)
    residue = (-numerator * inverse) % modulus
    positive_residue = residue.zero? ? modulus : residue
    unless positive_residue * denominator > numerator
      raise "gap counterexample at (#{length}, #{weight})"
    end
  end
end

puts "christoffel_max_length=#{max_length}"
puts "christoffel_high_density_pairs_checked=#{pairs_checked}"
puts 'christoffel_gap_counterexamples=0'
puts 'status=all independent exact checks passed'
