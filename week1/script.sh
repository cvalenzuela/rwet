#!bin/bash

# Assignment #1 RWET
# New Fitter Happier
# By Cristóbal Valenzuela

# Get the first letter of each line
while read line
do
  echo  "$line" | cut -d " " -f 1 >> temp1.txt
done < fitter.txt # Here the input file

#Replace the first letter with a new word from the dictionary.
while read word && [[ $word != end ]]
do if look "$word" > /dev/null
  echo "$word"
  then look "$word" | tail -1 >> temp2.txt
  fi
done < temp1.txt # Input file to replace words from

# Erase the last word of the dictionary "Zyzzogeton" we are getting.
cat temp2.txt | sed 's/^Zyzzogeton//' >> new_fitter.txt

# Remove temp file created
rm temp1.txt
rm temp2.txt

exit 0

# Read the original song
# espeak -f fitter.txt -s 170
