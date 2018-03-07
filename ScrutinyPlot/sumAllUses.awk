BEGIN {ds = "start"}
{if (ds != "start" && ds != $1) {print ds "," size "," sumuse; sumuse = 0}}
{ds = $1; size = $2; sumuse = sumuse + $3}
END {print ds "," size "," sumuse}
