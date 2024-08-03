const std = @import("std");
const utils = @import("../utilities.zig");

const is_part_two = false;

const Position = struct {
    x: i32 = 0,
    y: i32 = 0,
};

pub fn run(allocator: std.mem.Allocator) !void {
    const buffer = try utils.load_from_file(allocator, "./2015/inputs/day3.txt");
    defer allocator.free(buffer);

    var visits = std.AutoHashMap(Position, u32).init(allocator);
    defer visits.deinit();

    var positions = [_]Position{ .{}, .{} };
    var index: usize = 0;

    for (buffer) |char| {
        for (positions) |position| {
            if (visits.get(position)) |num_visits| {
                try visits.put(position, num_visits + 1);
            } else {
                try visits.put(position, 1);
            }
        }

        switch (char) {
            '^' => positions[index].y += 1,
            'v' => positions[index].y -= 1,
            '<' => positions[index].x -= 1,
            '>' => positions[index].x += 1,
            '\r', '\n' => break,
            else => return error.UnknownCharacter,
        }

        if (is_part_two) {
            index = (index + 1) % 2;
        }
    }

    const num_houses_visited = visits.count();

    std.debug.print("Number of houses visited: {}\n", .{num_houses_visited});
}
