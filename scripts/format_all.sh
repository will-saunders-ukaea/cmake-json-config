# This script formats the source files in NESO. This script should be ran from
# the root of the git repository. This script should be run as:
#
#   bash format_all.sh
#
# to format all source files. 

if [[ -f .cmake-format ]]; then
    # cmake-format
    cmake-format -c .cmake-format -i JSONConfig.cmake
    cmake-format -c .cmake-format -i examples/CMakeLists.txt
    # black
    find ./tests -iname \*.py | xargs black
    exit 0;
else
    echo "ERROR: The files .clang-format and .cmake-format do not exist. Please
       check this script is executed from the root directory of the git
       repository."
    exit 1;
fi

