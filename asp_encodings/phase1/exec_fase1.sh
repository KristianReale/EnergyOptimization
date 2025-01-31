dirlist=(`ls input/*`)
numFiles=${#dirlist[@]}
inputStr=""

for (( i=0; i < $numFiles; i++ ))
do    
    inputStr="$inputStr input/input_$i.asp"
done
../../../../clingo-4.5.4-linux-x86_64/clingo --parallel-mode=8 encoding.asp params.asp $inputStr > output_optimum.txt
