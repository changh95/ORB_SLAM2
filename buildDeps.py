#!/usr/bin/env python3

import os
import sys
import argparse

pwd = os.path.dirname(os.path.abspath(__file__))


def main():
    # This script installs necessary C++ and Python packages to build and run this program.
    # The package configuration file is read from third_party/packages.yaml.

    parser = argparse.ArgumentParser(
        description='Script for project setup. It reads setup configuration from `package.yaml` file.')
    parser.add_argument('--d', action='store_true',
                        help='Enable building libraries in debug mode as well')
    parser.add_argument('--password', metavar='\b', type=str, default="",
                        help='Provide your Linux password to avoid manually typing in your password for every auto internal \'sudo\' command usage. This will leave traces of your password in your shell history. If you are concerned about security, do not use this option.')
    args = parser.parse_args()

    pw = Password(args.password)

    os.system(pw.sudo() + "apt -y install unzip wget git build-essential cmake gcc libpng-dev libtiff-dev libjpeg-dev zlib1g-dev freeglut3-dev libglew-dev")

    install_pangolin(pw, "0.6", args.d)
    install_eigen(pw, "3.3.9", args.d)
    install_opencv(pw, "3.4.15", args.d)


class Password:
    def __init__(self, password):
        self.data = password

    def redeem(self):
        if self.data != "":
            os.system("echo \"" + self.data +
                      "\" | sudo -S echo \"Password activated\"")

    def sudo(self):
        if self.data == "":
            return "sudo "

        return "echo " + self.data + " | sudo -S "


def install_pangolin(password, version_num, enable_debug):
    os.chdir(pwd)

    try:
        os.system(password.sudo() + "rm -rf ./Thirdparty/pangolin")

        os.makedirs("./Thirdparty/pangolin")
        os.chdir("./Thirdparty/pangolin")

        if os.system("wget -O " + "./pangolin.zip https://github.com/stevenlovegrove/Pangolin/archive/refs/tags/v" + version_num + ".zip") != 0:
            raise Exception("Pangolin: cloning failed")
        if os.system("unzip ./pangolin -d .") != 0:
            raise Exception

        os.makedirs("./build/Release", exist_ok=True)
        os.makedirs("./install/Release", exist_ok=True)
        os.chdir("./build/Release")

        exec_string = "cmake ../../Pangolin-" + version_num

        if os.system(exec_string + " -DCMAKE_INSTALL_PREFIX=../../install/Release") != 0:
            raise Exception("Pangolin: cmake configuration failed")

        if os.system("make -j") != 0:
            raise Exception("Pangolin: make failed")

        if os.system(password.sudo() + "make install") != 0:
            raise Exception("Pangolin: make install failed")

        if enable_debug:
            os.chdir("../../")
            os.makedirs("./build/Debug", exist_ok=True)
            os.makedirs("./install/Debug", exist_ok=True)
            os.chdir("./build/Debug")

            if os.system(exec_string + " -DCMAKE_INSTALL_PREFIX=../../install/Debug") != 0:
                raise Exception("Pangolin: cmake configuration failed")

            if os.system("make -j") != 0:
                raise Exception("Pangolin: make failed")

            if os.system(password.sudo() + "make install") != 0:
                raise Exception("Pangolin: make install failed")

        os.chdir("../../")
        os.system(password.sudo() + "rm -rf ./build")
        os.system(password.sudo() + "rm -rf Pangolin-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


def install_eigen(password, version_num, enable_debug):
    os.chdir(pwd)

    try:
        os.system(password.sudo() + "rm -rf ./Thirdparty/eigen")

        os.makedirs("./Thirdparty/eigen")
        os.chdir("./Thirdparty/eigen")

        if os.system("wget -O " + "./eigen.zip https://gitlab.com/libeigen/eigen/-/archive/" + version_num + "/eigen-" + version_num + ".zip") != 0:
            raise Exception("Eigen: pulling source code from gitlab failed")
        if os.system("unzip ./eigen.zip -d .") != 0:
            raise Exception

        os.makedirs("./build/Release", exist_ok=True)
        os.makedirs("./install/Release", exist_ok=True)
        os.chdir("./build/Release")

        exec_string = "cmake ../../eigen-" + version_num

        print(exec_string)

        if os.system(exec_string + " -DCMAKE_INSTALL_PREFIX=../../install/Release") != 0:
            raise Exception("Eigen: cmake configuration failed")

        if os.system("make -j") != 0:
            raise Exception("Eigen: make failed")

        if os.system(password.sudo() + "make install") != 0:
            raise Exception("Eigen: make install failed")

        if enable_debug:
            os.chdir("../../")
            os.makedirs("./build/Debug", exist_ok=True)
            os.makedirs("./install/Debug", exist_ok=True)
            os.chdir("./build/Debug")

            if os.system(exec_string + " -DCMAKE_INSTALL_PREFIX=../../install/Debug") != 0:
                raise Exception("Eigen: cmake configuration failed")

            if os.system("make -j") != 0:
                raise Exception("Eigen: make failed")

            if os.system(password.sudo() + "make install") != 0:
                raise Exception("Eigen: make install failed")

        os.chdir("../../")
        os.system(password.sudo() + "rm -rf ./build")
        os.system(password.sudo() + "rm -rf eigen-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


def install_opencv(password, version_num, enable_debug):
    # TODO(Hyunggi): Check if we need contrib?
    # TODO(Hyunggi): Check whether we use OpenCV 3 or 4.
    os.chdir(pwd)

    try:
        os.system(password.sudo() + "apt -y install unzip cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev")
        os.system(password.sudo() + "rm -rf ./Thirdparty/opencv")

        os.makedirs("./Thirdparty/opencv")
        os.chdir("./Thirdparty/opencv")

        if os.system("wget -O ./opencv.zip https://github.com/opencv/opencv/archive/" + version_num + ".zip") != 0:
            raise Exception("OpenCV: pulling source code from opencv failed")

        os.system("unzip ./opencv.zip -d .")

        os.makedirs("./build/Release", exist_ok=True)
        os.makedirs("./install/Release", exist_ok=True)
        os.chdir("./build/Release")

        exec_string = "cmake ../../opencv-" + version_num

        if os.system(exec_string + " -DCMAKE_INSTALL_PREFIX=../../install/Release") != 0:
            raise Exception("OpenCV: cmake configuration failed")

        if os.system("make -j4") != 0:
            raise Exception("OpenCV: make failed")

        if os.system(password.sudo() + "make install") != 0:
            raise Exception("OpenCV: make install failed")

        if enable_debug:
            os.chdir("../../")
            os.makedirs("./build/Debug", exist_ok=True)
            os.makedirs("./install/Debug", exist_ok=True)
            os.chdir("./build/Debug")

            if os.system(exec_string + " -DCMAKE_INSTALL_PREFIX=../../install/Debug") != 0:
                raise Exception("OpenCV: cmake configuration failed")

            if os.system("make -j4") != 0:
                raise Exception("OpenCV: make failed")

            if os.system(password.sudo() + "make install") != 0:
                raise Exception("OpenCV: make install failed")

        os.chdir("../../")
        os.system(password.sudo() + "rm -rf ./build")
        os.system(password.sudo() + "rm -rf opencv-" + version_num)
    except Exception as e:
        print("")
        sys.exit(e)


if __name__ == "__main__":
    main()
