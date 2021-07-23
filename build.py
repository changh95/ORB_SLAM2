#!/usr/bin/env python3

import os
import sys


def main():
    print("Configuring and building Thirdparty/DBoW2 ...")

    os.chdir("./Thirdparty/DBoW2")
    os.system("sudo rm -rf build")
    os.system("mkdir build")
    os.chdir("./build")

    try:
        os.system("cmake .. -DCMAKE_BUILD_TYPE=Release")
        os.system("make -j")
        os.chdir("../../../")
    except Exception as e:
        sys.exit(e)

    print("Configuring and building Thirdparty/g2o ...")

    os.chdir("./Thirdparty/g2o")
    os.system("sudo rm -rf build")
    os.system("mkdir build")
    os.chdir("./build")

    try:
        os.system("cmake .. -DCMAKE_BUILD_TYPE=Release")
        os.system("make -j")
        os.chdir("../../../")
    except Exception as e:
        sys.exit(e)

    print("Uncompress vocabulary ...")

    os.chdir("./Vocabulary")
    os.system("tar -xf ORBvoc.txt.tar.gz")
    os.chdir("../")

    print("Configuring and building ORB_SLAM2 ...")
    os.system("sudo rm -rf build")
    os.system("mkdir build")
    os.chdir("./build")

    try:
        os.system("cmake .. -DCMAKE_BUILD_TYPE=Release")
        os.system("make -j")
        os.chdir("../../../")
    except Exception as e:
        sys.exit(e)


if __name__ == "__main__":
    main()
