const std = @import("std");
const utils = @import("../utilities.zig");

const Package = struct {
    length: u16,
    width: u16,
    height: u16,

    pub fn surface_area(self: Package) u32 {
        const lw = self.length * self.width;
        const wh = self.width * self.height;
        const hl = self.height * self.length;

        return 2 * lw + 2 * wh + 2 * hl;
    }

    pub fn smallest_side_area(self: Package) u32 {
        return @min(
            self.length * self.width,
            self.width * self.height,
            self.height * self.length,
        );
    }

    pub fn smallest_perimeter(self: Package) u32 {
        return @min(
            2 * (self.length + self.width),
            2 * (self.width + self.height),
            2 * (self.height + self.length),
        );
    }

    pub fn volume(self: Package) u32 {
        return self.length * self.width * self.height;
    }
};

pub fn run(allocator: std.mem.Allocator) !void {
    const buffer = try utils.load_from_file(allocator, "./2015/inputs/day2.txt");
    defer allocator.free(buffer);

    var line_iterator = std.mem.splitScalar(u8, buffer, '\n');
    var total_paper: u32 = 0;
    var total_ribbon: u32 = 0;

    while (line_iterator.next()) |line| {
        if (line.len == 0) continue;

        // Remove the carriage return character.
        const end_index = if (line[line.len - 1] == '\r') line.len - 1 else line.len;

        var dim_iterator = std.mem.splitScalar(u8, line[0..end_index], 'x');

        var dimensions: [3]u8 = undefined;
        var index: u8 = 0;

        while (dim_iterator.next()) |dim_string| : (index += 1) {
            std.debug.assert(index < 3);

            dimensions[index] = try std.fmt.parseInt(u8, dim_string, 10);
        }

        const package = Package{
            .length = dimensions[0],
            .width = dimensions[1],
            .height = dimensions[2],
        };

        const paper = package.surface_area() + package.smallest_side_area();
        const ribbon = package.smallest_perimeter() + package.volume();

        total_paper += paper;
        total_ribbon += ribbon;
    }

    std.debug.print("Paper required: {d}\n", .{total_paper});
    std.debug.print("Ribbon required: {d}\n", .{total_ribbon});
}
