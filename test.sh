clear
rm -f test-out/*.png
echo "xxx" > test-out/already-exists

echo "=== Converting 10 files, one verbosely ==="
python3 uniquetiles.py test-in/small-grayscale.png test-out/small-grayscale.png
python3 uniquetiles.py test-in/small-indexed.png   test-out/small-indexed.png
python3 uniquetiles.py test-in/small-rgb.png       test-out/small-rgb.png
python3 uniquetiles.py test-in/keen4.png           test-out/keen4-default.png
python3 uniquetiles.py test-in/keen4.png           test-out/keen4-a.png         --tileorder a
python3 uniquetiles.py test-in/keen4.png           test-out/keen4-ca,avg.png    --tileorder ca
python3 uniquetiles.py test-in/keen4.png           test-out/keen4-p.png         --tileorder p
python3 uniquetiles.py test-in/wolf3d.png          test-out/wolf3d-default.png  --verbose
python3 uniquetiles.py test-in/wolf3d.png          test-out/wolf3d-10x5-a.png   --tilewidth 10 --tileheight 5 --tileorder a
python3 uniquetiles.py test-in/wolf3d.png          test-out/wolf3d-a.png        --tileorder a
echo

echo "=== These should cause 7 distinct errors ==="
python3 uniquetiles.py test-in/wolf3d.png     test-out/test1.png --tilewidth 0
python3 uniquetiles.py test-in/nonexistent    test-out/test2.png
python3 uniquetiles.py test-in/wolf3d.png     test-out/already-exists
python3 uniquetiles.py test-in/wolf3d.png     test-out/nonexistent/
python3 uniquetiles.py test-in/small-rgba.png test-out/small-rgba.png
python3 uniquetiles.py test-in/wolf3d.png     test-out/test3.png --tilewidth 7
python3 uniquetiles.py test-in/wolf3d.png     test-out/test4.png --tileheight 7
echo

echo "=== Check test-out/*.png manually ==="
echo
