rm -rf build
rmdir build
rm -rf DevToolsLib.egg-info
rmdir DevToolsLib.egg-info
rm -rf dist
rmdir dist

python setup.py bdist
python setup.py bdist_rpm
python setup.py bdist_egg

rm -rf build
rmdir build
rm -rf DevToolsLib.egg-info
rmdir DevToolsLib.egg-info

echo "Press enter to finish"
read -n 1 -s