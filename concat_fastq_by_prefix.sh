#!/bin/bash

# Default values
input_dir="."
output_dir="."

# Help message
print_help() {
    echo "Usage: ./concatenate_by_prefix.sh -i [input_dir] -o [output_dir]"
    echo ""
    echo "Options:"
    echo "-i    Directory containing the FASTQ files (default: current directory)."
    echo "-o    Directory to save the concatenated files (default: current directory)."
    echo "-h    Show help message."
}

# Get options from command line arguments
while getopts ":i:o:h" opt; do
    case $opt in
        i) input_dir="$OPTARG";;
        o) output_dir="$OPTARG";;
        h) print_help; exit 0;;
        \?) echo "Invalid option -$OPTARG" >&2; exit 1;;
    esac
done

# Navigate to input directory
cd "$input_dir"

# Get unique prefixes
prefixes=$(ls *_1.fastq.gz 2>/dev/null | sed 's/_SRR.*//g' | uniq)

# Print unique prefixes line by line
echo "Unique Prefixes:"
for prefix in $prefixes; do
    echo "$prefix"
done
echo "-------------------------"

for prefix in $prefixes; do
    # Get sorted list of _1.fastq.gz files for the current prefix
    files_1=($(ls ${prefix}_SRR*_1.fastq.gz 2>/dev/null | sort))
    
    # Concatenate files with the current prefix and _1.fastq.gz
    cat "${files_1[@]}" > "${output_dir}/${prefix}_R1.fastq.gz"

    # Get sorted list of _2.fastq.gz files for the current prefix
    files_2=($(ls ${prefix}_SRR*_2.fastq.gz 2>/dev/null | sort))

    # Concatenate files with the current prefix and _2.fastq.gz
    cat "${files_2[@]}" > "${output_dir}/${prefix}_R2.fastq.gz"
done

# Navigate back to original directory
cd -

