#!/bin/bash
dirlist=('ls Facts/H*')
numFiles=${#dirlist[@]}

# rm -r Results
if [ -d Results ]; then
    echo "Directory Results already exists. Please remove it"
else

for (( i=1; i <= 20; i++ ))
#for (( i=1; i <= 1; i++ ))
do    
    initChargeFile="Facts/H${i}_Wh/asp/initCharge.asp"

    for filepath in "Facts/H${i}_Wh/asp"/*
    #for (( j=1; j <= 3; j++ ))  
    do    
      #echo "${initChargeFile}"
	#filepath="Facts/H${i}_Wh/asp/2020-01-0${j}.asp" 		
      factsFile="$filepath"  # Variabile con percorso completo
	date=${factsFile##*/}
	date="${date%.*}"
        echo "Executing ${date}"  
        mkdir -p "Results/H${i}"
        /home/dlv/Clingo/clingo-4.5.4-linux-x86_64/clingo encoding_article.asp params_article.asp maxChargeKwh.asp "${factsFile}" "${initChargeFile}" $1 --parallel-mode=8 --time-limit=1200 --quiet=1 --outf=1 > "Results/H${i}/output_H${i}_${date}.txt" 
	sed -e 's/ANSWER/%ANSWER/g' "Results/H${i}/output_H${i}_${date}.txt" > "Results/H${i}/tmp.txt"
	sed -e 's/OPTIMUM/%OPTIMUM/g' "Results/H${i}/tmp.txt" > "Results/H${i}/tmp_2.txt"
	sed -e 's/COST/%COST/g' "Results/H${i}/tmp_2.txt" > "Results/H${i}/output_H${i}_${date}.txt"
	/home/dlv/Clingo/clingo-4.5.4-linux-x86_64/clingo "Results/H${i}/output_H${i}_${date}.txt" maxChargeKwh.asp final_charge.asp --outf=1 > "Results/H${i}/tmp.txt" 
	echo "/home/dlv/Clingo/clingo-4.5.4-linux-x86_64/clingo Results/H${i}/output_H${i}_${date}.txt maxChargeKwh.asp final_charge.asp --outf=1 > Results/H${i}/tmp.txt"
	initChargeFile="Results/H${i}/output_H${i}_${date}_finalCharge.asp"
	sed -e 's/ANSWER/%ANSWER/g' "Results/H${i}/tmp.txt" > "Results/H${i}/tmp_2.txt"
	sed -e 's/vFinalChargePercentage/vE_SinitPercentage/g' "Results/H${i}/tmp_2.txt" > "${initChargeFile}"

	rm "Results/H${i}/tmp.txt"
	rm "Results/H${i}/tmp_2.txt"
     done
done

fi
