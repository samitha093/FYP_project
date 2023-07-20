#!/bin/bash
echo "😎 => deleting cash files ..."
find child_cart/api/templates -mindepth 1 -delete
rm *.spec
rm dist/*.bin
rm -rf build
echo "😎 => creating web app ..."
cd web_app
yarn build
cd ..
echo "😎 => copying web app to child cart ..."
cp -r web_app/dist/* child_cart/api/templates
echo "😎 => creating python binary file for parent..."
# pyinstaller --onefile --add-data "web_app/dist:web_app/dist" --name PARENT_CART_LINUX.bin P_main.py
pyinstaller --onefile --add-data  "child_cart/api/templates:child_cart/api/templates"  --name PARENT_CART_LINUX.bin P_main.py
echo "😎 =>creating python binary file for child..."
# pyinstaller --onefile --add-data "web_app/dist:web_app/dist" --name CHILD_CART_LINUX.bin C_main.py
pyinstaller --onefile --add-data "child_cart/api/templates:child_cart/api/templates"  --name CHILD_CART_LINUX.bin C_main.py
echo "😎 => Build is Sucessfully completed!"
