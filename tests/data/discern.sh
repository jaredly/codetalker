
for i in c/more/*.c;do
    echo "looking at $i"
    if [ -z "`~/clone/codetalker/examples/parse_c.py $i -q 2>&1`" ];then
        echo "good"
    else
        echo "bad"
        mv $i c/more/problem/
    fi
done
