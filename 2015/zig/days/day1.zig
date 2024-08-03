const std = @import("std");
const utils = @import("../utilities.zig");

pub fn run(allocator: std.mem.Allocator) !void {
    const buffer = try utils.load_from_file(allocator, "./2015/inputs/day1.txt");
    defer allocator.free(buffer);

    var floor: isize = 0;
    var first_position: usize = 0;

    for (buffer, 1..) |char, position| {
        switch (char) {
            '(' => floor += 1,
            ')' => floor -= 1,
            '\r', '\n' => break,
            else => return error.UnknownCharacter,
        }
        if (floor < 0 and (first_position == 0)) {
            first_position = position;
        }
    }

    std.debug.print("Basement entered at position: {}\n", .{first_position});
    std.debug.print("Instructions end at floor: {}\n", .{floor});
}
