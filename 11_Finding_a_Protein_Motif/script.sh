#!/usr/bin/env bash

# if [[ $# -ne 2 ]]; then
# 	echo "The code only cath one argument"
# 	exit 1
# fi

OUT_DIR=test/$2
if [[ ! -d $OUTDIR  ]]; then
	mkdir -p "$OUT_DIR"
fi 


while read -r prot_id; do
	prot_id="${prot_id//$'\r'/}"	
	echo "$prot_id"
	prot_url="${prot_id%%_*}"
	URL="https://www.uniprot.org/uniprot/${prot_url}.fasta"
	OUT_FILE="$OUT_DIR/${prot_id}.fasta"
	wget -q -O "$OUT_FILE" "$URL"
done < $1

echo "Done, see output in \"$OUT_DIR\"."
