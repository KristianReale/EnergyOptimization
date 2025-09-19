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
    initChargeFile="initCharge.asp"

    for filepath in Facts/*_KWh.asp
    #for (( j=1; j <= 3; j++ ))  
    do    
      #echo "${initChargeFile}"
      house="cubo"
      factsFile="$filepath"  # Variabile con percorso completo
	date=${factsFile##*/}
	date="${date%.*}"
        echo "Executing ${date}"  
        mkdir -p "Results/${house}"
        clingo ../../encoding_article.asp params_article.asp maxChargeKWh.asp "${factsFile}" "${initChargeFile}" $1 --parallel-mode=8 --time-limit=1200 --quiet=1 --outf=1 > "Results/${house}/output_${house}_${date}.txt" 
#        clingo ../../encoding_article.asp params_article.asp maxChargeKWh.asp "${factsFile}" "${initChargeFile}" $1 --parallel-mode=8 -n 15 --outf=1 > "Results/${house}/output_${house}_${date}.txt" 
	sed -e 's/ANSWER/%ANSWER/g' "Results/${house}/output_${house}_${date}.txt" > "Results/${house}/tmp.txt"
	sed -e 's/OPTIMUM/%OPTIMUM/g' "Results/${house}/tmp.txt" > "Results/${house}/tmp_2.txt"
	sed -e 's/COST/%COST/g' "Results/${house}/tmp_2.txt" > "Results/${house}/output_${house}_${date}.txt"
	clingo "Results/${house}/output_${house}_${date}.txt" maxChargeKWh.asp final_charge.asp --outf=1 > "Results/${house}/tmp.txt" 
	echo "clingo Results/${house}/output_${house}_${date}.txt maxChargeKWh.asp final_charge.asp --outf=1 > Results/${house}/tmp.txt"
	initChargeFile="Results/${house}/output_${house}_${date}_finalCharge.asp"
	sed -e 's/ANSWER/%ANSWER/g' "Results/${house}/tmp.txt" > "Results/${house}/tmp_2.txt"
	sed -e 's/vFinalChargePercentage/vE_SinitPercentage/g' "Results/${house}/tmp_2.txt" > "${initChargeFile}"

	rm "Results/${house}/tmp.txt"
	rm "Results/${house}/tmp_2.txt"
     done
done

fi
