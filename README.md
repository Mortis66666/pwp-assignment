# PWP Assignment

## Prerequisites

- [VsCode](https://code.visualstudio.com/download)
- [Git](https://git-scm.com/downloads)
- [Github account](https://github.com/join)

## Setup guide

1. Open windows file explorer, and navigate to the folder where you want to store the project. Copy the path from the address bar.
![alt text](screenshots/fileexp.png)

2. Open terminal with `Win + R`, type `cmd` and hit enter.  
3. In the terminal, type `cd` followed by the path you copied earlier. Hit enter.

   ```bash
   cd C:\path\to\your\folder
   ```

4. Clone the repository by running the following command:

   ```bash
    git clone https://github.com/Mortis66666/pwp-assignment.git
    ```

5. Open project in VsCode by running:

   ```bash
   code pwp-assignment
    ```

## Edit access

- Send me your github username
- Accept the invite to the repository in email

## Project structure

- `main.py` - Main program file
- `users.txt`, `books.txt`, `borrow_logs.txt` - Data files

## Git guide

### What is Git?

Git is a version control system that helps you track changes to your code over time. It allows multiple people to work on the same project simultaneously without overwriting each other's changes.

### What is GitHub?

GitHub is a web-based platform that hosts Git repositories. It provides a collaborative environment where developers can share code, track issues, and manage projects.

### Syncing workflow

1. Locate the Source Control icon on the left sidebar of VsCode (it looks like a branch with a dot at the end) and click on it. Alternatively, you can use the keyboard shortcut `Ctrl + Shift + G, G` to open the Source Control panel directly. This panel allows you to manage your Git repositories, view changes, and perform various version control operations.

2. Before making any changes, it's important to ensure that your local repository is up to date with the latest changes from the remote repository. To do this, click on the "..." (More Actions) button at the top of the Source Control panel and select "Pull" from the dropdown menu. This action will fetch and merge any changes from the remote repository into your local copy.

3. After pulling the latest changes, you can proceed to make your edits to the code files as needed.

4. Once you've made your changes, return to the Source Control panel. You will see a list of files that have been modified. Review the changes to ensure everything is as expected.

5. To stage your changes for commit, click on the "+" icon next to each file you want to include. This action prepares the files to be committed to the repository.

6. After staging your changes, you'll need to provide a commit message that describes the changes you've made. This message helps others (and yourself) understand the purpose of the changes. Type your commit message in the input box at the top of the Source Control panel.

7. Once you've entered your commit message, click on the commit button (✓ Commit) to commit the changes to your local repository.

8. Finally, to share your changes with others, you'll need to push your commits to the remote repository. Click on the "..." (More Actions) button again and select "Push" from the dropdown menu. This action will upload your committed changes to the remote repository on GitHub.

#### Learn more

[Official VsCode Guide](https://code.visualstudio.com/docs/editor/versioncontrol#_git-support)

## Documentation: main.py

This section documents the overall structure and each function in main.py so you can understand behavior and extend the program.

High-level structure

- Constants and globals: role identifiers (GUEST, ADMIN, STAFF, MEMBER), table name constants (USERS_TABLE, BOOKS_TABLE, BORROW_LOGS) and runtime globals (username, role, log_message, history).
- Helper utilities: input wrappers, menu decorators, logging, and navigation helpers used by all menus.
- File/table utilities: simple CSV-like file loader/dumper and basic table operations (add, delete, update, filter).
- Domain helpers: user/book creation helpers.
- Menus and features: functions decorated with @menu to build interactive CLI menus (home_menu, login_menu, user_menu, admin/staff/member menus and submenus).

Globals

- GUEST, ADMIN, STAFF, MEMBER: role integer constants.
- roles: list for printing role names by index.
- USERS_TABLE, BOOKS_TABLE, BORROW_LOGS: filenames without extension ('.txt' used by table functions).
- username, role: current session identity and role.
- log_message: message passed between menus.
- history: stack of menu functions for "back" navigation.

Helper functions

- exception_quit(e)
  - Prints error, waits for Enter and exits. Used as default error handler for prompts.
  - Args: e (Exception or any)
  - Return: exits program.

- clear_screen()
  - Clears terminal screen (Windows or Unix).

- menu(func)
  - Decorator for menu functions. Clears screen, appends the function to history, prints any pending log_message, then calls the wrapped function.
  - Usage: annotate functions that represent interactive screens.

- option_value(x)
  - Returns a zero-arg lambda that returns the value x. Useful to have prompt_options return values rather than call functions.

- prompt_yes_no(prompt)
  - Displays a Y/N prompt and returns True for 'y' (case-insensitive), False otherwise.

- prompt_options(option_texts, option_functions=None, error_function=exception_quit)
  - Display enumerated options and run the selected function or return the selected index (when no functions provided).
  - Args:
    - option_texts: list[str]
    - option_functions: list[callable] or None
    - error_function: callable invoked on invalid input (default exception_quit)
  - Returns: result of the chosen function (or index/value when using option_value)

- paginator(option_texts, option_functions, page_index=0, page_title="", max_per_page=6, cancel_function=None, error_function=exception_quit)
  - Paginate long option lists and provide "Previous", "Next", "Back" and optional "Cancel".
  - Handles page navigation by recursively calling itself.
  - Returns the chosen option function's result.

- prompt_inputs(*prompts, types=None)
  - Collect multiple inputs with optional type casts.
  - Returns list of typed values.

- back(skip_repeat=True)
  - Pop the last menu from history and return to the previous menu.
  - skip_repeat avoids repeating the same menu if it was appended twice.
  - Raises if history is empty.

- log_and_redirect(func, message)
  - Helper that prints a message (via print_log) and then calls func. Useful as an option target to both log and redirect.

- print_log(message)
  - Store message in global log_message to be shown by the next menu.

File / table functions (simple CSV-like file format)

- load_table(table_name)
  - Reads table_name.txt. Expects first row column names, second row Python type names as strings (e.g. "int","str"), followed by data rows.
  - Returns a list-like table: [first_column, raw_types, *data_rows] where raw_types are strings and data rows are typed.

- dump_table(table_name, table)
  - Writes the table back to table_name.txt using comma-separated values.

- get_column(table, index)
  - Return values at index for every row in table.

- get_column_by_name(table, column)
  - Lookup column index from first row and return that column.

- print_divider(column_sizes) / print_row(row, column_sizes) / print_table(table, padding=0)
  - Utilities to print a simple ASCII table of the in-memory table data.

- add_rows(table_name, columns, *value_rows)
  - Add rows to a table; validates columns match table first row, converts values to expected types where necessary.
  - columns is a tuple of column names matching the order of the provided value rows.
  - Raises on type mismatch that cannot be converted.

- delete_rows(table_name, filter_func=lambda x: True)
  - Remove rows matching filter_func. filter_func receives [first_row, types, row].

- update_rows(table_name, *column_value_pairs, filter_func=lambda x: True)
  - Update rows matching filter_func with provided (column, value) pairs. Attempts type conversion.

- filter_rows(table, filter_func)
  - Return a new table containing only rows where filter_func([first_row, types, row]) is True.

- filter_columns(table, columns)
  - Select and return only the requested columns (list of column names).

Predicate helpers (composable where- functions)

- where_equal(*column_value_pairs)
  - Returns lambda(table_row) that checks equality for specified (column, value) pairs against the last row value.

- where_greater(*column_value_pairs)
  - Returns lambda(table_row) that checks > for given (column, value) pairs.

- where_not(func), where_and(*funcs), where_or(*funcs)
  - Logical combinators for predicates used by filter_rows / update / delete helpers.

- is_empty(table)
  - True if table has only header and types rows (no data).

Domain helpers

- create_user(username, password, role=MEMBER)
  - Load users table, compute new incremental id from existing ids, add user row.

- create_book(title, author, isbn, quantity=1)
  - Load books table, compute new id and add a book row.

Menus and features (interactive)

- book_management(), add_book(), remove_book(), modify_book()
  - Admin book-management flows. Use menu, paginator, prompt_inputs, add/update/delete functions to modify BOOKS_TABLE.

- user_management(), add_user(), remove_user()
  - Admin user-management flows. add_user prompts for role, username, password and calls create_user.

- search_menu()
  - Placeholder for staff search functionality. Currently TODO.

- home_menu()
  - Entry menu offering Login, Continue as guest, Quit Program.

- login_menu()
  - Prompts credentials, validates against USERS_TABLE using filter_rows and where_equal. On success sets global username and role and logs a welcome message.

- user_menu()
  - Main menu after login. Uses Python match on role to present role-specific options. Admins get book and user management options. Staff and member menus are placeholders to be extended.

Extending and adding new features (guidelines)

1. Plan the feature
   - Decide which role(s) should access it (ADMIN, STAFF, MEMBER, GUEST).
   - Define required table changes (new columns or new files) and interactions (create, read, update, delete).

2. Add data schema (if needed)
   - Open or create a .txt table file in the same simple format:
     - Row 1: comma-separated column names (e.g. id,title,author,isbn,quantity)
     - Row 2: comma-separated Python type names as strings (e.g. "int","str","str","int")
     - Following rows: data values.
   - Use existing helpers (load_table, dump_table) to read/write.

3. Implement domain helpers
   - Add pure functions like create_xxx(...) that call add_rows with correct columns and types.
   - Follow pattern in create_user/create_book to compute incremental id and validate inputs.

4. Implement CLI handlers
   - Add a @menu-decorated function for the new screen and any sub-screens.
   - Reuse prompt_inputs, prompt_options, paginator, prompt_yes_no for consistent UI and validation.
   - Use print_log to pass user-friendly messages between screens.
   - For actions that should redirect with a log message, use log_and_redirect.

5. Wire to user_menu
   - In user_menu, add an option for the role(s) to access the new feature:
     - Example: for Staff add ("My Feature", my_feature_menu) in the menu_options list inside the role match-case.
   - Ensure menu_options is a list of (label, callable) and append ["Logout", home_menu] at the end.

6. Data validation and types
   - Keep consistent use of the second header row (type names) so add_rows and update_rows can validate and convert.
   - When accepting numeric inputs from prompt_inputs or input(), validate or cast using try/except and use print_log to notify the user of invalid entries.

7. Back navigation and history
   - Always decorate interactive screens with @menu so history is managed and back() works.
   - If you need to return a value from a selection, use option_value to create a callable that returns the value.

8. Error handling and testing
   - Provide user-friendly error messages using print_log and redirect back to a safe menu.
   - Test end-to-end: create test users/books rows in the corresponding txt files and run flows covering add/update/delete.

Example: Add "My Books" feature for MEMBER

- Add a menu function:

  - ```py
    @menu
    def my_books():
      books = load_table(BOOKS_TABLE)
      # filter borrowed/available as needed and use paginator or print_table
    ```

- Wire to user_menu under case 2 (Member):
  - menu_options = [("My Books", my_books), ...existing member options...]

Notes and tips

- All interactive screens should be decorated with @menu to get consistent screen clears, logs, and history.
- Table files are simple CSV-like; keep second row as valid Python type names ("int","str").
- When designing new features, prefer composing existing helpers instead of reimplementing file I/O or pagination.

This documentation should give enough detail to read, modify, or extend main.py and to add role-based menu entries with minimal friction.

## Detailed helper usage (with Python examples)

This section provides explicit usage examples and detailed parameter/return descriptions for each helper in main.py. All code samples are Python and wrapped with ```py fences so you can copy/paste.

UI helpers

- exception_quit(e)
  - Purpose: Default error handler used by prompt functions. Prints an error message, waits for Enter, then exits.
  - Args: e (any) — typically an Exception
  - Returns: exits the program; does not return normally.
  - Example:

  ```py
  # Example: use as an error callback
  try:
      int("not-a-number")
  except Exception as e:
      exception_quit(e)  # prints error and exits
  ```

- clear_screen()
  - Purpose: Cross-platform clear terminal screen (Windows: cls, others: clear).
  - Args: none
  - Returns: None
  - Example:

  ```py
  clear_screen()
  print("Screen cleared")
  ```

- menu(func)  (decorator)
  - Purpose: Wrap menu functions to auto-clear screen, append to history, and show pending log_message before running the menu.
  - Usage: put @menu above functions that produce an interactive screen (no parameters).
  - Important: The wrapped function should accept no arguments; state is passed through globals (username, role, log_message).
  - Example:

  ```py
  @menu
  def example_menu():
      print("This is a menu screen")
      input("Press Enter to continue")
  ```

- option_value(x)
  - Purpose: Turn a static return value into a no-arg callable usable in prompt_options or paginator.
  - Args: x (any)
  - Returns: callable that when called returns x
  - Example:

  ```py
  # Using prompt_options to select between values
  choice = prompt_options(["One", "Two"], [option_value(1), option_value(2)])
  # choice will be 1 or 2 depending on the selection
  ```

- prompt_yes_no(prompt)
  - Purpose: Ask a yes/no question and return boolean.
  - Args: prompt (str)
  - Returns: True if user enters 'y' or 'Y', otherwise False
  - Example:

  ```py
  if prompt_yes_no("Delete item?"):
      print("Deleted")
  else:
      print("Canceled")
  ```

- prompt_options(option_texts, option_functions=None, error_function=exception_quit)
  - Purpose: Present enumerated options to the user and either return a chosen index/value or call the corresponding function.
  - Args:
    - option_texts: list[str] — texts to display (will be enumerated starting from 1)
    - option_functions: list[callable] or None — callables corresponding to each option; if None, prompt_options returns the index (0-based) by default using option_value wrappers created internally
    - error_function: callable — called on invalid input (default exception_quit)
  - Returns: result of chosen function or chosen value/index (depending on option_functions)
  - Notes: Input defaults to option 1 if user presses enter.
  - Example (call functions):

  ```py
  def a(): return "A selected"
  def b(): return "B selected"
  result = prompt_options(["Choose A", "Choose B"], [a, b])
  print(result)
  ```

  - Example (return index/value):

  ```py
  # When you want the chosen index/value:
  idx = prompt_options(["Red", "Blue"])  # returns 0 for Red, 1 for Blue, etc.
  ```

- paginator(option_texts, option_functions, page_index=0, page_title="", max_per_page=6, cancel_function=None, error_function=exception_quit)
  - Purpose: Paginate long lists of options with built-in "Previous", "Next", and "Back" navigation.
  - Args:
    - option_texts: list[str]
    - option_functions: list[callable] — same length as option_texts
    - page_index: int — which page to start from
    - page_title: str — printed at top of page
    - max_per_page: int — how many options per page
    - cancel_function: callable or None — optional "Cancel" action appended to last page
    - error_function: callable — handles invalid input
  - Returns: value returned by the selected option's callable
  - Example:

  ```py
  options = [f"Item {i}" for i in range(30)]
  functions = [option_value(i) for i in range(30)]
  choice = paginator(options, functions, page_title="Select an item", max_per_page=8)
  print("You chose index:", choice)
  ```

- prompt_inputs(*prompts, types=None)
  - Purpose: Collect multiple inputs and optionally cast types.
  - Args:
    - prompts: variable number of prompt strings
    - types: list[type] or None — types to cast each input to (defaults to str for all)
  - Returns: list of typed values (in same order)
  - Example:
  
  ```py
  name, age = prompt_inputs("Name", "Age", types=[str, int])
  print(name, age, type(age))  # age is int
  ```

- back(skip_repeat=True)
  - Purpose: Navigate back to previous menu using the history stack maintained by @menu.
  - Args:
    - skip_repeat: bool — if True, pop duplicate consecutive entries to avoid repeating same screen
  - Returns: calls the previous menu function (decorated) and returns its result
  - Example:

  ```py
  # Usually called as an option or after an action
  return back()  # returns to the previous menu
  ```

- log_and_redirect(func, message)
  - Purpose: Helper that sets a log message and then calls a function (e.g., back). Useful as an option target.
  - Args:
    - func: callable — to call after logging
    - message: str — message to show on next screen
  - Returns: a zero-arg callable (the inner) which when called logs then calls func
  - Example:

  ```py
  # Use as option to both log and go back
  some_option_functions = [log_and_redirect(back, "Operation cancelled")]
  ```

- print_log(message)
  - Purpose: Store a message in global log_message so the next @menu-decorated screen shows it.
  - Args:
    - message: str
  - Returns: None
  - Example:

  ```py
  print_log("User created successfully")
  return back()
  ```

Table / file helpers

- load_table(table_name)
  - Purpose: Read a simple CSV-like txt file named "<table_name>.txt".
  - Expected file format:
    - Line 1: comma-separated column names (e.g. id,username,password,role)
    - Line 2: comma-separated Python type names as strings (e.g. "int","str","str","int")
    - Remaining lines: data rows matching columns and types
  - Returns: list representing the table: [first_row (list of column names), raw_types (list of type names as strings), *data_rows (typed lists)]
  - Example:

  ```py
  table = load_table("users")
  # table[0] is the header: ["id","username","password","role"]
  # table[1] is raw types: ['int','str','str','int']
  # rows follow as typed values
  ```

- dump_table(table_name, table)
  - Purpose: Write in-memory table to "<table_name>.txt" using comma-separated values.
  - Args:
    - table_name: str
    - table: same format as returned by load_table
  - Example:

  ```py
  dump_table("users", table)
  ```

- get_column(table, index)
  - Purpose: Return a column by index from a table.
  - Args:
    - table: table returned by load_table or filtered table
    - index: int
  - Returns: list of values (header, types, and each data cell at index)
  - Example:

  ```py
  usernames = get_column(table, 1)  # includes header and types and data
  # More commonly:
  usernames_data = get_column(table, 1)[2:]  # get only data rows
  ```

- get_column_by_name(table, column)
  - Purpose: Return column data by name (uses header to lookup index).
  - Args:
    - table: table
    - column: str
  - Returns: list of column values (including header and type rows)
  - Example:

  ```py
  ids = get_column_by_name(table, "id")[2:]  # only data values
  ```

- print_divider, print_row, print_table(table, padding=0)
  - Purpose: Simple ASCII table printing utilities for quick debugging and user display.
  - Example:

  ```py
  print_table(load_table("books"))
  ```

- add_rows(table_name, columns, *value_rows)
  - Purpose: Add one or more rows to a table while validating column names and types.
  - Args:
    - table_name: str
    - columns: tuple/list of column names (order corresponds to values in each value_row)
    - value_rows: one or more tuples/lists of values (each value_row aligns with columns)
  - Behavior: Internally creates an insert_row of default values then maps provided values into correct indices; tries to convert types using eval on raw type strings; raises descriptive errors on mismatch.
  - Example:

  ```py
  # Add a user
  add_rows("users", ("id", "username", "password", "role"), (10, "alice", "secret", 2))
  # Add multiple books
  add_rows("books", ("id","title","author","isbn","quantity"),
           (101,"Title A","Author A",12345,3),
           (102,"Title B","Author B",67890,1))
  ```

- delete_rows(table_name, filter_func=lambda x: True)
  - Purpose: Delete rows that match filter_func. filter_func receives a table-row context [header, types, row] and should return True to delete.
  - Example:

  ```py
  # Delete user with id 10
  delete_rows("users", filter_func=where_equal(("id", 10)))
  ```

- update_rows(table_name, *column_value_pairs, filter_func=lambda x: True)
  - Purpose: Update matching rows with provided (column, value) pairs. Converts values to expected types when possible.
  - Args:
    - column_value_pairs: variable length tuples like ("username", "newname")
    - filter_func: predicate to select rows (receives [header, types, row])
  - Example:

  ```py
  # Set quantity to 5 for book with id 101
  update_rows("books", ("quantity", 5), filter_func=where_equal(("id", 101)))
  ```

- filter_rows(table, filter_func)
  - Purpose: Return a new table containing only rows where filter_func([header, types, row]) is True.
  - Example:

  ```py
  books = load_table("books")
  expensive = filter_rows(books, where_greater(("quantity", 2)))  # example predicate
  print_table(expensive)
  ```

- filter_columns(table, columns)
  - Purpose: Return only selected columns from a table.
  - Args:
    - columns: list of column names to select (must exist in header)
  - Example:
  
  ```py
  tbl = load_table("users")
  small = filter_columns(tbl, ["id","username"])
  print_table(small)
  ```

Predicate helpers (how to build filters)

- where_equal(*column_value_pairs)
  - Usage: where_equal(("username","bob"), ("role", 1))
  - Returns: a predicate function that accepts [header, types, row] and checks equality against the last item of the specified column.
  - Example:

  ```py
  delete_rows("users", where_equal(("username", "bob")))
  ```

- where_greater(*column_value_pairs)
  - Purpose: Return predicate that checks ">" for the given column/value pair.
  - Example:

  ```py
  big_stock = filter_rows(load_table("books"), where_greater(("quantity", 5)))
  ```

- where_not(func), where_and(*funcs), where_or(*funcs)
  - Purpose: Logical combinators to negate or combine predicates.
  - Example:

  ```py
  predicate = where_and(where_greater(("quantity", 0)), where_not(where_equal(("title","Out of Print"))))
  results = filter_rows(load_table("books"), predicate)
  ```

- is_empty(table)
  - Purpose: Return True when a table contains only header and types (no data rows).
  - Example:

  ```py
  if is_empty(load_table("users")):
      print("No users defined")
  ```

Practical recipes / idioms

- Creating a new user (pattern used in create_user)

  ```py
  users = load_table("users")
  next_id = max(get_column_by_name(users, "id")[2:]) + 1
  add_rows("users", ("id","username","password","role"), (next_id, "new", "pw", 2))
  ```

- Searching and modifying a row (pattern used in modify_book)

  ```py
  books = load_table("books")
  # find the first book with title "Foo"
  found = filter_rows(books, where_equal(("title", "Foo")))
  if not is_empty(found):
      book_id = get_column_by_name(found, "id")[-1]
      update_rows("books", ("quantity", 10), filter_func=where_equal(("id", book_id)))
  ```

- Safely prompting numeric input with validation

  ```py
  raw = input("Enter ISBN: ")
  if not raw.isdigit():
      print_log("ISBN should be a number")
      return add_book()  # typical pattern in menus to show message and re-open screen
  isbn = int(raw)
  ```

Extending features for roles (quick checklist)

1. Add/modify table schema if needed (edit .txt file header and types).
2. Implement domain helper(s) that perform table operations.
3. Implement @menu-annotated CLI handlers and submenus, reusing prompt_inputs, prompt_options, paginator.
4. Wire handlers into user_menu under the appropriate role case.
5. Test flows and use print_log/log_and_redirect for user feedback.

This section aims to give copy/paste-ready examples and precise function descriptions so you can extend main.py confidently. If you want, I can also generate small sample table files (users.txt, books.txt) containing headers and types to use with these examples.
