# use this to convert all ui files to py files using `pyside6-uic`
ui_folder=./resources
py_folder=./view
export py_folder

generate_py() {
    ui_file=$1
    output=${py_folder}/`ui_file=$ui_file; m=${ui_file/.ui/_ui.py}; echo ${m##*/}`
    echo "> pyside6-uic $ui_file > $output"
    pyside6-uic $ui_file > $output
}
export -f generate_py

find $ui_folder -name *.ui -type f -exec bash -c 'generate_py "$1"' bash {} \;