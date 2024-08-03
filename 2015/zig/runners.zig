const std = @import("std");

pub const runners = [_]*const fn (allocator: std.mem.Allocator) anyerror!void{
    &@import("days/day1.zig").run,
    &@import("days/day2.zig").run,
    &@import("days/day3.zig").run,
};
