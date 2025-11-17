import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from knowledge_expert import run_diagnosis

class SleepOptimizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sleep Quality Optimizer - Expert System")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Store user responses
        self.responses = {}
        
        # Create main container
        main_frame = tk.Frame(root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(main_frame, text="🌙 Sleep Quality Optimizer", 
                        font=('Helvetica', 24, 'bold'), 
                        bg='#2c3e50', fg='#ecf0f1')
        title.pack(pady=(0, 10))
        
        subtitle = tk.Label(main_frame, 
                           text="Answer the questions below to receive personalized sleep recommendations",
                           font=('Helvetica', 11), 
                           bg='#2c3e50', fg='#bdc3c7')
        subtitle.pack(pady=(0, 20))
        
        # Create canvas with scrollbar for questions
        canvas_frame = tk.Frame(main_frame, bg='#34495e')
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg='#34495e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#34495e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Question frame (we'll render one question at a time here)
        self.questions_frame = scrollable_frame

        # Build question definitions and start at the first question
        self.build_questions_data()
        self.current_q = 0

        # Container where a single question will be shown
        self.question_container = tk.Frame(self.questions_frame, bg='#34495e')
        self.question_container.pack(fill='both', expand=True, padx=10, pady=10)

        # Navigation / action area (prev / next / analyze)
        self.nav_frame = tk.Frame(main_frame, bg='#2c3e50')
        self.nav_frame.pack(fill='x', pady=(10, 0))

        # Start by showing the first question
        self.show_question(0)

    def build_questions_data(self):
        """Prepare questions as a data list: (text, var_name, options)"""
        # raw question definitions with logical values (may repeat)
        raw_questions = [
            ("1. How would you rate your overall sleep quality?", "sleep_quality",
             [("Excellent", "excellent"), ("Good", "good"), ("Fair", "fair"), ("Poor", "poor"), ("Very Poor", "very_poor")]),
            ("2. How long does it typically take you to fall asleep?", "sleep_onset",
             [("Less than 15 minutes", "normal"), ("15-30 minutes", "normal"), ("30-60 minutes", "long"), ("More than 60 minutes", "long")]),
            ("3. How many times do you wake up during the night?", "night_awakenings",
             [("0 times", "none"), ("1-2 times", "occasional"), ("3-4 times", "frequent"), ("5+ times", "frequent")]),
            ("4. How many hours of sleep do you get per night on average?", "sleep_duration",
             [("Less than 5 hours", "insufficient"), ("5-6 hours", "insufficient"), ("6-7 hours", "adequate"), ("7-9 hours", "adequate"), ("More than 9 hours", "excessive")]),
            ("5. Do you feel excessively sleepy during the day?", "daytime_sleepiness",
             [("Not at all", "low"), ("Occasionally", "medium"), ("Frequently", "high"), ("All the time", "high")]),
            ("6. Do you snore loudly?", "snoring",
             [("No", "none"), ("Occasionally", "mild"), ("Yes, frequently", "loud"), ("I don't know", "unknown")]),
            ("7. Has anyone noticed you stop breathing during sleep?", "breathing_pauses",
             [("Yes", "yes"), ("No", "no"), ("I sleep alone/Don't know", "unknown")]),
            ("8. When do you consume your last caffeinated beverage?", "caffeine_timing",
             [("I don't consume caffeine", "none"), ("Before noon", "early"), ("12 PM - 2 PM", "early"), ("After 2 PM", "late")]),
            ("9. How much screen time do you have in the hour before bed?", "screen_time",
             [("None", "low"), ("Less than 30 minutes", "low"), ("30-60 minutes", "medium"), ("More than 60 minutes", "high")]),
            ("10. Do you experience racing thoughts when trying to sleep?", "racing_thoughts",
             [("Never", "no"), ("Occasionally", "sometimes"), ("Frequently", "yes"), ("Always", "yes")]),
            ("11. How would you rate your current stress level?", "stress_level",
             [("Low", "low"), ("Moderate", "medium"), ("High", "high"), ("Very High", "high")]),
            ("12. Do you experience anxiety symptoms?", "anxiety",
             [("No", "low"), ("Mild", "medium"), ("Moderate", "high"), ("Severe", "high")]),
            ("13. How consistent is your sleep schedule (bedtime and wake time)?", "schedule_consistency",
             [("Very consistent (within 30 min)", "good"), ("Somewhat consistent (within 1 hour)", "fair"), ("Inconsistent (varies by 1-2 hours)", "poor"), ("Very inconsistent (varies by 2+ hours)", "poor")]),
            ("14. Do you work shifts or have an irregular work schedule?", "shift_work",
             [("No, regular schedule", "no"), ("Yes, rotating shifts", "yes"), ("Yes, night shifts", "yes"), ("Yes, irregular hours", "yes")]),
            ("15. Do you go to bed at different times each night?", "irregular_bedtime",
             [("No, usually same time", "no"), ("Sometimes varies", "sometimes"), ("Yes, very irregular", "yes")]),
            ("16. How is your bedroom temperature?", "room_temp",
             [("Too cold", "too_cold"), ("Comfortable (60-67°F)", "comfortable"), ("Too hot", "too_hot")]),
            ("17. How dark is your bedroom at night?", "bedroom_light",
             [("Very dark", "dark"), ("Some light", "dim"), ("Bright/Light pollution", "bright")]),
            ("18. How noisy is your bedroom environment?", "bedroom_noise",
             [("Very quiet", "low"), ("Some noise", "medium"), ("Noisy", "high")]),
            ("19. Do you use your bedroom for activities other than sleep?", "bedroom_activities",
             [("No, only for sleep", "sleep_only"), ("Yes, occasionally", "some"), ("Yes, frequently (TV, work, etc.)", "multiple")]),
            ("20. Do you consume alcohol within 3 hours of bedtime?", "alcohol_consumption",
             [("Never", "no"), ("Occasionally", "sometimes"), ("Frequently", "yes"), ("Daily", "yes")]),
            ("21. When do you typically exercise?", "exercise_timing",
             [("I don't exercise regularly", "none"), ("Morning", "early"), ("Afternoon", "early"), ("Within 3 hours of bedtime", "late")]),
            ("22. When do you eat your last meal?", "meal_timing",
             [("3+ hours before bed", "early"), ("2-3 hours before bed", "moderate"), ("Within 2 hours of bed", "late"), ("Right before bed", "late")]),
            ("23. How often do you nap during the day?", "napping",
             [("Never", "none"), ("Occasionally (< 30 min)", "moderate"), ("Frequently (30+ min)", "excessive"), ("Daily long naps", "excessive")]),
            ("24. Do you experience leg discomfort or restlessness at night?", "leg_discomfort",
             [("No", "no"), ("Occasionally", "sometimes"), ("Frequently", "yes"), ("Always", "yes")]),
            ("25. Do you have an irresistible urge to move your legs when lying down?", "urge_to_move",
             [("No", "no"), ("Sometimes", "sometimes"), ("Yes", "yes")]),
        ]

        # Build questions with unique UI ids for each option, but keep mapping to logical values
        self._ui_to_logical = {}
        self.questions = []
        for q_text, q_name, opts in raw_questions:
            ui_opts = []
            for i, (display, logical_val) in enumerate(opts):
                ui_id = f"{q_name}__opt{i}"
                ui_opts.append((display, ui_id))
                self._ui_to_logical[ui_id] = logical_val
            self.questions.append((q_text, q_name, ui_opts))

        self.total_questions = len(self.questions)

    def clear_question_container(self):
        for child in self.question_container.winfo_children():
            child.destroy()

    def show_question(self, index):
        """Render one question at a time with previous/next controls"""
        # clamp index
        if index < 0:
            index = 0
        if index >= len(self.questions):
            index = len(self.questions) - 1
        self.current_q = index

        # Clear existing question widgets
        self.clear_question_container()

        q_text, q_name, q_options = self.questions[index]

        # Ensure a StringVar exists for this question
        if q_name not in self.responses:
            self.responses[q_name] = tk.StringVar(self.root)

        # Create the question UI
        self.create_question_widget(self.question_container, q_text, q_name, q_options)

        # Update navigation frame
        for child in self.nav_frame.winfo_children():
            child.destroy()

        # Progress label
        progress = tk.Label(self.nav_frame, text=f"Question {index+1} of {self.total_questions}",
                            font=('Helvetica', 10), bg='#2c3e50', fg='#bdc3c7')
        progress.pack(side='left', padx=10)

        # Previous button
        prev_btn = tk.Button(self.nav_frame, text="◀ Previous", command=self.prev_question,
                             font=('Helvetica', 11), bg='#95a5a6', fg='white', relief='flat', padx=12, pady=8, cursor='hand2')
        prev_btn.pack(side='right', padx=6)
        if index == 0:
            prev_btn.config(state=tk.DISABLED)

        # Next or Analyze button
        if index == self.total_questions - 1:
            next_text = "🔍 Analyze"
            next_cmd = self.analyze_sleep
        else:
            next_text = "Next ▶"
            next_cmd = self.next_question

        next_btn = tk.Button(self.nav_frame, text=next_text, command=next_cmd,
                             font=('Helvetica', 11), bg='#3498db', fg='white', relief='flat', padx=12, pady=8, cursor='hand2')
        next_btn.pack(side='right', padx=6)

    def next_question(self):
        # Ensure current has a selection
        q_name = self.questions[self.current_q][1]
        var = self.responses.get(q_name)
        if var is None or not var.get():
            messagebox.showwarning("Select an answer", "Please select an answer before continuing.")
            return
        # Move to next
        if self.current_q < self.total_questions - 1:
            self.show_question(self.current_q + 1)

    def prev_question(self):
        if self.current_q > 0:
            self.show_question(self.current_q - 1)

    
    def create_question_widget(self, parent, question_text, var_name, options):
        """Create a question widget that shows modern, single-select radio options."""
        # Centering container: create an inner frame centered in parent
        q_frame = tk.Frame(parent, bg='#34495e')
        q_frame.pack(fill='both', expand=False, pady=10)

        inner = tk.Frame(q_frame, bg='#34495e')
        inner.pack(anchor='center')

        # Question label (centered)
        question_label = tk.Label(inner, text=question_text,
                                  font=('Helvetica', 14, 'bold'),
                                  bg='#34495e', fg='#ecf0f1',
                                  wraplength=700, justify='center')
        question_label.pack(padx=10, pady=(8, 12))

        # Options container (centered, limited width)
        options_frame = tk.Frame(inner, bg='#34495e')
        options_frame.pack(padx=10, pady=(0, 8))

        # Ensure a unique StringVar exists for this question
        var = self.responses.get(var_name)
        if var is None:
            var = tk.StringVar(self.root)
            self.responses[var_name] = var

        # Widgets list to update visuals
        option_widgets = []

        def refresh_styles(*args):
            sel = var.get()
            for opt_frame, val, label, indicator in option_widgets:
                if val == sel:
                    opt_frame.configure(bg='#34495e')
                    label.configure(bg='#34495e', fg='#3498db', font=('Helvetica', 11, 'bold'))
                    # draw selected indicator
                    indicator.delete('all')
                    indicator.create_oval(2, 2, 16, 16, outline='#3498db', width=2)
                    indicator.create_oval(5, 5, 13, 13, fill='#3498db', outline='')
                else:
                    opt_frame.configure(bg='#2c3e50')
                    label.configure(bg='#2c3e50', fg='#ecf0f1', font=('Helvetica', 10))
                    indicator.delete('all')
                    indicator.create_oval(2, 2, 16, 16, outline='#95a5a6', width=2)

        var.trace_add('write', lambda *a: refresh_styles())

        # Create each option as a centered row with a custom indicator
        for display, value in options:
            opt_frame = tk.Frame(options_frame, bg='#2c3e50', cursor='hand2')
            opt_frame.pack(fill='x', pady=6, ipadx=10)

            # Indicator canvas (custom radio circle)
            indicator = tk.Canvas(opt_frame, width=18, height=18, bg=opt_frame.cget('bg'), highlightthickness=0)
            indicator.pack(side='left', padx=(6, 12), pady=6)
            # default unselected outline
            indicator.create_oval(2, 2, 16, 16, outline='#95a5a6', width=2)

            # Label centered within a fixed-width area
            label = tk.Label(opt_frame, text=display, font=('Helvetica', 10), bg='#2c3e50', fg='#ecf0f1', anchor='w')
            label.pack(side='left', fill='x', expand=True, pady=6)

            # Select handler
            def make_select(v):
                return lambda e=None: var.set(v)

            # Bind clicks to entire row
            opt_frame.bind('<Button-1>', make_select(value))
            label.bind('<Button-1>', make_select(value))
            indicator.bind('<Button-1>', make_select(value))

            # Hover visuals
            def on_enter(e, frame=opt_frame, val=value):
                if var.get() != val:
                    frame.configure(bg='#445566')
                    for child in frame.winfo_children():
                        child.configure(bg='#445566')

            def on_leave(e, frame=opt_frame, val=value):
                if var.get() != val:
                    frame.configure(bg='#2c3e50')
                    for child in frame.winfo_children():
                        child.configure(bg='#2c3e50')

            opt_frame.bind('<Enter>', on_enter)
            opt_frame.bind('<Leave>', on_leave)

            option_widgets.append((opt_frame, value, label, indicator))

        # Initial style refresh
        refresh_styles()
    
    def create_questions(self):
        """Create all question widgets"""
        
        row = 0
        
        # Sleep Quality
        self.create_question_widget(
            self.questions_frame,
            "1. How would you rate your overall sleep quality?",
            "sleep_quality",
            [("Excellent", "excellent"), ("Good", "good"), ("Fair", "fair"), ("Poor", "poor"), ("Very Poor", "very_poor")],
            row
        )
        row += 1
        
        # Sleep Onset
        self.create_question_widget(
            self.questions_frame,
            "2. How long does it typically take you to fall asleep?",
            "sleep_onset",
            [("Less than 15 minutes", "normal"), ("15-30 minutes", "normal"), 
             ("30-60 minutes", "long"), ("More than 60 minutes", "long")],
            row
        )
        row += 1
        
        # Night Awakenings
        self.create_question_widget(
            self.questions_frame,
            "3. How many times do you wake up during the night?",
            "night_awakenings",
            [("0 times", "none"), ("1-2 times", "occasional"), 
             ("3-4 times", "frequent"), ("5+ times", "frequent")],
            row
        )
        row += 1
        
        # Sleep Duration
        self.create_question_widget(
            self.questions_frame,
            "4. How many hours of sleep do you get per night on average?",
            "sleep_duration",
            [("Less than 5 hours", "insufficient"), ("5-6 hours", "insufficient"),
             ("6-7 hours", "adequate"), ("7-9 hours", "adequate"), ("More than 9 hours", "excessive")],
            row
        )
        row += 1
        
        # Daytime Sleepiness
        self.create_question_widget(
            self.questions_frame,
            "5. Do you feel excessively sleepy during the day?",
            "daytime_sleepiness",
            [("Not at all", "low"), ("Occasionally", "medium"), ("Frequently", "high"), ("All the time", "high")],
            row
        )
        row += 1
        
        # Snoring
        self.create_question_widget(
            self.questions_frame,
            "6. Do you snore loudly?",
            "snoring",
            [("No", "none"), ("Occasionally", "mild"), ("Yes, frequently", "loud"), ("I don't know", "unknown")],
            row
        )
        row += 1
        
        # Breathing Pauses
        self.create_question_widget(
            self.questions_frame,
            "7. Has anyone noticed you stop breathing during sleep?",
            "breathing_pauses",
            [("Yes", "yes"), ("No", "no"), ("I sleep alone/Don't know", "unknown")],
            row
        )
        row += 1
        
        # Caffeine Timing
        self.create_question_widget(
            self.questions_frame,
            "8. When do you consume your last caffeinated beverage?",
            "caffeine_timing",
            [("I don't consume caffeine", "none"), ("Before noon", "early"), 
             ("12 PM - 2 PM", "early"), ("After 2 PM", "late")],
            row
        )
        row += 1
        
        # Screen Time
        self.create_question_widget(
            self.questions_frame,
            "9. How much screen time do you have in the hour before bed?",
            "screen_time",
            [("None", "low"), ("Less than 30 minutes", "low"), 
             ("30-60 minutes", "medium"), ("More than 60 minutes", "high")],
            row
        )
        row += 1
        
        # Racing Thoughts
        self.create_question_widget(
            self.questions_frame,
            "10. Do you experience racing thoughts when trying to sleep?",
            "racing_thoughts",
            [("Never", "no"), ("Occasionally", "sometimes"), ("Frequently", "yes"), ("Always", "yes")],
            row
        )
        row += 1
        
        # Stress Level
        self.create_question_widget(
            self.questions_frame,
            "11. How would you rate your current stress level?",
            "stress_level",
            [("Low", "low"), ("Moderate", "medium"), ("High", "high"), ("Very High", "high")],
            row
        )
        row += 1
        
        # Anxiety
        self.create_question_widget(
            self.questions_frame,
            "12. Do you experience anxiety symptoms?",
            "anxiety",
            [("No", "low"), ("Mild", "medium"), ("Moderate", "high"), ("Severe", "high")],
            row
        )
        row += 1
        
        # Schedule Consistency
        self.create_question_widget(
            self.questions_frame,
            "13. How consistent is your sleep schedule (bedtime and wake time)?",
            "schedule_consistency",
            [("Very consistent (within 30 min)", "good"), ("Somewhat consistent (within 1 hour)", "fair"),
             ("Inconsistent (varies by 1-2 hours)", "poor"), ("Very inconsistent (varies by 2+ hours)", "poor")],
            row
        )
        row += 1
        
        # Shift Work
        self.create_question_widget(
            self.questions_frame,
            "14. Do you work shifts or have an irregular work schedule?",
            "shift_work",
            [("No, regular schedule", "no"), ("Yes, rotating shifts", "yes"), 
             ("Yes, night shifts", "yes"), ("Yes, irregular hours", "yes")],
            row
        )
        row += 1
        
        # Irregular Bedtime
        self.create_question_widget(
            self.questions_frame,
            "15. Do you go to bed at different times each night?",
            "irregular_bedtime",
            [("No, usually same time", "no"), ("Sometimes varies", "sometimes"), ("Yes, very irregular", "yes")],
            row
        )
        row += 1
        
        # Room Temperature
        self.create_question_widget(
            self.questions_frame,
            "16. How is your bedroom temperature?",
            "room_temp",
            [("Too cold", "too_cold"), ("Comfortable (60-67°F)", "comfortable"), ("Too hot", "too_hot")],
            row
        )
        row += 1
        
        # Bedroom Light
        self.create_question_widget(
            self.questions_frame,
            "17. How dark is your bedroom at night?",
            "bedroom_light",
            [("Very dark", "dark"), ("Some light", "dim"), ("Bright/Light pollution", "bright")],
            row
        )
        row += 1
        
        # Bedroom Noise
        self.create_question_widget(
            self.questions_frame,
            "18. How noisy is your bedroom environment?",
            "bedroom_noise",
            [("Very quiet", "low"), ("Some noise", "medium"), ("Noisy", "high")],
            row
        )
        row += 1
        
        # Bedroom Activities
        self.create_question_widget(
            self.questions_frame,
            "19. Do you use your bedroom for activities other than sleep?",
            "bedroom_activities",
            [("No, only for sleep", "sleep_only"), ("Yes, occasionally", "some"), 
             ("Yes, frequently (TV, work, etc.)", "multiple")],
            row
        )
        row += 1
        
        # Alcohol
        self.create_question_widget(
            self.questions_frame,
            "20. Do you consume alcohol within 3 hours of bedtime?",
            "alcohol_consumption",
            [("Never", "no"), ("Occasionally", "sometimes"), ("Frequently", "yes"), ("Daily", "yes")],
            row
        )
        row += 1
        
        # Exercise Timing
        self.create_question_widget(
            self.questions_frame,
            "21. When do you typically exercise?",
            "exercise_timing",
            [("I don't exercise regularly", "none"), ("Morning", "early"), 
             ("Afternoon", "early"), ("Within 3 hours of bedtime", "late")],
            row
        )
        row += 1
        
        # Meal Timing
        self.create_question_widget(
            self.questions_frame,
            "22. When do you eat your last meal?",
            "meal_timing",
            [("3+ hours before bed", "early"), ("2-3 hours before bed", "moderate"), 
             ("Within 2 hours of bed", "late"), ("Right before bed", "late")],
            row
        )
        row += 1
        
        # Napping
        self.create_question_widget(
            self.questions_frame,
            "23. How often do you nap during the day?",
            "napping",
            [("Never", "none"), ("Occasionally (< 30 min)", "moderate"), 
             ("Frequently (30+ min)", "excessive"), ("Daily long naps", "excessive")],
            row
        )
        row += 1
        
        # Leg Discomfort
        self.create_question_widget(
            self.questions_frame,
            "24. Do you experience leg discomfort or restlessness at night?",
            "leg_discomfort",
            [("No", "no"), ("Occasionally", "sometimes"), ("Frequently", "yes"), ("Always", "yes")],
            row
        )
        row += 1
        
        # Urge to Move Legs
        self.create_question_widget(
            self.questions_frame,
            "25. Do you have an irresistible urge to move your legs when lying down?",
            "urge_to_move",
            [("No", "no"), ("Sometimes", "sometimes"), ("Yes", "yes")],
            row
        )
        row += 1
    
    def analyze_sleep(self):
        """Analyze sleep patterns and show results"""
        # Check if all questions are answered
        unanswered = []
        for var_name, var in self.responses.items():
            if not var.get():
                unanswered.append(var_name)

        if unanswered:
            messagebox.showwarning("Incomplete Form", 
                                  f"Please answer all questions before analyzing.\n\n"
                                  f"{len(unanswered)} question(s) remaining.")
            return

        # Collect user inputs and translate UI ids back to logical values
        user_inputs = {}
        for var_name, var in self.responses.items():
            ui_val = var.get()
            # map UI id to logical value if mapping exists
            logical = self._ui_to_logical.get(ui_val, ui_val)
            user_inputs[var_name] = logical
        
        # Run expert system
        try:
            diagnoses, recommendations, confidence_scores = run_diagnosis(user_inputs)
            
            # Show results
            self.show_results(diagnoses, recommendations, confidence_scores)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during analysis:\n{str(e)}")
    
    def show_results(self, diagnoses, recommendations, confidence_scores):
        """Display analysis results in a new window"""
        
        results_window = tk.Toplevel(self.root)
        results_window.title("Sleep Analysis Results")
        results_window.geometry("800x600")
        results_window.configure(bg='#2c3e50')
        
        # Main frame
        main_frame = tk.Frame(results_window, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(main_frame, text="📊 Your Sleep Analysis Results", 
                        font=('Helvetica', 20, 'bold'), 
                        bg='#2c3e50', fg='#ecf0f1')
        title.pack(pady=(0, 20))
        
        # Small illustrative icons row (drawn inline so no external assets required)
        icons_row = tk.Frame(main_frame, bg='#2c3e50')
        icons_row.pack(fill='x', pady=(0, 10))

        def _draw_magnifier(c):
            c.create_oval(4,4,28,28, outline='#3498db', width=2)
            c.create_line(20,20,30,30, fill='#3498db', width=3)

        def _draw_lightbulb(c):
            c.create_oval(6,2,26,22, outline='#f1c40f', width=2)
            c.create_rectangle(12,20,20,28, fill='#f1c40f', outline='')

        def _draw_warning(c):
            c.create_polygon(18,4, 4, thirty:=30 if False else 30, 32,30, outline='#f1c40f', fill='#f39c12')
            c.create_text(18,20, text='!', fill='white', font=('Helvetica', 12, 'bold'))

        # Magnifier icon
        mag_can = tk.Canvas(icons_row, width=36, height=36, bg='#2c3e50', highlightthickness=0)
        _draw_magnifier(mag_can)
        mag_can.pack(side='left', padx=12)
        tk.Label(icons_row, text='Findings', font=('Helvetica', 9), bg='#2c3e50', fg='#bdc3c7').pack(side='left', padx=(0,18))

        # Lightbulb icon
        bulb_can = tk.Canvas(icons_row, width=36, height=36, bg='#2c3e50', highlightthickness=0)
        _draw_lightbulb(bulb_can)
        bulb_can.pack(side='left', padx=12)
        tk.Label(icons_row, text='Recommendations', font=('Helvetica', 9), bg='#2c3e50', fg='#bdc3c7').pack(side='left', padx=(0,18))

        # Warning icon
        warn_can = tk.Canvas(icons_row, width=36, height=36, bg='#2c3e50', highlightthickness=0)
        # simple triangle with exclamation
        warn_can.create_polygon(18,4, 4,32, 32,32, outline='#f1c40f', fill='#f39c12')
        warn_can.create_text(18,22, text='!', fill='white', font=('Helvetica', 12, 'bold'))
        warn_can.pack(side='left', padx=12)
        tk.Label(icons_row, text='Disclaimer', font=('Helvetica', 9), bg='#2c3e50', fg='#bdc3c7').pack(side='left', padx=(0,18))
        
        # Create scrolled text widget
        text_widget = scrolledtext.ScrolledText(main_frame, 
                                               wrap=tk.WORD, 
                                               font=('Helvetica', 11),
                                               bg='#34495e',
                                               fg='#ecf0f1',
                                               padx=15,
                                               pady=15)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for formatting
        text_widget.tag_configure("heading", font=('Helvetica', 14, 'bold'), foreground='#3498db')
        text_widget.tag_configure("diagnosis", font=('Helvetica', 12, 'bold'), foreground='#e74c3c')
        text_widget.tag_configure("confidence", font=('Helvetica', 10, 'italic'), foreground='#95a5a6')
        text_widget.tag_configure("high_priority", foreground='#e74c3c', font=('Helvetica', 11, 'bold'))
        text_widget.tag_configure("medium_priority", foreground='#f39c12', font=('Helvetica', 11))
        text_widget.tag_configure("low_priority", foreground='#2ecc71', font=('Helvetica', 11))
        
        # Insert content
        if not diagnoses:
            text_widget.insert(tk.END, "No specific issues detected. ", "diagnosis")
            text_widget.insert(tk.END, "Your sleep pattern appears healthy!\n\n")
        else:
            text_widget.insert(tk.END, "🔍 DIAGNOSES IDENTIFIED:\n\n", "heading")
            
            for diagnosis in diagnoses:
                confidence = confidence_scores.get(diagnosis, 0.5)
                text_widget.insert(tk.END, f"• {diagnosis}\n", "diagnosis")
                text_widget.insert(tk.END, f"  Confidence: {confidence*100:.0f}%\n\n", "confidence")
        
        text_widget.insert(tk.END, "\n" + "="*80 + "\n\n")
        text_widget.insert(tk.END, "💡 RECOMMENDATIONS:\n\n", "heading")
        
        if not recommendations:
            text_widget.insert(tk.END, "Keep up your healthy sleep habits!\n")
        else:
            # Sort recommendations by priority
            priority_order = {"high": 1, "medium": 2, "low": 3}
            sorted_recommendations = sorted(recommendations, 
                                          key=lambda x: priority_order.get(x[1], 3))
            
            current_priority = None
            for rec, priority in sorted_recommendations:
                # Add priority header
                if priority != current_priority:
                    current_priority = priority
                    text_widget.insert(tk.END, f"\n{priority.upper()} PRIORITY:\n", 
                                     f"{priority}_priority")
                
                # Add recommendation
                text_widget.insert(tk.END, f"  ✓ {rec}\n", f"{priority}_priority")
        
        # Add disclaimer
        text_widget.insert(tk.END, "\n\n" + "="*80 + "\n\n")
        text_widget.insert(tk.END, "⚠️ IMPORTANT DISCLAIMER:\n\n", "heading")
        text_widget.insert(tk.END, 
                          "This expert system provides educational information only and is NOT a substitute "
                          "for professional medical advice. If you have persistent sleep problems, daytime "
                          "impairment, or suspect a serious condition like sleep apnea, please consult a "
                          "healthcare provider or sleep specialist.\n\n"
                          "If you experience severe symptoms, seek medical attention immediately.")
        
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(main_frame, text="Close", 
                             command=results_window.destroy,
                             font=('Helvetica', 12, 'bold'),
                             bg='#95a5a6', fg='white',
                             activebackground='#7f8c8d',
                             cursor='hand2',
                             padx=20, pady=8)
        close_btn.pack(pady=(15, 0))

def main():
    root = tk.Tk()
    app = SleepOptimizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()