#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk

DATA = [
    (1, "Manzana", 0.99),
    (2, "Banana", 0.59),
    (3, "Cereza", 2.49),
    (4, "Durazno", 1.49),
    (5, "Uva", 2.99),
    (6, "Kiwi", 1.09),
    (7, "Mango", 1.89),
    (8, "Naranja", 0.79),
    (9, "Pera", 1.19),
    (10, "Sandía", 3.99),
]

def make_table(root):
    root.title("Minimal Treeview Table (Tkinter)")

    # --- container frame
    frm = ttk.Frame(root, padding=8)
    frm.grid(sticky="nsew")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # --- treeview (table)
    columns = ("id", "producto", "precio")
    tree = ttk.Treeview(frm, columns=columns, show="headings", height=12)
    tree.grid(row=0, column=0, sticky="nsew")

    # --- scrollbar
    vsb = ttk.Scrollbar(frm, orient="vertical", command=tree.yview)
    vsb.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=vsb.set)

    # --- table sizing behavior
    frm.rowconfigure(0, weight=1)
    frm.columnconfigure(0, weight=1)

    # --- headings & columns
    tree.heading("id", text="ID", command=lambda c="id": sort_by(tree, c))
    tree.heading("producto", text="Producto", command=lambda c="producto": sort_by(tree, c))
    tree.heading("precio", text="Precio (€)", command=lambda c="precio": sort_by(tree, c))

    tree.column("id", width=60, anchor="e")
    tree.column("producto", width=200, anchor="w")
    tree.column("precio", width=100, anchor="e")

    # --- striped rows
    tree.tag_configure("odd", background="#f7f7f7")
    tree.tag_configure("even", background="#ffffff")

    # --- populate
    for i, row in enumerate(DATA):
        tags = ("even",) if i % 2 == 0 else ("odd",)
        tree.insert("", "end", values=row, tags=tags)

    # --- double click handler
    def on_open(event):
        item_id = tree.focus()
        if not item_id:
            return
        print("Selected row:", tree.item(item_id, "values"))

    tree.bind("<Double-1>", on_open)

    return tree

# --- sorting helper
_sort_state = {}  # column -> bool (True asc, False desc)
def sort_by(tree: ttk.Treeview, column: str):
    # Extract column values
    rows = [(tree.set(k, column), k) for k in tree.get_children("")]
    # Try numeric sort if possible, else lexical (casefold for nicer results)
    def cast(x):
        try:
            return float(x.replace(",", "."))
        except Exception:
            return x.casefold()
    rows.sort(key=lambda t: cast(t[0]), reverse=_sort_state.get(column, False))
    _sort_state[column] = not _sort_state.get(column, False)

    # Reinsert in new order
    for index, (_, iid) in enumerate(rows):
        tree.move(iid, "", index)

if __name__ == "__main__":
    root = tk.Tk()
    make_table(root)
    root.mainloop()

