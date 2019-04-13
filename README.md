# nla
Exercises of numerical algebra course

# jpeg.py
Performs jpeg transformation on an image by first normalizing image (puting values between [-127, 128]) then spliting it to 8x8 blocks(paddings done so dimensions are divisible to 8) and then performing DCT on blocks, after that we divide coefficients by quantization matrix and and we round values(this makes small values to change to zero).
Then we perform reverse jpeg transform to transformed image to get our image back, these two images are pretty much the same.
In this particular example by performin jpeg transformation on this image only 14% of final transformed image are not zero which shows jpeg is a great tool for compression.

# fft.py
All of code is steps needed in 2.8.2 exercise in the book.
First we see log image.
Then we see fft compression and distorsion for different thresholds.
In the end we plot compression over distorsion to get a good insight about relations between them.
