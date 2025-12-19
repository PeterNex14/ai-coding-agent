from functions.get_files_info import get_files_info

def main():
    directory = [".", "pkg", "/bin", "../"]
    for dir in directory:
        current_dir = "current" if dir == "." else dir

        print(f"Result for {current_dir} directory:\n{get_files_info("calculator", dir)}\n")

if __name__ == "__main__":
    main()