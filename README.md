### 2024-11-27T08:57:22-08:00
Try using --duration 200 for mp4 to not skip frames?

### 2024-07-27T12:03:49-07:00
Looping is now optional

default is to not loop:
./create_gif.py /path/to/your/image_directory output.gif --duration 500 --max_size 500

specity --loop to loop
./create_gif.py /path/to/your/image_directory output.gif --duration 500 --max_size 500 --loop

#### Make a movie too
python3 ./create_gif.py /path/to/your/image_directory output.gif --output_mp4 output.mp4 --duration 50 --max_size 500 --skip 10

### Skip the first 10
python3 ./create_gif.py /path/to/your/image_directory output.gif --duration 50 --max_size 500 --skip 10


### Turn a directory of images into an nimated GIF

./create_gif.py /path/to/your/image_directory output.gif --duration 500 --max_size 500
