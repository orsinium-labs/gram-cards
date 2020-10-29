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

echo 'join 1/1'
convert \
    '(' $out/{1,2,3,4}.png +append ')' \
    '(' $out/{5,6,7,8}.png +append ')' \
    '(' $out/{9,10,11,12}.png +append ')' \
    '(' $out/{13,14,15,16}.png +append ')' \
    -background none \
    -append $out/result-01-16.png

echo 'join 2/2'
convert \
    '(' $out/{17,18,19,20}.png +append ')' \
    '(' $out/{21,22,23,24}.png +append ')' \
    '(' $out/{25,26,27}.png +append ')' \
    -background none \
    -append $out/result-17-27.png

