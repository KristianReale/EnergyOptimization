#!/bin/bash
dirlist=('ls Facts/H*')
numFiles=${#dirlist[@]}

# rm -r Results
if [ -d Results ]; then
    echo "Directory Results already exists. Please remove it"
else

#for (( i=1; i <= 20; i++ ))
for (( i=1; i <= 1; i++ ))
do    
    initChargeFile="Facts/initCharge.asp"

    for filepath in Facts/*_KWh.asp
    #for filepath in Facts/2023-08-21_KWh.asp
    #for (( j=1; j <= 3; j++ ))  
    do    
      echo "${initChargeFile}"
      house="cubo"
      factsFile="$filepath"  # Variabile con percorso completo
	date=${factsFile##*/}
	date="${date%.*}"
        echo "Executing ${date}"  
        mkdir -p "Results/${house}"
        clingcon ../../encoding_article_con2.asp params_article.asp maxChargeKWh.asp "${factsFile}" "${initChargeFile}" $1 --parallel-mode=8 --quiet=1 --time-limit=1 --outf=1 > "Results/${house}/output_${house}_${date}.txt" 
	sed -e 's/ANSWER/%ANSWER/g' "Results/${house}/output_${house}_${date}.txt" > "Results/${house}/tmp.txt"
	sed -e 's/OPTIMUM/%OPTIMUM/g' "Results/${house}/tmp.txt" > "Results/${house}/tmp_2.txt"

	sed -E 's/\)[[:space:]]*=[[:space:]]*([+-]?[0-9]+)/,\1)/g' "Results/${house}/tmp_2.txt" > "Results/${house}/tmp.txt"
	sed -e 's/Assignment:/%Assignment:/g' "Results/${house}/tmp.txt" > "Results/${house}/tmp_2.txt"
	sed -e 's/Cost:/%Cost:/g' "Results/${house}/tmp_2.txt" > "Results/${house}/tmp.txt"
	sed -e 's/)/)./g' "Results/${house}/tmp.txt" > "Results/${house}/tmp_2.txt"

	sed -e 's/COST/%COST/g' "Results/${house}/tmp_2.txt" > "Results/${house}/output_${house}_${date}.txt"


	clingcon "Results/${house}/output_${house}_${date}.txt" maxChargeKWh.asp mapping.asp --outf=1 > "Results/${house}/tmp.txt" 

	
	initChargeFile="Results/${house}/output_${house}_${date}_finalCharge.txt"

	sed -e 's/ANSWER/%ANSWER/g' "Results/${house}/tmp.txt" > "Results/${house}/tmp_2.txt"

	sed -e 's/Assignment:/%Assignment:/g' "Results/${house}/tmp_2.txt" > "Results/${house}/tmp.txt"

	sed -e 's/vFinalChargePercentage/vE_SinitPercentage/g' "Results/${house}/tmp.txt" > "Results/${house}/tmp_2.txt"

	sed -e 's/)/)./g' "Results/${house}/tmp_2.txt" > "Results/${house}/output_${house}_${date}_finalResults.txt"

	clingcon "Results/${house}/output_${house}_${date}_finalResults.txt" estractInitCharge.asp --outf=1 > "Results/${house}/tmp_2.txt" 

	sed -e 's/Assignment:/%Assignment:/g' "Results/${house}/tmp_2.txt" > "Results/${house}/tmp.txt"
	sed -e 's/)/)./g' "Results/${house}/tmp.txt" > "${initChargeFile}" 

	rm "Results/${house}/tmp.txt"
	rm "Results/${house}/tmp_2.txt"
     done
done

fi
