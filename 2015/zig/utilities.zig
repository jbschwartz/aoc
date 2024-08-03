const std = @import("std");

pub fn load_from_file(allocator: std.mem.Allocator, path: []const u8) ![]const u8 {
    const file = try std.fs.cwd().openFile(path, .{});

    const buffer = try file.readToEndAlloc(allocator, std.math.pow(u32, 2, 20));
    errdefer allocator.free(buffer);

    return buffer;
}
