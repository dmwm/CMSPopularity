BEGIN {ds = "start"}
{if (ds != "start" && (ds != $1 || dt != $2)) {print ds "," dt "," sumevts; sumevts = 0}}
{ds = $1; dt = $2; sumevts = sumevts + $3}
END {print ds "," dt "," sumevts}
