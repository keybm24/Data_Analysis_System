import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---- Main Window ----
root = tk.Tk()
root.title("Data Analysis System")
root.geometry("900x600")
root.configure(bg="#f0f0f0")

df_global = None

# ---- Load File ----
def load_file():
    global df_global
    file_path = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if not file_path:
        return
    try:
        df_global = pd.read_excel(file_path)
        show_summary(df_global)
        populate_table(df_global)
        populate_columns(df_global)
        messagebox.showinfo("Success", "File loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not load file:\n{e}")

# ---- Summary ----
def show_summary(df):
    summary_text.config(state="normal")
    summary_text.delete(1.0, tk.END)
    summary = f"Rows: {df.shape[0]}    Columns: {df.shape[1]}\n\n"
    for col in df.select_dtypes(include="number").columns:
        summary += f"{col}:\n"
        summary += f"  Total:   {df[col].sum():,.2f}\n"
        summary += f"  Average: {df[col].mean():,.2f}\n"
        summary += f"  Max:     {df[col].max():,.2f}\n"
        summary += f"  Min:     {df[col].min():,.2f}\n\n"
    summary_text.insert(tk.END, summary)
    summary_text.config(state="disabled")

# ---- Table ----
def populate_table(df):
    for item in table.get_children():
        table.delete(item)
    table["columns"] = list(df.columns)
    table["show"] = "headings"
    for col in df.columns:
        table.heading(col, text=col)
        table.column(col, width=120)
    for _, row in df.head(50).iterrows():
        table.insert("", tk.END, values=list(row))

# ---- Column Selector ----
def populate_columns(df):
    numeric_cols = list(df.select_dtypes(include="number").columns)
    col_selector["values"] = numeric_cols
    if numeric_cols:
        col_selector.current(0)

# ---- Generate Chart ----
def generate_chart():
    if df_global is None:
        messagebox.showwarning("Warning", "Please load a file first.")
        return
    col = col_selector.get()
    chart_type = chart_selector.get()
    if not col:
        messagebox.showwarning("Warning", "Please select a column.")
        return

    fig, ax = plt.subplots(figsize=(6, 3))
    fig.patch.set_facecolor("#f0f0f0")

    if chart_type == "Bar Chart":
        df_global[col].value_counts().plot(kind="bar", ax=ax, color="#4C72B0")
    elif chart_type == "Line Chart":
        df_global[col].plot(kind="line", ax=ax, color="#4C72B0")
    elif chart_type == "Pie Chart":
        df_global[col].value_counts().plot(kind="pie", ax=ax, autopct="%1.1f%%")

    ax.set_title(f"{chart_type} - {col}")
    plt.tight_layout()

    chart_window = tk.Toplevel(root)
    chart_window.title(f"Chart: {col}")
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# ---- UI Layout ----
top_frame = tk.Frame(root, bg="#4C72B0", pady=10)
top_frame.pack(fill=tk.X)

tk.Label(top_frame, text="Data Analysis System", font=("Arial", 16, "bold"),
         bg="#4C72B0", fg="white").pack(side=tk.LEFT, padx=20)

tk.Button(top_frame, text="📂 Load Excel File", command=load_file,
          bg="white", fg="#4C72B0", font=("Arial", 10, "bold"),
          padx=10, pady=5).pack(side=tk.RIGHT, padx=20)

main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Left: Summary
left_frame = tk.Frame(main_frame, bg="white", relief="groove", bd=1)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=5)

tk.Label(left_frame, text="Summary", font=("Arial", 11, "bold"),
         bg="white").pack(pady=5)

summary_text = tk.Text(left_frame, width=30, state="disabled",
                       font=("Courier", 9), bg="white", relief="flat")
summary_text.pack(padx=10, pady=5, fill=tk.Y, expand=True)

# Right: Table + Chart controls
right_frame = tk.Frame(main_frame, bg="#f0f0f0")
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

table = ttk.Treeview(right_frame)
table.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

scrollbar = ttk.Scrollbar(right_frame, orient="horizontal", command=table.xview)
scrollbar.pack(fill=tk.X)
table.configure(xscrollcommand=scrollbar.set)

# Chart controls
chart_frame = tk.Frame(right_frame, bg="white", relief="groove", bd=1, pady=8)
chart_frame.pack(fill=tk.X)

tk.Label(chart_frame, text="Column:", bg="white").pack(side=tk.LEFT, padx=10)
col_selector = ttk.Combobox(chart_frame, width=20, state="readonly")
col_selector.pack(side=tk.LEFT, padx=5)

tk.Label(chart_frame, text="Chart type:", bg="white").pack(side=tk.LEFT, padx=10)
chart_selector = ttk.Combobox(chart_frame, values=["Bar Chart", "Line Chart", "Pie Chart"],
                               width=15, state="readonly")
chart_selector.current(0)
chart_selector.pack(side=tk.LEFT, padx=5)

tk.Button(chart_frame, text="📊 Generate Chart", command=generate_chart,
          bg="#4C72B0", fg="white", font=("Arial", 10, "bold"),
          padx=10).pack(side=tk.LEFT, padx=15)

root.mainloop()