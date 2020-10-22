touch /tmp/lockfile
flock -x /tmp/lockfile bash -c "read -p 'press enter to begin'"
date +%N > tm
hping3 --faster -1 -c 5000 10.0.0.5