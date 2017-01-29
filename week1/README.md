# Fitters Happier Moresque

This assignment takes as input the song "Fitter, Happier" from Radiohead's OK Computer. It strips the first word of each line and replace it with the last word in the computers dictionary that contains that string as a prefix.
It's all done in bash.

First, to run a local version of the original song:

``` brew install espeak ```

then:

``` espeak -f fitter.txt -s 170 ```

To create "Fitters Happier Moresque" do:

``` bash script.sh ```

This will create a new file called new_fitter.txt

To play the new lyric do:

``` espeak -f new_fitter.txt -s 170 ```
