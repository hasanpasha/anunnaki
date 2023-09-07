import zipfile

def extract_file(zipfile_path, dest) -> bool:
    with zipfile.ZipFile(zipfile_path) as zfile:
        zfile.extractall(dest)
        return True
    
    return False