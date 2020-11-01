fcsv="input/catalog_example.csv"
fout="input/catalog_example"
cut -d ',' -f 2  $fcsv > lat
cut -d ',' -f 3  $fcsv > lon
cut -d ',' -f 5  $fcsv > mag
paste lon lat mag > $fout
rm lon lat mag
