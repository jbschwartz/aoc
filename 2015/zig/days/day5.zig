const std = @import("std");
const utils = @import("../utilities.zig");

const is_part_two = true;

fn part_one(line: []const u8, _: std.mem.Allocator) !bool {
    var vowel_count: usize = 0;
    var has_double_letter: bool = false;
    var has_bad_string: bool = false;

    var last_character: u8 = 0;

    for (line) |character| {
        switch (character) {
            'a', 'e', 'i', 'o', 'u' => vowel_count += 1,
            'b', 'd', 'q', 'y' => {
                has_bad_string = last_character == (character - 1);
                if (has_bad_string) break;
            },
            else => {},
        }

        if (character == last_character) {
            has_double_letter = true;
        }

        last_character = character;
    }

    return (vowel_count >= 3 and has_double_letter and !has_bad_string);
}

fn part_two(line: []const u8, allocator: std.mem.Allocator) !bool {
    var visits = std.AutoHashMap(u16, bool).init(allocator);
    defer visits.deinit();

    var last_pair: u16 = 0;

    var has_straddle: bool = false;
    var has_repeating_pair: bool = false;

    for (2..line.len + 1) |index| {
        const pair: u16 = std.mem.readInt(u16, @ptrCast(&line[index - 2]), .big);

        if (pair != last_pair) {
            if (visits.contains(pair)) {
                has_repeating_pair = true;
            } else {
                try visits.put(pair, true);
            }
            last_pair = pair;
        } else {
            // Reset the last pair so that two pairs in a row (four of the same character) in a
            // row is valid.
            last_pair = 0;
        }

        if (index == line.len) break;

        if (line[index - 2] == line[index]) {
            has_straddle = true;
        }
    }

    return has_straddle and has_repeating_pair;
}

pub fn run(allocator: std.mem.Allocator) !void {
    const buffer = try utils.load_from_file(allocator, "./2015/inputs/day5.txt");
    defer allocator.free(buffer);

    var line_iterator = std.mem.splitScalar(u8, buffer, '\n');

    var nice_count: usize = 0;

    const part = if (is_part_two) &part_two else &part_one;

    while (line_iterator.next()) |line| {
        if (line.len == 0) continue;

        if (try part(line, allocator)) nice_count += 1;
    }

    std.debug.print("Nice count: {d}\n", .{nice_count});
}
