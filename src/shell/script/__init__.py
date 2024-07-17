import os


def list_modules():
    package_path = os.path.dirname(__file__)
    module_list = []

    for root, dirs, files in os.walk(package_path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_name = os.path.splitext(file)[0]
                relative_path = os.path.relpath(root, package_path).replace(os.sep, '.')
                if relative_path == ".":
                    module_list.append(module_name)
                else:
                    module_list.append(f"{relative_path}.{module_name}")

    return module_list


class ReturnObject:
    def __init__(self, err, val):
        self.err = err
        self.val = val


__all__ = list_modules()
