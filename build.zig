const std = @import("std");

const ResolvedTarget = std.Build.ResolvedTarget;
const OptimizeMode = std.builtin.OptimizeMode;

fn executable(b: *std.Build) !void {
    const year: u16 = b.option(u16, "year", "The year to compile") orelse {
        std.debug.print("Missing required option: -Dyear=[int]\n", .{});
        return;
    };

    var buffer: [32]u8 = undefined;

    const path = try std.fmt.bufPrint(&buffer, "{}/zig/main.zig", .{year});

    const exe = b.addExecutable(.{
        .name = "aoc",
        .target = b.standardTargetOptions(.{}),
        .root_source_file = b.path(path),
    });

    b.installArtifact(exe);

    const run = b.addRunArtifact(exe);

    run.step.dependOn(b.getInstallStep());

    if (b.args) |args| {
        run.addArgs(args);
    }

    const run_command = b.step("run", "Run");
    run_command.dependOn(&run.step);
}

pub fn build(b: *std.Build) !void {
    try executable(b);
}
