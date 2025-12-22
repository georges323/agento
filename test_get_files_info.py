from functions.get_files_info import get_files_info

def test():
    print(f"Result for current directory:")
    result = get_files_info("calculator", ".")
    print(result)
    print("")

    print(f"Result for 'pkg' directory:")
    result = get_files_info("calculator", "pkg")
    print(result)
    print("")

    print(f"Result for '/bin' directory:")
    result = get_files_info("calculator", "/bin")
    print(result)
    print("")

    print(f"Result for '../' directory:")
    result = get_files_info("calculator", "../")
    print(result)
    print("")

if __name__ == "__main__":
    test()
