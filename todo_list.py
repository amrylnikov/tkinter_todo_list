import tkinter as tk
from tkinter import messagebox
import sqlite3


def load_tasks():
    listbox.delete(0, tk.END)
    cursor.execute(
        '''
        SELECT
            task
        FROM
            tasks
        '''
    )
    tasks = cursor.fetchall()
    for task in tasks:
        listbox.insert(tk.END, task[0])


def add_task():
    task = entry.get()
    if task:
        cursor.execute(
            '''
            INSERT INTO tasks (task)
            VALUES
                (?)
            ''', (task,)
        )
        conn.commit()
        entry.delete(0, tk.END)
        load_tasks()
    else:
        messagebox.showwarning('Invalid Input', 'Please enter a task.')


def delete_task():
    try:
        index = listbox.curselection()
        task = listbox.get(index)
        cursor.execute(
            '''
            DELETE FROM
                tasks
            WHERE
                task = ?
            ''', (task,)
        )
        conn.commit()
        listbox.delete(index)
    except tk.TclError:
        messagebox.showwarning('No Task Selected', 'Please select a task.')


def edit_task():
    try:
        index = listbox.curselection()
        edited_task = entry.get()
        if edited_task:
            original_task = listbox.get(index)
            listbox.delete(index)
            listbox.insert(index, edited_task)
            entry.delete(0, tk.END)
            cursor.execute(
                '''
                UPDATE
                    tasks
                SET
                    task = ?
                WHERE
                    task = ?
                ''', (edited_task, original_task)
            )
            conn.commit()
        else:
            messagebox.showwarning("Invalid Input", "Please enter a task.")
    except tk.TclError:
        messagebox.showwarning("No Task Selected", "Please select a task.")


def close_app(connection):
    conn.close()
    window.destroy()


conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT
    )
    '''
)
conn.commit()

window = tk.Tk()
window.title("Todo App")
window.geometry('700x450+100+100')

my_frame = tk.Frame(window)
my_frame.pack(pady=10)

label = tk.Label(
    my_frame, text='Daily Tasks', font=('Arial', 20, 'bold'), pady=10
)
label.pack(pady=10)

entry = tk.Entry(my_frame, width=60)
entry.pack(side="top", pady=10)

listbox = tk.Listbox(my_frame, width=50)
listbox.pack(side="left", fill="both")

scrollbar = tk.Scrollbar(my_frame)
scrollbar.pack(side="right", fill="both")

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

load_tasks()

add_button = tk.Button(
    window, text="Add", width=50, bg="#03bafc", fg='white', command=add_task
)
add_button.pack(pady=5)

edit_button = tk.Button(
    window, text="Edit", width=50, bg="#03bafc", fg='white', command=edit_task
)
edit_button.pack(pady=5)

delete_button = tk.Button(
    window, text="Delete", width=50, bg="#03bafc", fg='white',
    command=delete_task
)
delete_button.pack(pady=5)

window.protocol("WM_DELETE_WINDOW", lambda: close_app(conn))
window.mainloop()
