const std = @import("std");

fn placeholder(_: std.mem.Allocator) anyerror!void {
    return;
}

pub const runners = [_]*const fn (allocator: std.mem.Allocator) anyerror!void{
    &@import("days/day1.zig").run,
    &@import("days/day2.zig").run,
    &@import("days/day3.zig").run,
    &placeholder,
    &@import("days/day5.zig").run,
};
