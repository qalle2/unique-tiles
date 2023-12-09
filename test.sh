clear
rm -f test-out/*.png
echo "xxx" > test-out/already-exists

echo "=== Converting 10 files ==="
python3 uniquetiles.py test-in/small-grayscale.png test-out/small-grayscale.png
python3 uniquetiles.py test-in/small-indexed.png   test-out/small-indexed.png
python3 uniquetiles.py test-in/small-rgb.png       test-out/small-rgb.png
python3 uniquetiles.py test-in/keen4.png           test-out/keen4-default.png
python3 uniquetiles.py test-in/keen4.png           test-out/keen4-10x10.png 10
python3 uniquetiles.py test-in/keen4.png           test-out/keen4-a.png 8 A
python3 uniquetiles.py test-in/keen4.png           test-out/keen4-ca,avg.png 8 CA
python3 uniquetiles.py test-in/keen4.png           test-out/keen4-p.png 8 P
python3 uniquetiles.py test-in/wolf3d.png          test-out/wolf3d-default.png 8
python3 uniquetiles.py test-in/wolf3d.png          test-out/wolf3d-a.png 8 A
echo

echo "=== These should cause 3 distinct errors ==="
python3 uniquetiles.py test-in/nonexistent    test-out/test1.png
python3 uniquetiles.py test-in/wolf3d.png     test-out/already-exists
python3 uniquetiles.py test-in/small-rgba.png test-out/small-rgba.png
echo

echo "=== Check test-out/*.png manually ==="
echo