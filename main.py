import os

# Role identifiers
GUEST = -1
ADMIN = 0
STAFF = 1
MEMBER = 2

# Table names
USERS_TABLE = "users"
BOOKS_TABLE = "books"

username = "Anonymous"
role = -1


# Helper functions
def exception_quit(e):
    print(f"Error: {e}")
    input("Press enter to quit...")
    exit()


def menu(func):
    def wrapper(*args, **kwargs):
        os.system("cls" if os.name == "nt" else "clear")
        return func(*args, **kwargs)

    return wrapper


def option_value(x):
    return lambda: x


@menu
def prompt_options(option_texts, option_functions, error_function=exception_quit):
    try:
        print(
            *[f"[{i}] {option_text}" for i, option_text in enumerate(option_texts, 1)],
            sep="\n",
        )

        return option_functions[int(input("Enter option: ") or 1) - 1]()
    except Exception as e:
        return error_function(e)


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

    return [first_column, raw_types] + data_rows


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
    print(load_table(table_name))
    print(types)

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
                raise ValueError(
                    f"Error in row: {value_row}, cell at column {i} is expected to be type {data_type}, found {type(cell).__name__}"
                )
            insert_row[index_map[i]] = cell

        data_rows.append(insert_row)

    dump_table(table_name, [first_row, types, *data_rows])


def update_rows(table_name, *column_value_pairs, filter_func=lambda x: True):
    table = load_table(table_name)

    column_idx_value_pairs = [
        (table[0].index(column), value) for column, value in column_value_pairs
    ]

    for row in table[2:]:
        if not filter_func(table[:2] + [row]):
            continue

        for column_idx, value in column_idx_value_pairs:
            row[column_idx] = value

    dump_table(table_name, table)


def filter_rows(table, filter_func):
    first_row, types, *data_rows = table

    return [first_row, types] + [
        data_row for data_row in data_rows if filter_func([first_row, types, data_row])
    ]


def where_equal(*column_value_pairs):
    def inner(table_row):
        for column, value in column_value_pairs:
            if get_column_by_name(table_row, column)[-1] != value:
                return False
        return True

    return inner


# User table functions
def create_user(username, password, role=MEMBER):
    users = load_table(USERS_TABLE)
    id = max(get_column_by_name(users, "id")[2:]) + 1  # Incremental id

    add_rows(
        USERS_TABLE,
        ("id", "username", "password", "role"),
        (id, username, password, role),
    )


# Admin features
@menu
def calculator():
    a = input("first number: ")
    b = input("second number: ")

    print("Sum is", a + b)
    input("Press enter to continue...")
    return calculator()


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
        [login_menu, user_menu("", ADMIN), exit],
    )


@menu
def login_menu():
    username = input("Username: ")
    password = input("Password: ")

    # TODO get user and handle incorrect credentials

    return user_menu("Bob", ADMIN)()


@menu
def user_menu():
    def menu_function():
        menu_options = []

        # TODO add options for each user
        match role:
            case 0:  # Admin
                menu_options = [["Caculator", calculator]]
            case 1:  # Staff
                menu_options = [["Search Users", search_menu]]
            case 2:  # Member
                menu_options = []
            case -1:  # Guest
                menu_options = []

        menu_options.append(["Logout", home_menu])

        return prompt_options(*zip(*menu_options))

    return menu_function


if __name__ == "__main__":
    # print((user_menu("Bob", ADMIN)))
    # home_menu()

    # add_rows(
    #     "test",
    #     ("id", "password", "username", "passsword"),
    #     (123123, "psasdsadas", "Ali", 3),
    # )
    table = load_table("test")
    # filtered = filter_rows(table, where_equal(("username", "Bob")))
    print_table(table)

    update_rows(
        "test", ("username", "Jacky"), filter_func=where_equal(("username", "Jack"))
    )

    table = load_table("test")

    print_table(table)
