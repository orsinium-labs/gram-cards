#!/usr/bin/env bash
set -e

out="build"
font="PublicSans-Black.otf"

mkdir -p "$out"

# generate cards
n=0
cat phrases.txt | grep -v "^$" | while read phrase; do
  n=$((n+1))
  echo "$n. $phrase"
  convert \
    -background white \
    -fill '#2c3e50' \
    -font $font \
    -extent 760x1060 \
    -size 720x1060 \
    -bordercolor gray \
    -border 4x4 \
    -pointsize 96 \
    -gravity center \
    caption:"$phrase" \
    -fill '#95a5a6' \
    -pointsize 48 \
    -gravity SouthEast \
    -draw "text 40,40 '$n'" \
    "$out/$n.png"
done


# join cards

convert \
    '(' $out/{1,2,3}.png +append ')' \
    '(' $out/{4,5,6}.png +append ')' \
    '(' $out/{7,8,9}.png +append ')' \
    -background none \
    -append $out/result-01-09.png

convert \
    '(' $out/{10,11,12}.png +append ')' \
    '(' $out/{13,14,15}.png +append ')' \
    '(' $out/{16,17,18}.png +append ')' \
    -background none \
    -append $out/result-10-18.png

convert \
    '(' $out/{19,20,21}.png +append ')' \
    '(' $out/{22,23,24}.png +append ')' \
    '(' $out/{25,26,27}.png +append ')' \
    -background none \
    -append $out/result-19-27.png

