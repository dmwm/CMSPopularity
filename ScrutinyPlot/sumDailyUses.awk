BEGIN {ds = "start"}
{if (ds != "start" && (ds != $1 || dt != $2)) {print ds "," dt "," cnt "," sumevts; sumevts = 0; cnt = 0}}
{ds = $1; dt = $2; sumevts = sumevts + $3; cnt = cnt + 1}
END {print ds "," dt "," cnt "," sumevts}
