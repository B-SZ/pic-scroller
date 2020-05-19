#!/bin/bash

main() {
    OUT="../pictures/"
    mkdir -p "$OUT"
    local COUNT="500"
    local TMP="$OUT/tmp.jpg"
    {
      yes 800 600 | head -n "$COUNT"
      yes 1024 768 | head -n "$COUNT"
    } |
    number_lines |
    shuf |
    number_lines |
    while read I OLD WIDTH HEIGHT; do
	echo "$I $OLD $WIDTH $HEIGHT" >&2
        local FILE="$OUT/`printf "%04d-${WIDTH}x$HEIGHT.jpg" "$I"`"
        genpic "$WIDTH" "$HEIGHT" > "$FILE"
        convert -scale ${WIDTH}x$HEIGHT "$FILE" "$TMP"
	jpegtopnm "$TMP" 2>/dev/null |
	ppmlabel -background black -size 72 -text "$I $WIDTH $HEIGHT" |
	pnmtojpeg > "$FILE"
    done
    rm "$TMP"
}

number_lines() {
 cat -n |sed "s~\t~ ~g"|tr -s " "|sed "s~^ ~~"
}

genpics() {
    local N="$1"
    local WIDTH="$2"
    local HEIGHT="$3"
    local TMP="$OUT/tmp.jpg"
    for I in `seq 1 $N`; do
        local FILE="$OUT/`printf "${WIDTH}x$HEIGHT-%03d.jpg" "$I"`"
        genpic "$WIDTH" "$HEIGHT" > "$FILE"
        convert -scale ${WIDTH}x$HEIGHT "$FILE" "$TMP"
	jpegtopnm "$TMP" 2>/dev/null |
	ppmlabel -background black -size 76 -text "$WIDTH $HEIGHT $I" |
	pnmtojpeg > "$FILE"
    done
}

genpic() {
    local IW="16"
    local IH="12"
    local PIXELS="`expr $IW \* $IH`"
    {
        cat <<EOF
P3
$IW $IH
255
EOF
    for PIXEL in `seq 1 $PIXELS`; do
        for RGB in `seq 1 3`; do
	    printf "%s " `expr $RANDOM % 256`
        done
	echo
    done
    } |
    ppmtojpeg
}

main "$@"
