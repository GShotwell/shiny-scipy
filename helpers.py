from pathlib import Path


def include_shiny_folder(path):
    folder_path = Path(__name__).parent / path

    # Start with the header
    header = "```{shinylive-python}\n#| standalone: true\n#| components: [editor, viewer]\n#| layout: horizontal"
    print(header)

    # Print contents of app.py
    app_path = folder_path / "app.py"

    with open(app_path, "r") as app_file:
        app_contents = app_file.read()
        print(app_contents)

    exclude_list = ["__pycache__", "app.py"]

    file_paths = [
        path
        for path in folder_path.glob("**/*")
        if not any(exclude in path.parts for exclude in exclude_list)
    ]

    # Additional files need to start with ## file:
    for file_path in file_paths:
        if file_path.name != "app.py":
            print(f"\n## file: {file_path.name}")
            with open(file_path, "r") as file:
                file_contents = file.read()
                print(file_contents)

    # Finish with the closing tag
    print("```")
