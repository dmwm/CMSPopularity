BEGIN {ds = "start"}
{if (ds != "start" && ds != $1) {print ds "," sz / cnt "," beginDt "," endDt; beginDt = 0; endDt = 0; sz = 0; cnt = 0}}
{ds = $1; sz = sz + $2; firstDt = $3; secondDt = $4; cnt = cnt + 1}
{if (beginDt == 0 || firstDt < beginDt) {beginDt = firstDt}}
{if (endDt == 0 || secondDt > endDt) {endDt = secondDt}}
END {print ds "," sz / cnt "," beginDt "," endDt;}
