import random
import tkinter as tk


# ── 色彩主題 ──────────────────────────────────────────
BG          = "#2b2d42"
CARD_BG     = "#3d3f5c"
INPUT_BG    = "#4a4c6a"
TEXT_WHITE   = "#edf2f4"
TEXT_GRAY    = "#d4d4d4"
TEXT_DIM     = "#8d99ae"
ACCENT_GUESS = "#8d99ae"
HOVER_GUESS  = "#ef233c"
ACCENT_RESET = "#06d6a0"
HOVER_RESET  = "#1b9aaa"
HINT_TOO_LOW = "#ff9f1c"
HINT_TOO_HIGH = "#ef233c"
HINT_CORRECT = "#06d6a0"
HINT_ERROR   = "#ef233c"
FONT_FAMILY  = "Microsoft JhengHei"


class GuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("猜數字遊戲（範圍縮小版）")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.placeholder_active = False
        self.reset_game()
        self.build_ui()
        self.center_window(420, 400)

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

    # ── 建立 UI ───────────────────────────────────────
    def build_ui(self):
        # 標題
        tk.Label(
            self.root, text="🎯 猜數字遊戲", bg=BG,
            fg=TEXT_WHITE, font=(FONT_FAMILY, 22, "bold"),
        ).pack(pady=(20, 2))
        tk.Label(
            self.root, text="範圍縮小版 — 請猜 1 ~ 100 之間的數字", bg=BG,
            fg=TEXT_DIM, font=(FONT_FAMILY, 10),
        ).pack()

        # ── 資訊卡片 ──────────────────────────────────
        card = tk.Frame(self.root, bg=CARD_BG, bd=0, highlightthickness=0)
        card.pack(padx=30, pady=(18, 0), fill="x")

        self.range_var = tk.StringVar(value=f"目前範圍：{self.low} ~ {self.high}")
        tk.Label(
            card, textvariable=self.range_var, bg=CARD_BG,
            fg=TEXT_WHITE, font=(FONT_FAMILY, 15, "bold"),
        ).pack(pady=(12, 2))

        self.attempts_var = tk.StringVar(value=f"猜測次數：{self.attempts}")
        tk.Label(
            card, textvariable=self.attempts_var, bg=CARD_BG,
            fg=TEXT_DIM, font=(FONT_FAMILY, 11),
        ).pack(pady=(0, 12))

        # ── 輸入區 ────────────────────────────────────
        input_frame = tk.Frame(self.root, bg=BG)
        input_frame.pack(pady=20)

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
            activeforeground=TEXT_WHITE, bd=0, padx=18, pady=6,
            cursor="hand2", command=self.make_guess,
        )
        self.guess_btn.pack(side=tk.LEFT)
        self.guess_btn.bind("<Enter>", lambda e: self.guess_btn.config(bg=HOVER_GUESS))
        self.guess_btn.bind("<Leave>", lambda e: self.guess_btn.config(bg=ACCENT_GUESS))

        # ── 提示訊息（內嵌） ──────────────────────────
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
            activeforeground=TEXT_WHITE, bd=0, padx=14, pady=4,
            cursor="hand2", command=self.restart,
        )
        self.reset_btn.pack(pady=(5, 18))
        self.reset_btn.bind("<Enter>", lambda e: self.reset_btn.config(bg=HOVER_RESET))
        self.reset_btn.bind("<Leave>", lambda e: self.reset_btn.config(bg=ACCENT_RESET))

    # ── Placeholder 功能 ─────────────────────────────
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
        if not self.entry.get():
            self._show_placeholder()

    # ── 提示顏色 ─────────────────────────────────────
    def _set_hint(self, text, color):
        self.hint_var.set(text)
        self.hint_label.config(fg=color)

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
            self.guess_btn.config(state=tk.DISABLED)
            self.entry.config(state=tk.DISABLED)
        elif guess < self.target:
            self.low = guess + 1
            self._set_hint("太小了！再大一點", HINT_TOO_LOW)
            self.range_var.set(f"目前範圍：{self.low} ~ {self.high}")
        else:
            self.high = guess - 1
            self._set_hint("太大了！再小一點", HINT_TOO_HIGH)
            self.range_var.set(f"目前範圍：{self.low} ~ {self.high}")

    # ── 重新開始 ─────────────────────────────────────
    def restart(self):
        self.reset_game()
        self.range_var.set(f"目前範圍：{self.low} ~ {self.high}")
        self.attempts_var.set(f"猜測次數：{self.attempts}")
        self._set_hint("", TEXT_WHITE)
        self.entry.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)
        self._show_placeholder()
        self.guess_btn.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = GuessingGame(root)
    root.mainloop()
