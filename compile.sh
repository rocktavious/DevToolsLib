rm -rf build
rmdir build
rm -rf DTL.egg-info
rmdir DTL.egg-info
rm -rf dist
rmdir dist

python register setup.py bdist bdist_rpm bdist_egg upload

rm -rf build
rmdir build
rm -rf DTL.egg-info
rmdir DTL.egg-info

echo "Press enter to finish"
read -n 1 -s