#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent owner-map audit for the [7] x [7] x [2] cross-boundary core.
#
# This is the exact Ruby audit recovered from the 2026-09-05 research session,
# curated as a reproducible source file.  It constructs cell owners directly
# from the displayed coordinate rule rather than importing or translating the
# Python part constructor.  It checks the finite base certificate and 250,000
# instances of the two part-count identities.  It does not prove the universal
# stripping, lifting, or Hamming upper-bound arguments.
#
# Ruby 2.6 or later; standard library only.

require "digest"
require "json"

owners = Hash.new { |hash, key| hash[key] = [] }

2.times do |z|
  7.times do |y|
    7.times do |x|
      owner = if y == 0 && x < 4
                [:nonlinear]
              elsif y >= 3 ||
                    (y == 0 && x >= 4) ||
                    (y == 1 && x < 2) ||
                    (y == 2 && (2..3).include?(x))
                [:column, x, z]
              elsif y == 1
                [:row1, z]
              else
                [:row2, z]
              end
      owners[owner] << [x, y, z]
    end
  end
end

raise "owner count" unless owners.size == 19
raise "coverage" unless owners.values.flatten(1).uniq.size == 98

owners.each do |name, cells|
  expected_size = name[0] == :nonlinear ? 8 : 5
  raise "size" unless cells.size == expected_size

  cells.each do |vertex|
    degree = cells.count do |other|
      vertex.zip(other).count { |left, right| left != right } == 1
    end
    raise "degree" unless degree >= 4
  end
end

canonical = owners.values.map(&:sort).sort
puts "ruby owner classes: #{owners.size}"
puts "ruby covered cells: #{owners.values.sum(&:size)}"
puts "ruby base certificate SHA-256: #{Digest::SHA256.hexdigest(JSON.generate(canonical))}"

(1..500).each do |a|
  (1..500).each do |b|
    quotient = 10 * a * b + 4 * a + 4 * b + 1
    raise "quotient" unless quotient == 2 * (5 * a + 2) * (5 * b + 2) / 5
    raise "line gap" unless quotient - 1 == 2 * ((5 * a + 2) * (5 * b + 2) / 5)
  end
end

puts "ruby formula instances: 250000"
