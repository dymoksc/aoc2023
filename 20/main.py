import fileinput
from enum import Enum


class Pulse(Enum):
    LOW = 0
    HIGH = 1


class Module:
    def __init__(self, name: str):
        self.outputs: list['Module'] = []
        self.name: str = name

    def add_output(self, module: 'Module'):
        self.outputs.append(module)

    def add_input(self, module: 'Module'):
        pass

    def accept(self, module: 'Module', pulse: Pulse):
        pass


queue: list[tuple[Module, Pulse, Module]] = []


class FlipFlop(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.is_on: bool = False

    def accept(self, module: Module, pulse: Pulse):
        super().accept(module, pulse)
        if pulse == Pulse.HIGH:
            return
        for output in self.outputs:
            queue.append((self, Pulse.LOW if self.is_on else Pulse.HIGH, output))
        self.is_on = not self.is_on


class Conjunction(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.input_pulses: dict[Module, Pulse] = {}

    def add_input(self, module: Module):
        super().add_input(module)
        self.input_pulses[module] = Pulse.LOW

    def accept(self, module: Module, pulse: Pulse):
        super().accept(module, pulse)
        self.input_pulses[module] = pulse
        if len([i for i in self.input_pulses.values() if i == Pulse.LOW]) == 0:
            for output in self.outputs:
                queue.append((self, Pulse.LOW, output))
        else:
            for output in self.outputs:
                queue.append((self, Pulse.HIGH, output))


class Broadcaster(Module):
    def accept(self, module: Module, pulse: Pulse):
        super().accept(module, pulse)
        for output in self.outputs:
            queue.append((self, pulse, output))

    def add_output(self, module: 'Module'):
        super().add_output(module)


modules: dict[str, Module] = {}
outputs_by_module_name: dict[str, list[str]] = {}
with (fileinput.input(files=("input"), encoding="utf-8") as f):
    for line in f:
        type_name, cs_outputs = line.rstrip('\n').split(' -> ')
        m: Module
        if type_name[0] == '%':
            name = type_name[1:]
            m = FlipFlop(name)
        elif type_name[0] == '&':
            name = type_name[1:]
            m = Conjunction(name)
        elif type_name == 'broadcaster':
            name = type_name
            m = Broadcaster(name)
        else:
            name = type_name
            m = Module(name)

        modules[name] = m
        outputs_by_module_name[name] = cs_outputs.split(', ')

current_module_names = list(modules.keys())
for name in current_module_names:
    for output_name in outputs_by_module_name[name]:
        if output_name not in modules:
            modules[output_name] = Module(output_name)
        modules[name].add_output(modules[output_name])
        modules[output_name].add_input(modules[name])

high_pulses = 0
low_pulses = 0
for i in range(1000):
    queue.append((Module('button'), Pulse.LOW, modules["broadcaster"]))
    while len(queue) != 0:
        sender, pulse, recipient = queue.pop(0)
        # print("{} -{}-> {}".format(sender.name, "high" if pulse == Pulse.HIGH else "low", recipient.name))
        recipient.accept(sender, pulse)
        if pulse == Pulse.HIGH:
            high_pulses += 1
        if pulse == Pulse.LOW:
            low_pulses += 1
    # print()

print(high_pulses, low_pulses, high_pulses * low_pulses)
