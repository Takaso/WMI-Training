import random; import toga; from toga.style import Pack; from toga.style.pack import COLUMN, ROW;
letters = list("abcdefghijklmnopqrstuvwxyz".upper());
class WMITraining(toga.App):
    def startup(self):
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=10));
        self.main_window = toga.MainWindow(title=self.formal_name);
        self.main_window.content = self.main_box;
        self.main_window.show(); self.menu();
    def menu(self):
        self.n_back_label = toga.Label("Enter N-Back:", style=Pack(padding=(5, 0)));
        self.n_back_input = toga.TextInput(style=Pack(flex=1));
        self.loops_label = toga.Label("Enter Number of Loops:", style=Pack(padding=(5, 0)));
        self.loops_input = toga.TextInput(style=Pack(flex=1));
        self.start_button = toga.Button("Start Training", on_press=self.start_training, style=Pack(padding=(10, 0)));
        self.main_box.add(self.n_back_label);
        self.main_box.add(self.n_back_input);
        self.main_box.add(self.loops_label);
        self.main_box.add(self.loops_input);
        self.main_box.add(self.start_button);
    def start_training(self, widget):
        try:
            self.n_back = int(self.n_back_input.value);
            self.loops = int(self.loops_input.value);
            if self.n_back <= 0 or self.loops <= self.n_back:
                raise ValueError("Invalid values, qwq");
            self.correct = 0;
            self.history = [];
            self.current_index = 0;
            self.initial_items = [];
            for _ in range(self.n_back):
                item = [random.choice(letters), random.randint(0, 15)];
                self.history.append(item); self.initial_items.append(f"{item[0]} {item[1]}");
            self.main_box.remove(*self.main_box.children);
            self.initial_label = toga.Label("Initial N-Back Items:", style=Pack(font_size=18, padding=(10, 0)));
            self.initial_items_label = toga.Label("\n".join(self.initial_items), style=Pack(font_size=16, padding=(10, 0), font_family="Comic Sans MS"));
            self.start_test_button = toga.Button("Start recalling", on_press=self.start_test, style=Pack(padding=(10, 0)));
            self.main_box.add(self.initial_label);
            self.main_box.add(self.initial_items_label);
            self.main_box.add(self.start_test_button);
        except ValueError:
            self.n_back_input.value = ""; self.loops_input.value = "";
            self.n_back_input.placeholder = "Enter a valid number, bozo"; self.loops_input.placeholder = "Enter a valid number, bozo x2";
    def start_test(self, widget):
        self.main_box.remove(*self.main_box.children);
        self.current_stimulus_label = toga.Label("", style=Pack(font_size=24, padding=(10, 0), font_family="Comic Sans MS"));
        self.main_box.add(self.current_stimulus_label);
        self.button_box = toga.Box(style=Pack(direction=ROW, padding=10));
        self.yes_button = toga.Button("Yes", on_press=self.record_yes, style=Pack(flex=1, padding=(0, 5)));
        self.no_button = toga.Button("No", on_press=self.record_no, style=Pack(flex=1, padding=(0, 5)));
        self.button_box.add(self.yes_button); self.button_box.add(self.no_button);
        self.main_box.add(self.button_box); self.next_stimulus();
    def next_stimulus(self):
        if self.current_index < self.loops - self.n_back:
            if random.choice([True, False]):
                self.current_stimulus = self.history[self.current_index];
            else:
                self.current_stimulus = [random.choice(letters), random.randint(0, 15)];
            self.current_stimulus_label.text = f"{self.current_stimulus[0]} {self.current_stimulus[1]}";
            self.history.append(self.current_stimulus); self.current_index += 1;
        else:
            self.show_results();
    def record_yes(self, widget):
        if self.current_stimulus == self.history[self.current_index - self.n_back - 1]:
            self.correct += 1;
        self.next_stimulus();
    def record_no(self, widget):
        if self.current_stimulus != self.history[self.current_index - self.n_back - 1]:
            self.correct += 1;
        self.next_stimulus();
    def show_results(self):
        self.main_box.remove(*self.main_box.children)
        accuracy = self.correct/(self.loops-self.n_back)*100;
        result_label = toga.Label(f"Results:\nKukuku.. correct Responses: {self.correct}/{self.loops - self.n_back}\nAccuracy: {accuracy:.2f}%", style=Pack(font_size=18, padding=(10, 0));
        restart_button = toga.Button("Restart", on_press=self.restart, style=Pack(padding=(10, 0)));
        self.main_box.add(result_label); self.main_box.add(restart_button);
    def restart(self, widget):
        self.main_box.remove(*self.main_box.children); self.menu();
def main():
    return WMITraining();
