import sys
from src.cis_pdir.hide import hide
from src.cis_pdir.extract import extract
from src.cis_pdir.build_indexdb import construct_indexfiles


def main(args):
    n = len(args)
    if n >= 1:
        if args[0] == "indexfiles":
            if n >= 2:
                path_imgs = args[1]
                return construct_indexfiles(input_path_images=path_imgs)

        elif args[0] == "hide":
            if n >= 3:
                path_secret_image = args[1]
                path_send_imgs = args[2]
                return hide(path_secret_image, path_imgs=path_send_imgs)

        elif args[0] == "extract":
            if n >= 3:
                path_send_image = args[1]
                path_extract_img = args[2]
                return extract(path_imgs=path_send_image).save(path_extract_img)

    print("[USAGE]")
    print("python cis_pdir.py <indexfiles|hide|extract>\n")
    print("[CMD] : indexfiles")
    print("\tpython cis_pdir.py indexfiles <path_images>")
    print("\t[EXEMPLE] python cis_pdir.py indexfiles ./images")
    print("")
    print("[CMD] : hide")
    print("\tpython cis_pdir.py hide <path_secret_image> <path_send_imgs>")
    print("\t[EXEMPLE] python cis_pdir.py hide ./test.jpg ./send_imgs")
    print("")
    print("[CMD] : extract")
    print("\tpython cis_pdir.py extract <path_send_image> <path_extract_img>")
    print("\t[EXEMPLE] python cis_pdir.py extract ./send_imgs ./test_extract_msg.txt")
    print("")


if __name__ == "__main__":
    main(sys.argv[1:])
