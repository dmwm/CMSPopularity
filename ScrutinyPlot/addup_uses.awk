BEGIN {ds = "start"}
{if (ds == "start" || ds == $1) {cnt = cnt + 1} else {print ds "," dt "," cnt; cnt = 1}}
{ds = $1; dt = $2}
END {print ds "," dt "," cnt}
