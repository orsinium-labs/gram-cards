#!/usr/bin/env bash
set -e

out="build"
font="/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Medium.ttf"

mkdir -p "$out"

# generate cards
n=0
cat phrases.txt | while read phrase; do
  n=$((n+1))
  echo "$n. $phrase"
  convert \
    -background white \
    -fill black \
    -font $font \
    -extent 380x530 \
    -size 360x530 \
    -bordercolor gray \
    -border 2x2 \
    -pointsize 56 \
    -gravity center \
    caption:"$phrase" \
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

