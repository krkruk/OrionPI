import pathlib
import zipfile


def handle_exception(func):
    def _create_file_with_exception_handling(zip_name, list_of_file_names):
        try:
            func(zip_name, list_of_file_names)
        except RuntimeError:
            print("Could not create a zip file.")
        except FileExistsError:
            print("Strange things happened! File exists and cannot be overwritten.")
    return _create_file_with_exception_handling


def find_files_recursively_with_extension(start_directory="./", extension="*.py"):
    path = pathlib.Path(start_directory)
    return [str(file) for file in path.rglob(extension)]


@handle_exception
def create_zip_file(zip_name, list_of_file_names):
    with zipfile.ZipFile(zip_name, mode="w") as file:
        for zip_file in list_of_file_names:
            file.write(zip_file)


if __name__ == "__main__":
    zip_files = find_files_recursively_with_extension()
    create_zip_file("update.zip", zip_files)
    print("Exit CreateOrionPIUpdate app.")
