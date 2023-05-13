echo "ratio is: 0.3884" >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 3 299 299 32 3 3 0 0 2 2 0 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 3 299 299 32 3 3 0 0 2 2 1 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 3 299 299 32 3 3 0 0 2 2 1 1 >> cov2dprofile.txt
echo "\n" >> cov2dprofile.txt


echo "ratio is: 0.5" >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 32 147 147 64 3 3 1 1 1 1 0 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 32 147 147 64 3 3 1 1 1 1 1 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 32 147 147 64 3 3 1 1 1 1 1 1 >> cov2dprofile.txt
echo "\n" >> cov2dprofile.txt


echo "ratio is: 4" >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 192 35 35 48 1 1 0 0 1 1 0 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 192 35 35 48 1 1 0 0 1 1 1 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 192 35 35 48 1 1 0 0 1 1 1 1 >> cov2dprofile.txt
echo "\n" >> cov2dprofile.txt


echo "ratio is: 0.6667" >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 64 35 35 96 3 3 1 1 1 1 0 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 64 35 35 96 3 3 1 1 1 1 1 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 64 35 35 96 3 3 1 1 1 1 1 1 >> cov2dprofile.txt
echo "\n" >> cov2dprofile.txt


echo "ratio is: 3.179" >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 288 35 35 384 3 3 0 0 2 2 0 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 288 35 35 384 3 3 0 0 2 2 1 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 288 35 35 384 3 3 0 0 2 2 1 1 >> cov2dprofile.txt
echo "\n" >> cov2dprofile.txt


echo "ratio is: 3" >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 192 35 35 64 1 1 0 0 1 1 0 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 192 35 35 64 1 1 0 0 1 1 1 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 192 35 35 64 1 1 0 0 1 1 1 1 >> cov2dprofile.txt
echo "\n" >> cov2dprofile.txt


echo "ratio is: 1" >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 192 35 35 192 1 1 0 0 1 1 0 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 192 35 35 192 1 1 0 0 1 1 1 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 192 35 35 192 1 1 0 0 1 1 1 1 >> cov2dprofile.txt
echo "\n" >> cov2dprofile.txt


echo "ratio is: 2" >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 192 35 35 96 1 1 0 0 1 1 0 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 192 35 35 96 1 1 0 0 1 1 1 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 192 35 35 96 1 1 0 0 1 1 1 1 >> cov2dprofile.txt
echo "\n" >> cov2dprofile.txt


echo "ratio is: 9" >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 192 35 35 16 1 1 0 0 1 1 0 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 192 35 35 16 1 1 0 0 1 1 1 0 >> cov2dprofile.txt
./main Conv2d_Forward 1 1024 192 35 35 16 1 1 0 0 1 1 1 1 >> cov2dprofile.txt
echo "\n" >> cov2dprofile.txt
