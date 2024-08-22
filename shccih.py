import sys
from src.utils.pallier import generate_keypair
from src.shccih.hide import hide
from src.shccih.extract import extract
from src.utils.loadandsave import load_txt, save_txt, save2json


def main(args):
    n = len(args)
    if n >= 1:
        if args[0] == "genkeys":
            public_key, private_key = generate_keypair(16)
            
            save2json(public_key, "./pubk.json")
            save2json(private_key, "./prik.json")
            
            return None
        elif args[0] == "hide":
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
    print("python shccih.py <hide|extract>\n")
    print("[CMD] : genkeys")
    print("\tpython shccih.py genkeys")
    print("\t[EXEMPLE] python shccih.py genkeys")
    print("")
    print("[CMD] : hide")
    print("\tpython shccih.py hide <path_image> <path_message>")
    print("\t[EXEMPLE] python shccih.py hide ./test.jpg ./test_msg.txt")
    print("")
    print("[CMD] : extract")
    print("\tpython shccih.py extract <path_image> <path_extract_message>")
    print("\t[EXEMPLE] python shccih.py extract ./test.jpg ./test_extract_msg.txt")
    print("")


if __name__ == "__main__":
    main(sys.argv[1:])
