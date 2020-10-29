mkdir -p ./build/
n=0
cat phrases.txt | while read phrase; do
  n=$((n+1))
  echo "$n. $phrase"
  convert \
    -background white \
    -fill black \
    -font Ubuntu-Title \
    -extent 380x530 \
    -size 360x530 \
    -pointsize 56 \
    -gravity center \
    caption:"$phrase" \
    "./build/$n.png"
done

