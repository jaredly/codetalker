echo testing json parsing
python examples/prettyjson.py test/json/one.json
python examples/json.py test/json/one.json
echo
echo testing c parsing
echo 'parse'
python examples/parse_c.py test/c/hanoi.c > /dev/null
echo 'pretty'
python examples/prettyc.py test/c/hanoi.c > /dev/null
echo 'mini'
python examples/minify.py test/c/hanoi.c

exit
# disabling these for the moment... they take too long
echo "testing c snippets"
for i in test/c/more/*.c;do
    echo -n "parsing $i"
    python examples/prettyc.py $i>/dev/null
    echo -n "..parsed.."
done
echo
echo
echo "done testing"
