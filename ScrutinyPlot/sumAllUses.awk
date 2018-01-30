BEGIN {ds = "start"}
{if (ds != "start" && ds != $1) {print ds "," cnt "," sumbytes; cnt = 0; sumbytes = 0}}
{ds = $1; cnt = cnt + $2; sumbytes = sumbytes + $3}
END {print ds "," cnt "," sumbytes}
