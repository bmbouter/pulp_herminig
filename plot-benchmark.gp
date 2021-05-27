set title "Tasking system benchmark"
set xlabel "Tasks (burst)"
set ylabel "avg dispatch time (s)"
set y2label "avg time in system (s)"

set log
set xtics nomirror scale 1, 0 2
unset x2tics
set ytics nomirror
set y2tics nomirror
set style data points

f(x) = a + b * x
g(x) = c + d * x

fit f(x) 'workers-old.data' u (log($1)):(log($5)) via a, b
fit g(x) 'workers-new.data' u (log($1)):(log($5)) via c, d

plot \
       'workers-old.data' u 1:($2*1e-9/$1) axes x1y1 title "old avg dispatch time", \
       '' u 1:5 axes x1y2 title "old avg time in system", \
       exp(f(log(x))) axes x1y2 title "fit", \
       'workers-new.data' u 1:($2*1e-9/$1) axes x1y1 title "new avg dispatch time", \
       '' u 1:5 axes x1y2 title "new avg time in system", \
       exp(g(log(x))) axes x1y2 title "fit"
