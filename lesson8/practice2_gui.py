import random
import tkinter as tk


# ── 色彩主題 ──────────────────────────────────────────
BG          = "#2b2d42"
CARD_BG     = "#3d3f5c"
INPUT_BG    = "#4a4c6a"
TEXT_WHITE   = "#edf2f4"
TEXT_DIM     = "#8d99ae"
ACCENT_GUESS = "#8d99ae"
HOVER_GUESS  = "#ef233c"
ACCENT_RESET = "#06d6a0"
HOVER_RESET  = "#1b9aaa"
HINT_TOO_LOW = "#ff9f1c"
HINT_TOO_HIGH = "#ef233c"
HINT_CORRECT = "#06d6a0"
HINT_ERROR   = "#ef233c"
HIST_LOW     = "#ff9f1c"
HIST_HIGH    = "#ef233c"
HIST_CORRECT = "#06d6a0"
RANGE_BAR_BG = "#1a1b2e"
RANGE_BAR_FG = "#5e6ad2"
RANGE_MARKER = "#ef233c"
FONT_FAMILY  = "Microsoft JhengHei"


class GuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("猜數字遊戲（範圍縮小版）")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.placeholder_active = False
        self.history = []
        self.reset_game()
        self.build_ui()
        self.center_window(480, 540)
        self.draw_range_bar()

    # ── 視窗置中 ──────────────────────────────────────
    def center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # ── 遊戲狀態 ──────────────────────────────────────
    def reset_game(self):
        self.target = random.randint(1, 100)
        self.low = 1
        self.high = 100
        self.attempts = 0
        self.history = []

    # ── 建立 UI ───────────────────────────────────────
    def build_ui(self):
        # ── 標題區 ────────────────────────────────────
        self.title_label = tk.Label(
            self.root, text="🎯 猜數字遊戲", bg=BG,
            fg=TEXT_WHITE, font=(FONT_FAMILY, 24, "bold"),
        )
        self.title_label.pack(pady=(20, 2))

        tk.Label(
            self.root, text="範圍縮小版 — 請猜 1 ~ 100 之間的數字", bg=BG,
            fg=TEXT_DIM, font=(FONT_FAMILY, 10),
        ).pack()

        # ── 漸層裝飾線 ────────────────────────────────
        line = tk.Canvas(self.root, height=3, bg=BG, highlightthickness=0)
        line.pack(padx=50, pady=(8, 0), fill="x")
        self._draw_gradient_line(line, ACCENT_GUESS, HOVER_GUESS)

        # ── 資訊卡片 ──────────────────────────────────
        card_outer = tk.Frame(self.root, bg=CARD_BG, bd=0)
        card_outer.pack(padx=30, pady=(14, 0), fill="x")

        card = tk.Frame(card_outer, bg=CARD_BG, bd=0)
        card.pack(padx=2, pady=2, fill="x")

        self.range_var = tk.StringVar(value=f"目前範圍：{self.low} ~ {self.high}")
        tk.Label(
            card, textvariable=self.range_var, bg=CARD_BG,
            fg=TEXT_WHITE, font=(FONT_FAMILY, 15, "bold"),
        ).pack(pady=(12, 2))

        self.attempts_var = tk.StringVar(value=f"猜測次數：{self.attempts}")
        tk.Label(
            card, textvariable=self.attempts_var, bg=CARD_BG,
            fg=TEXT_DIM, font=(FONT_FAMILY, 11),
        ).pack(pady=(0, 6))

        # ── 猜測歷史 ──────────────────────────────────
        self.history_frame = tk.Frame(card, bg=CARD_BG)
        self.history_frame.pack(pady=(0, 10))
        self.history_label = tk.Label(
            self.history_frame, text="", bg=CARD_BG,
            fg=TEXT_DIM, font=(FONT_FAMILY, 10),
        )
        self.history_label.pack()

        # ── 視覺化範圍條 ──────────────────────────────
        bar_frame = tk.Frame(self.root, bg=BG)
        bar_frame.pack(padx=30, pady=(10, 0), fill="x")
        self.range_canvas = tk.Canvas(
            bar_frame, height=28, bg=RANGE_BAR_BG,
            highlightthickness=0, bd=0,
        )
        self.range_canvas.pack(fill="x")
        self.range_canvas.bind("<Configure>", lambda e: self.draw_range_bar())

        # ── 輸入區 ────────────────────────────────────
        input_frame = tk.Frame(self.root, bg=BG)
        input_frame.pack(pady=18)

        self.entry = tk.Entry(
            input_frame, font=(FONT_FAMILY, 16), width=10,
            justify="center", bg=INPUT_BG, fg=TEXT_WHITE,
            insertbackground=TEXT_WHITE, bd=0,
            highlightthickness=2, highlightbackground=CARD_BG,
            highlightcolor=ACCENT_GUESS,
        )
        self.entry.pack(side=tk.LEFT, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self.make_guess())
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        self._show_placeholder()

        self.guess_btn = tk.Button(
            input_frame, text="猜測", font=(FONT_FAMILY, 13, "bold"),
            bg=ACCENT_GUESS, fg=TEXT_WHITE, activebackground=HOVER_GUESS,
            activeforeground=TEXT_WHITE, bd=0, padx=20, pady=7,
            cursor="hand2", command=self.make_guess,
        )
        self.guess_btn.pack(side=tk.LEFT)
        self.guess_btn.bind("<Enter>", lambda e: self.guess_btn.config(bg=HOVER_GUESS))
        self.guess_btn.bind("<Leave>", lambda e: self.guess_btn.config(bg=ACCENT_GUESS))

        # ── 提示訊息 ──────────────────────────────────
        self.hint_var = tk.StringVar(value="")
        self.hint_label = tk.Label(
            self.root, textvariable=self.hint_var, bg=BG,
            fg=TEXT_WHITE, font=(FONT_FAMILY, 13, "bold"),
        )
        self.hint_label.pack(pady=(0, 5))

        # ── 重新開始 ──────────────────────────────────
        self.reset_btn = tk.Button(
            self.root, text="重新開始", font=(FONT_FAMILY, 11),
            bg=ACCENT_RESET, fg=BG, activebackground=HOVER_RESET,
            activeforeground=TEXT_WHITE, bd=0, padx=16, pady=5,
            cursor="hand2", command=self.restart,
        )
        self.reset_btn.pack(pady=(5, 18))
        self.reset_btn.bind("<Enter>", lambda e: self.reset_btn.config(bg=HOVER_RESET))
        self.reset_btn.bind("<Leave>", lambda e: self.reset_btn.config(bg=ACCENT_RESET))

    # ── 漸層裝飾線 ───────────────────────────────────
    def _draw_gradient_line(self, canvas, color1, color2):
        canvas.update_idletasks()
        w = canvas.winfo_width()
        if w <= 1:
            return
        r1, g1, b1 = self.root.winfo_rgb(color1)
        r2, g2, b2 = self.root.winfo_rgb(color2)
        steps = max(w, 1)
        for i in range(steps):
            r = int(r1 + (r2 - r1) * i / steps) >> 8
            g = int(g1 + (g2 - g1) * i / steps) >> 8
            b = int(b1 + (b2 - b1) * i / steps) >> 8
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(i, 0, i + 1, 3, fill=hex_color)

    # ── 視覺化範圍條 ─────────────────────────────────
    def draw_range_bar(self, *_):
        c = self.range_canvas
        c.delete("all")
        w = c.winfo_width()
        h = c.winfo_height()
        if w <= 1:
            return

        pad = 8
        bar_w = w - pad * 2
        bar_h = 12
        y = (h - bar_h) // 2

        # 底條
        c.create_rectangle(pad, y, pad + bar_w, y + bar_h,
                           fill=RANGE_BAR_BG, outline="", width=0)

        # 有效範圍高亮
        lx = pad + bar_w * (self.low - 1) / 99
        rx = pad + bar_w * (self.high - 1) / 99
        c.create_rectangle(lx, y, rx, y + bar_h,
                           fill=RANGE_BAR_FG, outline="", width=0)

        # 左右標籤
        c.create_text(pad, y + bar_h + 14, text=str(self.low),
                      fill=TEXT_DIM, font=(FONT_FAMILY, 8), anchor="w")
        c.create_text(pad + bar_w, y + bar_h + 14, text=str(self.high),
                      fill=TEXT_DIM, font=(FONT_FAMILY, 8), anchor="e")

        # 刻度線
        for v in [1, 25, 50, 75, 100]:
            x = pad + bar_w * (v - 1) / 99
            c.create_line(x, y + bar_h + 1, x, y + bar_h + 5,
                          fill=TEXT_DIM, width=1)

    # ── 更新歷史顯示 ─────────────────────────────────
    def _update_history(self):
        if not self.history:
            self.history_label.config(text="")
            return
        parts = []
        for val, direction in self.history[-5:]:
            if direction == "low":
                parts.append(f"{val}↓")
            elif direction == "high":
                parts.append(f"{val}↑")
            else:
                parts.append(f"{val}✓")
        text = "    ".join(parts)
        self.history_label.config(text=f"歷史：{text}")

    # ── Placeholder ──────────────────────────────────
    def _show_placeholder(self):
        if not self.entry.get():
            self.placeholder_active = True
            self.entry.config(fg=TEXT_DIM)
            self.entry.insert(0, "請輸入數字")

    def _on_focus_in(self, _):
        if self.placeholder_active:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=TEXT_WHITE)
            self.placeholder_active = False

    def _on_focus_out(self, _):
        if self.entry["state"] == tk.DISABLED:
            return
        if not self.entry.get():
            self._show_placeholder()

    # ── 提示顏色 ─────────────────────────────────────
    def _set_hint(self, text, color):
        self.hint_var.set(text)
        self.hint_label.config(fg=color)

    # ── 猜中動畫 ─────────────────────────────────────
    def _win_animation(self):
        self._anim_step = 0
        self._anim_title_size = 24
        self._animate_title()

    def _animate_title(self):
        if self._anim_step < 10:
            self._anim_title_size += 2
            self._anim_step += 1
        elif self._anim_step < 20:
            self._anim_title_size -= 2
            self._anim_step += 1
        else:
            self.title_label.config(font=(FONT_FAMILY, 24, "bold"))
            return
        self.title_label.config(font=(FONT_FAMILY, self._anim_title_size, "bold"))
        self.root.after(40, self._animate_title)

    def _flash_green(self):
        self._flash_count = 0
        self._flash_bg = BG
        self._do_flash()

    def _do_flash(self):
        if self._flash_count >= 6:
            self.root.configure(bg=BG)
            return
        color = "#1a4a2e" if self._flash_count % 2 == 0 else BG
        self.root.configure(bg=color)
        self._flash_count += 1
        self.root.after(150, self._do_flash)

    # ── 猜測邏輯 ─────────────────────────────────────
    def make_guess(self):
        text = self.entry.get().strip()
        if not text or self.placeholder_active:
            self._set_hint("請輸入一個數字", HINT_ERROR)
            return

        try:
            guess = int(text)
        except ValueError:
            self._set_hint("請輸入有效的整數", HINT_ERROR)
            return

        if guess < self.low or guess > self.high:
            self._set_hint(f"超出範圍，請輸入 {self.low} ~ {self.high}", HINT_ERROR)
            return

        self.entry.delete(0, tk.END)
        self.attempts += 1
        self.attempts_var.set(f"猜測次數：{self.attempts}")

        if guess == self.target:
            self._set_hint(f"🎉 恭喜你猜中了！答案就是 {self.target}", HINT_CORRECT)
            self.history.append((guess, "correct"))
            self._update_history()
            self.draw_range_bar()
            self.guess_btn.config(state=tk.DISABLED)
            self.entry.config(state=tk.DISABLED)
            self._win_animation()
            self._flash_green()
        elif guess < self.target:
            self.low = guess + 1
            self._set_hint("太小了！再大一點", HINT_TOO_LOW)
            self.history.append((guess, "low"))
            self._update_history()
            self.draw_range_bar()
            self.range_var.set(f"目前範圍：{self.low} ~ {self.high}")
        else:
            self.high = guess - 1
            self._set_hint("太大了！再小一點", HINT_TOO_HIGH)
            self.history.append((guess, "high"))
            self._update_history()
            self.draw_range_bar()
            self.range_var.set(f"目前範圍：{self.low} ~ {self.high}")

    # ── 重新開始 ─────────────────────────────────────
    def restart(self):
        self.reset_game()
        self.range_var.set(f"目前範圍：{self.low} ~ {self.high}")
        self.attempts_var.set(f"猜測次數：{self.attempts}")
        self._set_hint("", TEXT_WHITE)
        self.entry.config(state=tk.NORMAL, fg=TEXT_WHITE)
        self.entry.delete(0, tk.END)
        self.placeholder_active = False
        self.entry.focus_set()
        self.guess_btn.config(state=tk.NORMAL)
        self._update_history()
        self.draw_range_bar()
        self.root.configure(bg=BG)


if __name__ == "__main__":
    root = tk.Tk()
    app = GuessingGame(root)
    root.mainloop()
