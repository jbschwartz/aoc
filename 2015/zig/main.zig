const std = @import("std");
const runners = @import("runners.zig").runners;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    defer _ = gpa.deinit();

    const day = blk: {
        var args = std.process.argsWithAllocator(allocator) catch {
            return;
        };
        defer args.deinit();

        _ = args.skip();

        const path = args.next() orelse {
            std.debug.print("Usage: app <day>\n", .{});
            return;
        };

        break :blk try std.fmt.parseInt(u8, path, 10);
    };

    std.debug.print("Running day {}:\n\n", .{day});

    const runner = runners[day - 1];

    try runner(allocator);
}
