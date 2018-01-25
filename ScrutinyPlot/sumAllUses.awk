BEGIN {ds = "start"}
{if (ds != "start" && ds != $1) {print ds "," sz "," cnt; cnt = 0}}
{ds = $1; sz = $2; cnt = cnt + $6}
END {print ds "," sz "," cnt}
