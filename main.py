import os
import math
from getpass import getpass

# Role identifiers
GUEST = -1
ADMIN = 0
STAFF = 1
MEMBER = 2

roles = ["ADMIN", "STAFF", "MEMBER", "GUEST"]

# Table names
USERS_TABLE = "users"
BOOKS_TABLE = "books"
BORROW_LOGS = "borrow_logs"

username = "Anonymous"
role = -1

log_message = ""
history = []


# Helper functions
def exception_quit(e):
    print(f"Error: {e}")
    # raise e
    input("Press enter to quit...")
    exit()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def menu(func):
    def wrapper(*args, **kwargs):
        clear_screen()

        global log_message, history

        history.append(func)

        if log_message:
            print(log_message)
            log_message = ""

        return func(*args, **kwargs)

    return wrapper


def option_value(x):
    return lambda: x


def prompt_yes_no(prompt):
    return input(f"{prompt} (Y/N): ").lower() == "y"


def prompt_options(option_texts, option_functions=None, error_function=exception_quit):
    option_functions = option_functions or [
        option_value(i) for i in range(len(option_texts))
    ]

    try:
        print(
            *[f"[{i}] {option_text}" for i, option_text in enumerate(option_texts, 1)],
            sep="\n",
        )

        return option_functions[int(input("Enter option: ") or 1) - 1]()
    except Exception as e:
        try:
            return error_function(e)
        except TypeError:
            return error_function()


def paginator(
    option_texts: list,
    option_functions: list,
    page_index=0,
    page_title="",
    max_per_page=6,
    cancel_function=None,
    error_function=exception_quit,
):
    total_options = len(option_texts)
    total_page = math.ceil(total_options / max_per_page)

    page_options = option_texts[
        page_index * max_per_page : page_index * max_per_page + max_per_page
    ]
    page_functions = option_functions[
        page_index * max_per_page : page_index * max_per_page + max_per_page
    ]

    def previous_page():
        return paginator(
            option_texts,
            option_functions,
            page_index - 1 if page_index > 0 else total_page - 1,
            page_title,
            max_per_page,
            cancel_function=cancel_function,
            error_function=error_function,
        )

    def next_page():
        return paginator(
            option_texts,
            option_functions,
            page_index + 1 if page_index < total_page - 1 else 0,
            page_title,
            max_per_page,
            cancel_function=cancel_function,
            error_function=error_function,
        )

    clear_screen()
    print(page_title)
    print(f"Page {page_index + 1}/{total_page}")

    options = [*page_options, "Previous page", "Next page", "Back to menu"]
    functions = [*page_functions, previous_page, next_page, back]

    if cancel_function:
        options.append("Cancel")
        functions.append(cancel_function)

    return prompt_options(
        options,
        functions,
        error_function=error_function,
    )


def prompt_inputs(*prompts, types=None):
    types = types or [str] * len(prompts)
    return [
        data_type(input(prompt + ": ")) for data_type, prompt in zip(types, prompts)
    ]


def back(skip_repeat=True):
    global history
    if not history:
        raise Exception("No history to back")

    page = history.pop()

    while skip_repeat and history and page == history[-1]:
        history.pop()

    if not history:
        raise Exception("No history to back")

    return menu(history[-1])()


def log_and_redirect(func, message):
    def inner():
        print_log(message)
        return func()

    return inner


def print_log(message):
    global log_message
    log_message = message


# File functions
def load_table(table_name):
    with open(f"{table_name}.txt", "r") as f:
        raw_rows = f.readlines()

    first_column, raw_types, *raw_data_rows = map(
        lambda row: row.strip().split(","), raw_rows
    )
    types = list(map(eval, raw_types))
    data_rows = [
        [types[i](cell) for i, cell in enumerate(data_row)]
        for data_row in raw_data_rows
    ]

    return [first_column, raw_types, *data_rows]


def dump_table(table_name, table):
    with open(f"{table_name}.txt", "w") as f:
        print(*[",".join(map(str, row)) for row in table], sep="\n", file=f)


def get_column(table, index):
    return [row[index] for row in table]


def get_column_by_name(table, column):
    index = table[0].index(column)
    return get_column(table, index)


def print_divider(column_sizes):
    print(end="+")
    print(*map("-".__mul__, column_sizes), sep="+", end="+\n")


def print_row(row, column_sizes):
    print(end="|")
    print(
        *[cell.ljust(size) for cell, size in zip(row, column_sizes)], sep="|", end="|\n"
    )
    print_divider(column_sizes)


def print_table(table, padding=0):
    first_row, __types, *data_rows = table
    display_rows = [list(map(str, row)) for row in [first_row] + data_rows]

    column_sizes = [
        max(map(len, get_column(display_rows, i))) + padding
        for i in range(len(first_row))
    ]

    print_divider(column_sizes)

    for row in display_rows:
        print_row(row, column_sizes)


def add_rows(table_name, columns, *value_rows):
    first_row, types, *data_rows = load_table(table_name)

    if len(first_row) != len(columns):
        raise Exception(
            "Please provide data for every column, null values are prohibited"
        )

    if sorted(first_row) != sorted(columns):
        raise Exception("Wrong column name, please double-check")

    index_map = [first_row.index(column) for column in columns]

    for value_row in value_rows:
        insert_row = [eval(data_type)() for data_type in types]

        for i, (cell, data_type) in enumerate(zip(value_row, types)):
            if type(cell).__name__ != data_type:
                try:
                    cell = eval(data_type)(cell)  # Attempt to convert cell
                except ValueError:
                    raise ValueError(
                        f"Error adding row: {value_row}, cell at column {i} is expected to be type {data_type}, found {type(cell).__name__}"
                    )
            insert_row[index_map[i]] = cell

        data_rows.append(insert_row)

    dump_table(table_name, [first_row, types, *data_rows])


def delete_rows(table_name, filter_func=lambda x: True):
    first_row, types, *data_rows = load_table(table_name)

    new_rows = [row for row in data_rows if not filter_func([first_row, types, row])]
    dump_table(table_name, [first_row, types, *new_rows])


def update_rows(table_name, *column_value_pairs, filter_func=lambda x: True):
    table = load_table(table_name)
    types = table[1]

    column_idx_value_pairs = [
        (table[0].index(column), value) for column, value in column_value_pairs
    ]

    for row in table[2:]:
        if not filter_func(table[:2] + [row]):
            continue

        for column_idx, value in column_idx_value_pairs:
            expected_type = types[column_idx]

            if type(value).__name__ != expected_type:
                try:
                    value = eval(expected_type)(value)  # Attempt to convert value
                except ValueError:
                    raise ValueError(
                        f"Error updating row: {row}, cell at column {column_idx} is expected to be type {expected_type}, found {type(value).__name__}"
                    )

            row[column_idx] = value

    dump_table(table_name, table)


def filter_rows(table, filter_func):
    first_row, types, *data_rows = table

    return [first_row, types] + [
        data_row for data_row in data_rows if filter_func([first_row, types, data_row])
    ]


def filter_columns(table, columns):
    selects = [table[0].index(column) for column in columns]

    return [[cell for i, cell in enumerate(row) if i in selects] for row in table]


def where_equal(*column_value_pairs):
    def inner(table_row):
        for column, value in column_value_pairs:
            if get_column_by_name(table_row, column)[-1] != value:
                return False
        return True

    return inner


def where_greater(*column_value_pairs):
    def inner(table_row):
        for column, value in column_value_pairs:
            if get_column_by_name(table_row, column)[-1] <= value:
                return False
        return True

    return inner


def where_not(func):
    return lambda table_row: not func(table_row)


def where_and(*funcs):
    return lambda table_row: all(func(table_row) for func in funcs)


def where_or(*funcs):
    return lambda table_row: any(func(table_row) for func in funcs)


def is_empty(table):
    return len(table) == 2  # Empty if table only contains first two row


# User table functions
def create_user(username, password, role=MEMBER):
    users = load_table(USERS_TABLE)
    id = max(get_column_by_name(users, "id")[2:]) + 1  # Incremental id

    add_rows(
        USERS_TABLE,
        ("id", "username", "password", "role"),
        (id, username, password, role),
    )


# Book table functions
def create_book(title, author, isbn, quantity=1):
    books = load_table(BOOKS_TABLE)
    id = max(get_column_by_name(books, "id")[2:]) + 1  # Incremental id

    add_rows(
        BOOKS_TABLE,
        ("id", "title", "author", "isbn", "quantity"),
        (id, title, author, isbn, quantity),
    )


# Admin features
@menu
def book_management():
    return prompt_options(
        ["Add new books", "Remove books", "Modify books", "Back"],
        [add_book, remove_book, modify_book, back],
    )


@menu
def add_book():
    title, author, isbn = prompt_inputs("Title", "Author", "ISBN")

    if not isbn.isdigit():
        print_log("ISBN should be a number, please try again")
        return add_book()

    create_book(title, author, int(isbn))

    print_log(f"Book [{isbn}]{title} successfully created")
    return back()


@menu
def remove_book():
    books = load_table(BOOKS_TABLE)
    titles = get_column_by_name(books, "title")[2:]
    ids = get_column_by_name(books, "id")[2:]

    result = paginator(
        titles,
        [option_value(i) for i in range(len(titles))],
        page_title="Select a book to delete",
        error_function=log_and_redirect(
            back, "Book delete operation cancelled, invalid option"
        ),
    )

    book_id = ids[result]
    book_title = titles[result]

    if prompt_yes_no(f"Delete book <<{book_title}>>?"):
        delete_rows(BOOKS_TABLE, where_equal(("id", book_id)))
        print_log(f"Deleted book {book_title}")
        return back()

    else:
        print_log("Book delete operation cancelled")
        return back()


@menu
def modify_book():
    books = load_table(BOOKS_TABLE)
    titles = get_column_by_name(books, "title")[2:]
    ids = get_column_by_name(books, "id")[2:]
    isbns = get_column_by_name(books, "isbn")[2:]

    result = paginator(
        titles,
        [option_value(i) for i in range(len(titles))],
        page_title="Select a book to modify",
        error_function=log_and_redirect(
            back, "Book modification cancelled, invalid option"
        ),
    )

    book_id = ids[result]
    book_title = titles[result]
    book_isbn = isbns[result]

    clear_screen()

    print(f"Modifying  [{book_isbn}]<<{book_title}>>")
    print("Which field would you like to modify?")

    modifiable_fields = ["title", "author", "isbn", "quantity"]
    field_idx = prompt_options(
        ["Title", "Author", "ISBN", "Quantity", "Cancel"],
        [option_value(i) for i in range(len(modifiable_fields))]
        + [log_and_redirect(back, "Book modification cancelled")],
        error_function=log_and_redirect(
            back, "Book modification cancelled, invalid option"
        ),
    )
    field = modifiable_fields[field_idx]

    field_text = ("title", "author", "ISBN", "quantity")[field_idx]

    old_value = get_column_by_name(books, field)[result + 2]

    clear_screen()

    new_value = (
        input(
            f"Current book {field_text}: {old_value}\n"
            f"Enter new value (leave blank to keep current value): "
        )
        or old_value
    )

    expected_type = get_column_by_name(books, field)[1]

    try:
        new_value = eval(expected_type)(new_value)
    except ValueError:
        print_log(
            f"Invalid value, field '{field_text}' is expected to be {expected_type}"
        )
        return modify_book()

    update_rows(
        BOOKS_TABLE, (field, new_value), filter_func=where_equal(("id", book_id))
    )

    print_log(f"Successfully modified\n{old_value} -> {new_value}")

    return back()


@menu
def user_management():
    return prompt_options(
        ["Add new user", "Remove user", "Back"],
        [add_user, remove_user, back],
    )


@menu
def add_user():
    print("What kind of user would you like to create?")
    user_role = prompt_options(
        ["Staff", "Member"], [option_value(STAFF), option_value(MEMBER)]
    )

    clear_screen()

    username = input("Username: ")
    password = getpass()

    create_user(username, password, user_role)

    print_log(f"User [{roles[user_role]}] {username} successfully created")
    return back()


@menu
def remove_user():
    users = load_table(USERS_TABLE)
    usernames = get_column_by_name(users, "username")[2:]
    ids = get_column_by_name(users, "id")[2:]

    result = paginator(
        usernames,
        [option_value(i) for i in range(len(usernames))],
        page_title="Select a user to delete",
        error_function=log_and_redirect(
            back, "User delete operation cancelled, invalid option"
        ),
    )

    user_id = ids[result]
    user_name = usernames[result]

    if prompt_yes_no(f"Delete user <<{user_name}>>?"):
        delete_rows(USERS_TABLE, where_equal(("id", user_id)))
        print_log(f"Deleted user {user_name}")
        return back()

    else:
        print_log("User delete operation cancelled")
        return back()


# Staff features
@menu
def search_menu():
    query = input("Enter search query: ")
    # TODO search for users and display results
    pass


# Member features
# TODO

# Guest features
# TODO


# Home menu
@menu
def home_menu():
    return prompt_options(
        ["Login", "Continue as guest", "Quit Program"],
        [login_menu, user_menu, exit],
    )


@menu
def login_menu():
    global username, role
    username = input("Username: ")
    password = getpass()

    table = load_table(USERS_TABLE)
    user = filter_rows(
        table, where_equal(("username", username), ("password", password))
    )

    if is_empty(user):
        print_log("Login failed, invalid credentials, please try again.")
        return login_menu()

    username = get_column_by_name(user, "username")[-1]
    role = get_column_by_name(user, "role")[-1]

    print_log(
        f"[{roles[role]}] {username}, welcome to the LMS (Ligma Management System)\n"
        + """
            _     _                       
            | |   (_) __ _ _ __ ___   __ _ 
            | |   | |/ _` | '_ ` _ \ / _` |
            | |___| | (_| | | | | | | (_| |
            |_____|_|\__, |_| |_| |_|\__,_|
                    |___/    
        """
    )

    return user_menu()


@menu
def user_menu():
    menu_options = []

    # TODO add options for each user
    match role:
        case 0:  # Admin
            menu_options = [
                ("Book Management", book_management),
                ("User Management", user_management),
            ]
        case 1:  # Staff
            menu_options = [("Search Users", search_menu)]
        case 2:  # Member
            menu_options = []
        case -1:  # Guest
            menu_options = []

    menu_options.append(["Logout", home_menu])

    return prompt_options(*zip(*menu_options))


if __name__ == "__main__":
    # print((user_menu("Bob", ADMIN)))
    home_menu()

    # add_rows(
    #     BORROW_LOGS,
    #     ("id", "password", "username", "passsword"),
    #     (123123, "psasdsadas", "Ali", 3),
    # )
    # table = load_table("test")

    # filtered = filter_rows(table, where_equal(("username", "Bob")))
    # print_table(filtered)

    # update_rows(
    #     "test", ("username", "Jacky"), filter_func=where_equal(("username", "Jack"))
    # )

    # table = load_table("test")

    # print_table(table)
