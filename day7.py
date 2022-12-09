class FileSystem:
    def __init__(self):
        self.cd = ["/"]
        self.dir = {"/": {}}
        self.dir_sizes = {}

        self.is_list = False

    def parse(self, line):
        words = line.split(" ")

        if words[0] == "$":
            self._command(words[1], *words[2:])
        elif self.is_list:
            current_dir = self._current_dir()
            size = {} if words[0] == "dir" else words[0]
            current_dir[words[1]] = size

    def get_sum_of_sizes_under(self, amount):
        self._size()

        return sum(filter(lambda dir: dir <= amount, self.dir_sizes.values()))

    def smallest_sufficent_directory(self, total_disk, needed_space):
        free_space = total_disk - self.dir_sizes[""]
        deficit = needed_space - free_space

        sufficient_dirs = {
            directory: size
            for directory, size in self.dir_sizes.items()
            if size > deficit
        }

        return min(sufficient_dirs.values())

    def _command(self, command, *args):
        if command == "ls":
            self.is_list = True
            return

        self.is_list = False
        if command == "cd":
            if args[0] == "/":
                self.cd = ["/"]
            elif args[0] == "..":
                if len(self.cd) > 1:
                    self.cd.pop()
            else:
                current_dir = self._current_dir()

                if args[0] not in current_dir:
                    current_dir[args[0]] = {}

                self.cd.append(args[0])

    def _current_dir(self):
        dir_dict = self.dir
        for directory in self.cd:
            dir_dict = dir_dict[directory]

        return dir_dict

    def _size(self, directory="/"):
        self.parse(f"$ cd {directory}")

        total_size = 0
        for name, size in self._current_dir().items():
            if isinstance(size, dict):
                total_size += self._size(name)
            else:
                total_size += int(size)

        self.dir_sizes["/".join(self.cd[1:])] = total_size

        self.parse("$ cd ..")
        return total_size


fs = FileSystem()

with open("input/day7.txt", "r", encoding="utf-8") as file:
    for line in file:
        fs.parse(line.strip())

print(fs.get_sum_of_sizes_under(100000))
print(fs.smallest_sufficent_directory(70000000, 30000000))
