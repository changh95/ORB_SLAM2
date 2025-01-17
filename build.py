#!/usr/bin/env python3

import os
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Script for building ORB-SLAM2')
    parser.add_argument('--d', action='store_true', default=False,
                        help='Build debug mode')
    parser.add_argument('--ros', action='store_true', default=False,
                        help='Enable building ROS nodes')
    parser.add_argument('--profiler', action='store_true', default=False,
                        help='Enable building with profiler')
    args = parser.parse_args()

    print("Configuring and building Thirdparty/DBoW2 ...")

    os.chdir("./Thirdparty/DBoW2")
    os.system("sudo rm -rf build")
    os.system("mkdir build")
    os.chdir("./build")

    try:
        if args.d:
            os.system("cmake -DCMAKE_BUILD_TYPE=Debug ..")
        else:
            os.system("cmake -DCMAKE_BUILD_TYPE=Release ..")
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
        if args.d:
            os.system("cmake -DCMAKE_BUILD_TYPE=Debug ..")
        else:
            os.system("cmake -DCMAKE_BUILD_TYPE=Release ..")
        os.system("make -j")
        os.chdir("../../../")
    except Exception as e:
        sys.exit(e)

    print("Uncompress vocabulary ...")

    os.chdir("./Vocabulary")
    os.system("tar -xf ORBvoc.txt.tar.gz")
    os.chdir("../")

    if args.ros:
        print("Configuring and building ORB-SLAM2 (ROS) ...")
    else:
        print("Configuring and building ORB-SLAM2 ...")

    os.system("sudo rm -rf build")
    os.system("mkdir build")
    os.chdir("./build")

    try:
        exec_string = "cmake "
        if args.profiler:
            exec_string += "-DWITH_PROFILER=ON "
        if args.ros:
            if args.d:
                exec_string += "-DROS_BUILD_TYPE=Debug .."
                os.system(exec_string)
            else:
                exec_string += "-DROS_BUILD_TYPE=Release .."

                os.system(exec_string)
        else:
            if args.d:
                exec_string += "-DCMAKE_BUILD_TYPE=Debug .."
                os.system(exec_string)
            else:
                exec_string += "-DCMAKE_BUILD_TYPE=Release .."
                os.system(exec_string)

        os.system("make -j")
        os.chdir("../../../")
    except Exception as e:
        sys.exit(e)


if __name__ == "__main__":
    main()
