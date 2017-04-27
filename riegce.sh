sf=$1 # File where sentences are stored
cpus=7 # Assign number of cpus

AV=/almac/ignacio/rie_gce #$USTS

sents_dir=$(dirname "$sf")

source ~/.bashrc


if [ -z $ST ] || [ -z $FT ] || [ -z $DATA ]; then
    (>&2 echo "A directory is not in variables ST, FT or DATA.")
    (>&2 echo "Directories >>")
    (>&2 echo "Stanford: $ST")
    (>&2 echo "FastText: $FT")
    (>&2 echo "DATA: $DATA")
    exit 111;
fi

if [ ! -d "$sents_dir"/split_dir ]; then
    mkdir "$sents_dir"/split_dir
fi

split -a 5 -d -l 1 --additional-suffix=.splt "$sf" "$sents_dir"/split_dir/f_

N=$(cat "$sf" | wc -l)
Nf=$(find "$sents_dir"/split_dir/ -name "*splt" | wc -l)

if [[ !( "$Nf" == "$N" ) ]]; then
    (>&2 echo "Output line files amount does not match with input file")
    (>&2 echo "N = $N")
    (>&2 echo "Nfiles = $Nf")
    exit 111
fi

find "$sents_dir"/split_dir/ -name "*splt" > "$sents_dir"/split_dir/file_list
# Verify if files have been computed. If not do it.
#if [[ !( "$Nf" == "$N" ) && !( "$Nb" == "$N" ) || (("$ver" == "oie") || ("$ver" == "all")) ]]; then # If open files ie were not computed or they are wanted
java -mx1g -cp "$ST/*" edu.stanford.nlp.naturalli.OpenIE -triple.all_nominals true -format reverb\
                                                         -filelist "$sents_dir"/split_dir/file_list > "$sents_dir"/split_dir/oie_out.reverb
