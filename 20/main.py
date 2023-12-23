import fileinput
from enum import Enum
from functools import reduce


class Pulse(Enum):
    LOW = 0
    HIGH = 1


class Module:
    def __init__(self, name: str):
        self.outputs: list['Module'] = []
        self.name: str = name
        self.lows = 0
        self.highs = 0

    def add_output(self, module: 'Module'):
        self.outputs.append(module)

    def add_input(self, module: 'Module'):
        pass

    def accept(self, module: 'Module', pulse: Pulse):
        if pulse == Pulse.LOW:
            self.lows += 1
        else:
            self.highs += 1


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
        global state
        super().accept(module, pulse)
        self.input_pulses[module] = pulse
        if len([i for i in self.input_pulses.values() if i == Pulse.LOW]) == 0:
            for output in self.outputs:
                queue.append((self, Pulse.LOW, output))
        else:
            for output in self.outputs:
                queue.append((self, Pulse.HIGH, output))

        # for i in self.input_pulses.values():
        #     if i == Pulse.HIGH:
        #         state += 1
        #         break


class Broadcaster(Module):
    def accept(self, module: Module, pulse: Pulse):
        super().accept(module, pulse)
        for output in self.outputs:
            queue.append((self, pulse, output))

    def add_output(self, module: 'Module'):
        super().add_output(module)


modules: dict[str, Module] = {}
outputs_by_module_name: dict[str, list[str]] = {}
with (fileinput.input(files=("input_sample"), encoding="utf-8") as f):
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


freq: dict[str, tuple[Pulse, int]] = {}
ex_queue: list[tuple[Module, Pulse, int]] = []
conj_freqs: dict[str, list[int]] = {}


def explore(m: Module, init_pulse: Pulse = Pulse.HIGH, current_freq: int = 1):
    global freq
    if isinstance(m, FlipFlop):
        current_freq = current_freq * 2
    elif isinstance(m, Conjunction):
        if m.name not in conj_freqs:
            conj_freqs[m.name] = []
        conj_freqs[m.name].append(current_freq)
        if len(conj_freqs[m.name]) < len(m.input_pulses):
            return
        current_freq = reduce(lambda x, y: x * y, set(conj_freqs[m.name]))
        init_pulse = Pulse.LOW if init_pulse == Pulse.HIGH else Pulse.HIGH
    freq[m.name] = (init_pulse, current_freq)

    for o in m.outputs:
        ex_queue.append((o, init_pulse, current_freq))


ex_queue.append((modules["broadcaster"], Pulse.LOW, 1))
while len(ex_queue) != 0:
    mod, init_pulse, c_freq = ex_queue.pop(0)
    explore(mod, init_pulse, c_freq)


high_pulses = 0
low_pulses = 0
button_presses = 0
i = 0
while True and i < 10:
    # print(i, [(m.name, p) for m, p in modules["con"].input_pulses.items()])
    # print(i, modules["output"].lows)
    # if modules["output"].lows == 1:
    #     break

    queue.append((Module('button'), Pulse.LOW, modules["broadcaster"]))
    button_presses += 1
    print(i, end=" ")
    while len(queue) != 0:
        sender, pulse, recipient = queue.pop(0)
        recipient.accept(sender, pulse)
        if pulse == Pulse.HIGH:
            print(sender.name, "hi,", end=" ")
            high_pulses += 1
        if pulse == Pulse.LOW:
            print(sender.name, "lo,", end=" ")
            low_pulses += 1

    print()
    # has_on_flip_flops = False
    # for m in modules.values():
    #     if isinstance(m, FlipFlop) and m.is_on:
    #         has_on_flip_flops = True
    #         break
    # if not has_on_flip_flops:
    #     break

    i += 1

for name, f in freq.items():
    print("{} sends LOW on {} + k * {}".format(name,
                                               0 if f[0] == Pulse.LOW else f[1] // 2 if f[1] > 1 else "never", f[1]))

# print(high_pulses, low_pulses, high_pulses * low_pulses)
# print(button_presses)