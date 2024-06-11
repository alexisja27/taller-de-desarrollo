import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient


def get_players():
    # Conectar a MongoDB
    client = MongoClient(
        "mongodb+srv://alexis:aj00ta@cluster0.iypp2gq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
    db = client["badlockdb"]
    collection = db["players"]

    # Obtener lista de jugadores
    players = list(collection.find())
    return players


# Función para eliminar todos los jugadores de la base de datos
def delete_players():
    # Conectar a MongoDB
    client = MongoClient(
        "mongodb+srv://alexis:aj00ta@cluster0.iypp2gq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
    db = client["badlockdb"]
    collection = db["players"]

    # Eliminar todos los jugadores
    collection.delete_many({})

    print("Todos los jugadores han sido eliminados.")


def create_table_ui(root, players):
    columns = ["Username", "Online"]
    tree = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)

    for player in players:
        tree.insert("", "end", values=(player["username"], player["online"]))

    tree.pack(fill=tk.BOTH, expand=True)

    return tree


def add_player(username, online):
    if username:
        client = MongoClient(
            "mongodb+srv://alexis:aj00ta@cluster0.iypp2gq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        )
        db = client["badlockdb"]
        collection = db["players"]
        new_player = {"username": username, "online": online}
        collection.insert_one(new_player)
        return new_player
    return None


def on_add_player():
    username = username_entry.get()
    online = online_var.get()
    new_player = add_player(username, online)
    if new_player:
        tree.insert("", "end", values=(new_player["username"], new_player["online"]))
        username_entry.delete(0, tk.END)
        online_var.set(False)


def on_key_press(event):
    if event.keysym == "Return":
        players = get_players()
        for item in tree.get_children():
            tree.delete(item)
        for player in players:
            tree.insert("", "end", values=(player["username"], player["online"]))


# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Lista de Jugadores")
    root.geometry("400x400")

    # Usar estilo ttk
    style = ttk.Style()
    style.theme_use("clam")

    main_frame = ttk.Frame(root, padding="10 10 10 10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Entry para nuevo usuario
    username_label = ttk.Label(main_frame, text="Nombre de Usuario:")
    username_label.grid(column=0, row=0, sticky=tk.W, pady=5)

    username_entry = ttk.Entry(main_frame, width=30)
    username_entry.grid(column=1, row=0, pady=5)

    # Checkbutton para estado en línea
    online_var = tk.BooleanVar()
    online_checkbutton = ttk.Checkbutton(main_frame, text="Online", variable=online_var)
    online_checkbutton.grid(column=1, row=1, pady=5)

    # Botón para agregar usuario
    add_button = ttk.Button(main_frame, text="Agregar Jugador", command=on_add_player)
    add_button.grid(column=1, row=2, pady=10)

    # Crear tabla de jugadores
    tree_frame = ttk.Frame(main_frame)
    tree_frame.grid(
        column=0, row=3, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S, pady=10
    )

    players = get_players()
    tree = create_table_ui(tree_frame, players)

    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(3, weight=1)

    # Llamar a la función cuando se presiona Enter
    root.bind("<Return>", on_key_press)

    root.mainloop()
