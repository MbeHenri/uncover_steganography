import sys
from src.hccih.hide import hide
from src.hccih.extract import extract
from src.utils.loadandsave import load_txt, save_txt


def main(args):
    n = len(args)
    if n >= 1:
        if args[0] == "hide":
            if n >= 3:
                path_cover_image = args[1]
                secret_message = load_txt(args[2])
                hide(path_cover_image, secret_message)

                return None
        elif args[0] == "extract":
            if n >= 3:
                path_cover_image = args[1]
                secret_message = extract(path_cover_image)
                save_txt(args[2], secret_message)
                return None

    print("[USAGE]")
    print("python hccih.py <hide|extract>\n")
    print("[CMD] : hide")
    print("\tpython hccih.py hide <path_image> <path_message>")
    print("\t[EXEMPLE] python hccih.py hide ./test.jpg ./test_msg.txt")
    print("")
    print("[CMD] : extract")
    print("\tpython hccih.py extract <path_image> <path_extract_message>")
    print("\t[EXEMPLE] python hccih.py hide ./test.jpg ./test_extract_msg.txt")
    print("")


if __name__ == "__main__":
    main(sys.argv[1:])
